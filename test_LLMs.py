import os
import json
import time
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import torch
from llm import LLM, recipe_parser as rp

def ingredient_to_tuple(ingredient):
    """
    Converts a parsed ingredient dictionary to a standardized tuple representation.
    """
    try:
        # Round quantity to handle minor floating point discrepancies.
        quantity = round(float(ingredient.get("quantity")), 2)
    except (ValueError, TypeError):
        # If quantity is missing or not a number, default to 0.0 for consistency.
        quantity = 0.0

    unit = ingredient.get("unit")
    return (
        ingredient.get("ingredient", "").strip().lower(),
        quantity,
        # Ensure unit is also standardized (lowercase, stripped) or None.
        (unit.strip().lower() if unit else None)
    )

def load_ingredients_from_json(json_path):
    """
    Loads a set of standardized ingredient tuples from a ground-truth JSON file.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Use a set comprehension for concise and efficient creation of the ingredient set.
    return {ingredient_to_tuple(ing) for ing in data if "ingredient" in ing}

def compute_f1(gt, pred):
    """
    Computes precision, recall, and F1 score for two sets of items.
    """
    # True Positives (tp): Items correctly identified by the model.
    # This is the intersection of the ground truth and prediction sets.
    tp = len(gt.intersection(pred))

    # False Positives (fp): Items the model predicted but were not in the ground truth.
    # This is the set of items in the prediction that are not in the ground truth.
    fp = len(pred.difference(gt))

    # False Negatives (fn): Items the model failed to identify.
    # This is the set of items in the ground truth that are not in the prediction.
    fn = len(gt.difference(pred))

    # Precision: Of all the items the model predicted, how many were correct?
    # Measures the exactness of the model.
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    # Recall: Of all the actual items, how many did the model find?
    # Measures the completeness of the model.
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    # F1 Score: The harmonic mean of precision and recall. It provides a single
    # score that balances both concerns. Useful for comparing models.
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

def process_single_recipe(llm, recipe_file, gt_path, out_path):
    """
    Processes a single recipe file, runs LLM inference, and calculates performance metrics.
    """
    with open(recipe_file, "r", encoding="utf-8") as f:
        raw_input_text = f.read()

    # Pre-process the input text into a standardized prompt for the LLM.
    prompt = rp.pre_process_input(raw_input_text)
    
    # Time the inference call to measure model speed.
    start_time = time.time()
    response = llm.run(prompt)
    elapsed = time.time() - start_time

    # Extract the JSON object from the model's text output.
    pred_json = rp.extract_json_from_output(response)

    # Save the model's direct output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pred_json, f, indent=2)

    # Load ground truth and predictions into standardized sets for comparison.
    gt_ings = load_ingredients_from_json(gt_path)
    pred_ings = {ingredient_to_tuple(ing) for ing in pred_json if "ingredient" in ing}

    # --- METRIC CALCULATIONS ---

    # 1. Calculate Precision, Recall, and F1 on the full (name, qty, unit) tuple.
    p, r, f1 = compute_f1(gt_ings, pred_ings)

    # 2. Calculate F1 on ingredient names only to see how well the model identifies
    #    the correct ingredients, regardless of whether it gets the quantity/unit right.
    gt_names = {i[0] for i in gt_ings}
    pred_names = {i[0] for i in pred_ings}
    _, _, name_f1 = compute_f1(gt_names, pred_names)

    # 3. Calculate accuracy for quantity and unit, but ONLY for ingredients that
    #    the model correctly identified by name. This avoids penalizing the model twice.
    common_names = gt_names & pred_names
    # Create dictionary maps for lookup of ingredient details by name.
    gt_map = {i[0]: i for i in gt_ings}
    pred_map = {i[0]: i for i in pred_ings}

    # Count how many quantities and units match for the common ingredients.
    qty_correct = sum(gt_map[n][1] == pred_map[n][1] for n in common_names)
    unit_correct = sum(gt_map[n][2] == pred_map[n][2] for n in common_names)

    # Calculate accuracy as a percentage. Handle the case of no common names to avoid division by zero.
    qty_acc = qty_correct / len(common_names) if common_names else 0.0
    unit_acc = unit_correct / len(common_names) if common_names else 0.0

    return p, r, f1, name_f1, qty_acc, unit_acc, elapsed

def evaluate_model(model_class, model_name):
    """
    Runs the full evaluation pipeline for a single model across all test recipes.
    """
    print(f"Evaluating {model_name}...")

    # Set up directories
    base_dir = Path("test")
    recipe_dir = base_dir / "recipe"
    gt_dir = base_dir / "json"
    parsed_output_dir = base_dir / "parsing" / model_name
    # Create the output directory for this model's results if it doesn't exist.
    parsed_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Find all recipe text files in the directory.
        recipe_files = sorted([f for f in recipe_dir.iterdir() if f.name.startswith("recipe_in_") and f.suffix == ".txt"])
        print(f"Found {len(recipe_files)} recipes.")
        if not recipe_files:
            print("Warning: No recipe files found. Aborting evaluation for this model.")
            return None
    except FileNotFoundError:
        print(f"Error: Directory not found at {recipe_dir}. Please ensure the test files are in the correct location.")
        return None

    # Initialize a dictionary to aggregate metrics across all recipes.
    metrics = {
        "precision": 0.0, "recall": 0.0, "f1": 0.0,
        "name_f1": 0.0, "qty_accuracy": 0.0, "unit_accuracy": 0.0,
        "time": 0.0, "count": 0
    }

    # Instantiate the LLM. This might load the model into memory/VRAM.
    llm = model_class()

    # Loop through each recipe file for processing.
    for recipe_file in recipe_files:
        # Extract the unique index from the filename to find the matching ground-truth file.
        file_index = recipe_file.stem.split("_")[-1]
        gt_path = gt_dir / f"json_out_{file_index}.json"
        out_path = parsed_output_dir / f"parsed_json_out_{file_index}.json"

        # Skip if the corresponding ground-truth file is missing.
        if not gt_path.exists():
            print(f"Missing ground truth for recipe {file_index}, skipping.")
            continue

        try:
            # Process the recipe and get the metrics.
            p, r, f1, name_f1, qty_acc, unit_acc, elapsed = process_single_recipe(llm, recipe_file, gt_path, out_path)
            
            # Add the results for this recipe to the aggregate totals.
            metrics["precision"] += p
            metrics["recall"] += r
            metrics["f1"] += f1
            metrics["name_f1"] += name_f1
            metrics["qty_accuracy"] += qty_acc
            metrics["unit_accuracy"] += unit_acc
            metrics["time"] += elapsed
            metrics["count"] += 1
            print(f"  Processed recipe {file_index} in {elapsed:.2f}s")
        except Exception as e:
            # Catch potential errors during processing of a single file to allow the script to continue.
            print(f"  Failed on recipe {file_index}: {e}")

    # After processing all recipes, calculate the average for each metric.
    count = metrics["count"]
    if count > 0:
        for key in ["precision", "recall", "f1", "name_f1", "qty_accuracy", "unit_accuracy", "time"]:
            metrics[key] /= count

        # Print a summary of the results to the console.
        print(f"\n=== {model_name} Results ({count} recipes) ===")
        print(f"Avg Precision: {metrics['precision']:.4f}")
        print(f"Avg Recall:    {metrics['recall']:.4f}")
        print(f"Avg F1:        {metrics['f1']:.4f}")
        print(f"Name F1:       {metrics['name_f1']:.4f}")
        print(f"Qty Accuracy:  {metrics['qty_accuracy']:.4f}")
        print(f"Unit Accuracy: {metrics['unit_accuracy']:.4f}")
        print(f"Avg Time:      {metrics['time']:.2f} sec")
    else:
        print(f"No recipes were evaluated successfully for {model_name}.")

    metrics["model"] = model_name
    return metrics

def visualize_results(results):
    """
    Generates and saves bar chart plots to compare all evaluated models.

    Args:
        results: A list of result dictionaries, one for each model evaluated.
    """
    if not results:
        print("No results to visualize.")
        return

    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)
    
    models = [r["model"] for r in results]
    num_recipes = results[0].get("count", 'N/A')
    # `x` provides the positions for the groups of bars.
    x = np.arange(len(models))
    # `width` is the width of a single bar.
    width = 0.35

    # --- Plot 1: F1 Scores ---
    fig1, ax1 = plt.subplots(figsize=(12, 7))
    # Plot two bars for each model, slightly offset from the center `x` position.
    ax1.bar(x - width/2, [r["f1"] for r in results], width, label='F1 (Full Tuple)')
    ax1.bar(x + width/2, [r["name_f1"] for r in results], width, label='F1 (Names Only)')
    ax1.set(
        ylabel='F1 Score',
        title=f'Model F1 Scores ({num_recipes} recipes)',
        xticks=x,
        xticklabels=models,
        ylim=(0, 1.05) # Set y-limit slightly above 1.0 for better visuals.
    )
    ax1.legend()
    # Rotate x-axis labels to prevent them from overlapping.
    plt.setp(ax1.get_xticklabels(), rotation=15, ha="right")
    fig1.tight_layout() # Adjust plot to ensure everything fits without overlapping.
    fig1.savefig(output_dir / "f1_scores.png", dpi=300)
    print(f"\nPlot saved to {output_dir / 'f1_scores.png'}")
    
    # Save a version with no title for use in reports or presentations.
    ax1.set_title("")
    fig1.savefig(output_dir / "f1_scores_no_title.png", dpi=300)
    print(f"Plot saved to {output_dir / 'f1_scores_no_title.png'}")

    # --- Plot 2: Quantity & Unit Accuracy ---
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    ax2.bar(x - width/2, [r["qty_accuracy"] for r in results], width, label='Quantity Accuracy')
    ax2.bar(x + width/2, [r["unit_accuracy"] for r in results], width, label='Unit Accuracy')
    ax2.set(
        ylabel='Accuracy',
        title=f'Quantity & Unit Accuracy ({num_recipes} recipes)',
        xticks=x,
        xticklabels=models,
        ylim=(0, 1.05)
    )
    ax2.legend()
    plt.setp(ax2.get_xticklabels(), rotation=15, ha="right")
    fig2.tight_layout()
    fig2.savefig(output_dir / "accuracy.png", dpi=300)
    print(f"Plot saved to {output_dir / 'accuracy.png'}")

    # Save a version with no title.
    ax2.set_title("")
    fig2.savefig(output_dir / "accuracy_no_title.png", dpi=300)
    print(f"Plot saved to {output_dir / 'accuracy_no_title.png'}")

    # --- Plot 3: Inference Time ---
    fig3, ax3 = plt.subplots(figsize=(12, 7))
    # This is a single bar plot, so no offset is needed.
    ax3.bar(x, [r["time"] for r in results], width, color='skyblue')
    ax3.set(
        ylabel='Seconds',
        title=f'Average Inference Time per Recipe ({num_recipes} recipes)',
        xticks=x,
        xticklabels=models
    )
    plt.setp(ax3.get_xticklabels(), rotation=15, ha="right")
    fig3.tight_layout()
    fig3.savefig(output_dir / "inference_time.png", dpi=300)
    print(f"Plot saved to {output_dir / 'inference_time.png'}")
    
    # Save a version with no title.
    ax3.set_title("")
    fig3.savefig(output_dir / "inference_time_no_title.png", dpi=300)
    print(f"Plot saved to {output_dir / 'inference_time_no_title.png'}")

    # Display the plots interactively after saving.
    plt.show()

def main():
    # A dictionary mapping model names to their corresponding class constructors.
    # This makes it easy to add or remove models from the evaluation.
    models_to_evaluate = {
        "Llama-3.2-1B-Instruct": LLM.Llama_3_2_1B_LLM,
        "Llama-3.2-3B-Instruct": LLM.Llama_3_2_3B_LLM,
        "Gemma-2B-Instruct": LLM.Gemma_2B_LLM,
        "Mistral-7B-v0.1": LLM.Mistral_LLM,
    }

    # Generate a timestamped filename for the text results.
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"{date_str}_evaluation_results.txt"
    
    # Remove old results file if it exists to prevent appending to old data.
    if os.path.exists(output_filename):
        os.remove(output_filename)

    all_results = []
    # Iterate through the models defined above.
    for model_name, model_class in models_to_evaluate.items():
        llm = None # Initialize llm to None for the finally block.
        try:
            print(f"\n{'='*20} Starting: {model_name} {'='*20}")
            model_results = evaluate_model(model_class, model_name)
            
            # Only process and save results if the evaluation was successful.
            if model_results and model_results["count"] > 0:
                all_results.append(model_results)
                
                # Format the results into a readable string.
                num_recipes = model_results.get("count", 'N/A')
                results_header = f"\n===== {model_name} Results ({num_recipes} recipes) ====="
                results_body = [
                    f"Avg F1 Score (full tuple):  {model_results['f1']:.4f}",
                    f"Avg F1 Score (names only):  {model_results['name_f1']:.4f}",
                    "---",
                    f"Avg Quantity Accuracy:      {model_results['qty_accuracy']:.4f}",
                    f"Avg Unit Accuracy:          {model_results['unit_accuracy']:.4f}",
                    "---",
                    f"Avg Time per Recipe:        {model_results['time']:.2f} seconds"
                ]
                
                # Append the results for the current model to the output file.
                with open(output_filename, 'a', encoding='utf-8') as f:
                    f.write(results_header + "\n" + "\n".join(results_body) + "\n")
        except Exception as e:
            print(f"\nAn error occurred during evaluation of {model_name}: {e}")
        finally:
            # This block is crucial for managing GPU memory (VRAM).
            # It ensures that the model and tokenizer are deleted and VRAM is cleared,
            # even if an error occurred, preventing memory overflows when loading the next model.
            if llm is not None:
                print(f"Unloading {model_name} to free VRAM...")
                if hasattr(llm, 'model'): del llm.model
                if hasattr(llm, 'tokenizer'): del llm.tokenizer
                del llm
                torch.cuda.empty_cache()
                print("VRAM freed.")
        print(f"{'='*20} Finished: {model_name} {'='*20}")

    # After all models have been evaluated, generate the comparison plots.
    if all_results:
        visualize_results(all_results)

# Standard Python entry point.
if __name__ == "__main__":
    main()
