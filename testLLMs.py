from llm import LLM, recipe_parser as rp
import json
import os
import time
import torch
from typing import Tuple, Set

def ingredient_to_tuple(ingredient: dict) -> Tuple[str, float, str]:
    """Converts a parsed ingredient dictionary to a standardized tuple."""
    try:
        quantity = round(float(ingredient.get("quantity")), 2)
    except (ValueError, TypeError):
        quantity = 0.0

    unit = ingredient.get("unit")
    return (
        ingredient.get("ingredient", "").strip().lower(),
        quantity,
        (unit.strip().lower() if unit else None)
    )

def load_ingredients_from_json(json_path: str) -> Set[Tuple[str, float, str]]:
    """Loads a set of standardized ingredient tuples from a ground-truth JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {ingredient_to_tuple(ing) for ing in data if "ingredient" in ing}

def compute_f1(gt: set, pred: set) -> Tuple[float, float, float]:
    """Computes precision, recall, and F1 score for two sets."""
    # True Positives (tp): Items that are in both the ground truth and the prediction.
    # These are the correctly identified items.
    tp = len(gt.intersection(pred))
    # False Positives (fp): Items that are in the prediction but not in the ground truth.
    # These are items the model incorrectly identified.
    fp = len(pred.difference(gt))
    # False Negatives (fn): Items that are in the ground truth but not in the prediction.
    # These are items the model missed.
    fn = len(gt.difference(pred))

    # Precision: What proportion of predicted items were correct?
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    # Recall: What proportion of actual items were correctly identified?
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    # F1 Score: The harmonic mean of precision and recall.
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

def evaluate_model(llm, model_name: str, base_dir: str = "testing", output_file_path: str = None) -> None:
    """
    Evaluates an LLM's recipe parsing performance against a directory of
    recipes and their corresponding ground-truth JSON files.
    """
    recipe_dir = os.path.join(base_dir, "recipe_in")
    gt_dir = os.path.join(base_dir, "json_out")

    # --- Totals for calculating averages ---
    total_precision, total_recall, total_f1 = 0.0, 0.0, 0.0
    total_name_f1 = 0.0
    total_qty_accuracy = 0.0
    total_unit_accuracy = 0.0
    total_time = 0.0
    count = 0

    # --- Restored original loop to test recipes 1 through 10 ---
    for i in range(1, 21):
        recipe_path = os.path.join(recipe_dir, f"recipe_{i}.txt")
        gt_path = os.path.join(gt_dir, f"recipe_{i}.json")

        if not os.path.exists(recipe_path) or not os.path.exists(gt_path):
            continue

        with open(recipe_path, "r", encoding="utf-8") as f:
            raw_input_text = f.read()

        prompt = rp.pre_process_input(raw_input_text)

        start_time = time.time()
        response = llm.run(prompt)
        elapsed = time.time() - start_time

        try:
            pred_json = rp.extract_json_from_output(response)
            gt_ings = load_ingredients_from_json(gt_path)
            pred_ings = {ingredient_to_tuple(ing) for ing in pred_json if "ingredient" in ing}

            # --- METRIC 1: F1 Score for the full ingredient tuple (name, quantity, unit) ---
            # This is the strictest metric. An ingredient is only a "match" if all three parts are identical.
            precision, recall, f1 = compute_f1(gt_ings, pred_ings)
            total_precision += precision
            total_recall += recall
            total_f1 += f1

            # --- METRIC 2: F1 Score for ingredient names only ---
            # This is a more lenient metric to see if the model can identify the correct ingredients,
            # even if it gets the quantities or units wrong.
            gt_names = {i[0] for i in gt_ings}
            pred_names = {i[0] for i in pred_ings}
            _, _, name_f1 = compute_f1(gt_names, pred_names)
            total_name_f1 += name_f1

            # --- METRIC 3 & 4: Accuracy for quantity and unit on correctly identified ingredients ---
            # To calculate this, we only look at ingredients that were correctly identified by name
            # in both the ground truth and the prediction.
            
            # Create dictionaries to easily look up an ingredient's full tuple by its name.
            gt_map = {i[0]: i for i in gt_ings}
            pred_map = {i[0]: i for i in pred_ings}
            # Find the set of ingredient names that appear in both ground truth and prediction.
            common_names = gt_names.intersection(pred_names)

            qty_correct, unit_correct = 0, 0
            if common_names:
                # For each correctly identified ingredient, check if its quantity and unit also match.
                for name in common_names:
                    # Check if the quantity (index 1) is the same.
                    if gt_map[name][1] == pred_map[name][1]:
                        qty_correct += 1
                    # Check if the unit (index 2) is the same.
                    if gt_map[name][2] == pred_map[name][2]:
                        unit_correct += 1
                
                # Calculate accuracy as the fraction of correct items over the number of common ingredients.
                # This avoids penalizing the model twice for missing an ingredient entirely.
                total_qty_accuracy += qty_correct / len(common_names)
                total_unit_accuracy += unit_correct / len(common_names)
            
            total_time += elapsed
            count += 1
        except Exception as e:
            print(f"[{model_name}] Failed on recipe_{i}: {e}")

    if count > 0:
        # --- Calculate Averages ---
        avg_precision = total_precision / count
        avg_recall = total_recall / count
        avg_f1 = total_f1 / count
        avg_name_f1 = total_name_f1 / count
        avg_qty_accuracy = total_qty_accuracy / count
        avg_unit_accuracy = total_unit_accuracy / count
        avg_time = total_time / count

        # --- Format results for printing and file output ---
        results_header = f"\n===== {model_name} Results ({count} recipes) ====="
        results_body = [
            f"Avg Precision (full tuple): {avg_precision:.4f}",
            f"Avg Recall (full tuple):    {avg_recall:.4f}",
            f"Avg F1 Score (full tuple):  {avg_f1:.4f}",
            "---",
            f"Avg F1 Score (names only):  {avg_name_f1:.4f}",
            "---",
            f"Avg Quantity Accuracy (on matched ingredients): {avg_qty_accuracy:.4f}",
            f"Avg Unit Accuracy (on matched ingredients):     {avg_unit_accuracy:.4f}",
            "---",
            f"Avg Time per Recipe: {avg_time:.2f} seconds"
        ]
        
        # --- Print to console ---
        print(results_header)
        for line in results_body:
            print(line)

        # --- Write to output file if path is provided ---
        if output_file_path:
            with open(output_file_path, 'a', encoding='utf-8') as f:
                f.write(results_header + "\n")
                f.write("\n".join(results_body) + "\n")
    else:
        message = f"No successful evaluations for {model_name}"
        print(message)
        if output_file_path:
            with open(output_file_path, 'a', encoding='utf-8') as f:
                f.write(message + "\n")
        
def main():
    # A dictionary mapping a descriptive name to the LLM class.
    # This allows us to loop through and test them one by one.
    # Speeds up testing because I don't have to wait for the code to finish
    models_to_evaluate = {
        "Llama-3.2 1B Instruct": LLM.Llama_3_2_1B_LLM,
        "Llama-3.2 3B Instruct": LLM.Llama_3_2_3B_LLM,
        "Gemma 2B Instruct": LLM.Gemma_2B_LLM,
        "Mistral 7B v0.1": LLM.Mistral_LLM,
    }

    output_filename = "evaluation_results.txt"
    print(f"Evaluation results will be saved to {output_filename}")

    # Clear the file at the start of a new full run
    if os.path.exists(output_filename):
        os.remove(output_filename)

    for model_name, model_class in models_to_evaluate.items():
        print(f"\n{'='*20} Evaluating: {model_name} {'='*20}")
        llm = None # LLM instance
        try:
            print("Loading model...")
            llm = model_class()
            evaluate_model(llm, model_name, output_file_path=output_filename)
        except Exception as e:
            print(f"An error occurred during evaluation of {model_name}: {e}")
        finally: # Delete the llm instance if it exists. Otherwise our GPUs WILL DIE.
            if llm is not None:
                print(f"Unloading {model_name} to free VRAM...")
                if hasattr(llm, 'model'): del llm.model
                if hasattr(llm, 'tokenizer'): del llm.tokenizer
                del llm
                torch.cuda.empty_cache()
                print("VRAM freed.")
        print(f"{'='*20} Finished: {model_name} {'='*20}")

if __name__ == "__main__":
    main()
