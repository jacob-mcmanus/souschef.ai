import os
import json
import re
import time
import numpy as np
import matplotlib.pyplot as plt

from recipe_analyzer import RecipeAnalyzer, APITokenError

# Set up global variables and constants
MODEL_NAMES = ["Gemma-2B-Instruct"] #["Gemma-2B-Instruct", "Llama-3.2-1B-Instruct", "Llama-3.2-3B-Instruct", "Mistral-7B-v0.1"]
PARSING_BASE_DIR = os.path.join("test", "parsing")
GROUND_TRUTH_DIR = os.path.join("test", "value")
API_RESPONSE_DIR = "api_responses"
API_KEY = "2ef0bf9b42284292a74dde09b7690ae2"
METRICS = ["Calories", "Protein", "Fat", "Carbohydrates", "Price"]
RESULTS_FILENAME = "model_performance_results.json"

# --- Functions for reading and cleaning up the data ---
def parse_ground_truth(file_path):
    # Reads the correct answer file (the ground truth) and pulls out the numbers.
    try:
        with open(file_path, 'r') as f: content = f.read()
    except FileNotFoundError: return None
    patterns = { "Calories": r"Calories:\s*([\d\.]+)", "Protein": r"Protein:\s*([\d\.]+)", "Fat": r"Fat:\s*([\d\.]+)", "Carbohydrates": r"Carbohydrates:\s*([\d\.]+)", "Price": r"Cost:\s*\$([\d\.]+)"}
    truth_values = {key: float(match.group(1)) if (match := re.search(pattern, content)) else 0.0 for key, pattern in patterns.items()}
    return truth_values

def parse_api_output(api_result):
    # Takes the API's raw JSON output and organizes it into a clean dictionary.
    parsed = {key: float(value) for key, value in api_result.get("summary", {}).items()}
    parsed["Price"] = float(api_result.get("price", "$0.00").replace('$', ''))
    return parsed

# --- The main functions that do the heavy lifting ---
def collect_recipe_errors(analyzer):
    # Goes through each recipe, sends it to the API, and calculates the error for each metric.
    # It returns a big dictionary with all the individual errors.
    model_errors = {model: {m: {'abs_err': [], 'pct_err': []} for m in METRICS} for model in MODEL_NAMES}
    token_limit_reached = False

    for model in MODEL_NAMES:
        if token_limit_reached: break
        print(f"\n--- Processing Model: {model} ---")
        model_dir = os.path.join(PARSING_BASE_DIR, model)
        if not os.path.isdir(model_dir): continue
        
        json_files = sorted([f for f in os.listdir(model_dir) if f.startswith('parsed_json_out_') and f.endswith('.json')])
        
        for json_file in json_files:
            try:
                file_id = json_file.replace('parsed_json_out_', '').replace('.json', '')
                print(f"Analyzing recipe ID: {file_id}...")
                json_path = os.path.join(model_dir, json_file)
                with open(json_path, 'r') as f: llm_parsed_list = json.load(f)
                
                # Load the correct values to compare against.
                truth_path = os.path.join(GROUND_TRUTH_DIR, f"value_out_{file_id}.txt")
                ground_truth = parse_ground_truth(truth_path)
                if not ground_truth:
                    print(f"   -> Skipping recipe {file_id}: Ground truth not found.")
                    continue
                
                # This is where we actually call the external API.
                api_result = analyzer.analyze_recipe(llm_parsed_list)
                
                # Save the raw response from the API just in case we need it.
                api_output_dir = os.path.join(API_RESPONSE_DIR, model)
                api_output_path = os.path.join(api_output_dir, f"api_response_{model}_{file_id}.json")
                with open(api_output_path, 'w') as f:
                    json.dump(api_result, f, indent=4)
                
                # Calculate the errors between our result and the actual answer.
                api_values = parse_api_output(api_result)
                for metric in METRICS:
                    actual = api_values.get(metric, 0)
                    expected = ground_truth.get(metric, 0)
                    model_errors[model][metric]['abs_err'].append(abs(actual - expected))
                    model_errors[model][metric]['pct_err'].append(percentage_error(actual, expected) * 100)
                
                # Pause for a few seconds to not overwhelm the API.
                time.sleep(3)

            except APITokenError as e:
                # If we run out of API credits, stop and just analyze what we have.
                print(f"\n{e}\nStopping data collection. Proceeding to analysis...")
                token_limit_reached = True
                break
    
    return model_errors

def calculate_aggregate_metrics(model_errors):
    # Averages out all the individual errors to get the final MAE and MAPE.
    final_results = {}
    for model, metrics_data in model_errors.items():
        final_results[model] = {}
        # Skip if no data was collected for this model.
        if not any(metrics_data[m]['abs_err'] for m in METRICS):
            continue

        for metric, errors in metrics_data.items():
            mae = np.mean(errors['abs_err']) if errors['abs_err'] else 0
            mape = np.mean(errors['pct_err']) if errors['pct_err'] else 0
            final_results[model][metric] = {'mae': mae, 'mape': mape}
            
    return final_results

# --- Functions for showing the results ---
def save_results_to_json(results, filename):
    # Saves the final results to a JSON file so we don't have to run this whole script again.
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\nFinal model performance metrics saved to {filename}\n")

def print_summary_to_console(results):
    # Just prints a simple summary of the results to the terminal.
    for model, model_results in results.items():
        print(f"--- Overall Results for Model: {model} ---")
        if not model_results:
            print("   No data collected for this model.")
            continue
        for metric, values in model_results.items():
            print(f"   {metric:<15}: MAE = {values['mae']:6.1f}, MAPE = {values['mape']:5.1f}%")

def plot_model_performance(results):
    # Creates a bar chart to easily compare how well each model did.
    n_metrics = len(METRICS)
    model_labels = [name.replace("-Instruct", "").replace("-v0.1", "") for name in results.keys()]
    x = np.arange(len(model_labels))
    width = 0.15 
    fig, ax = plt.subplots(figsize=(18, 9))

    # Create a group of bars for each metric.
    for i, metric in enumerate(METRICS):
        mape_values = [results.get(model, {}).get(metric, {}).get('mape', 0) for model in results.keys()]
        offset = width * (i - n_metrics / 2 + 0.5)
        rects = ax.bar(x + offset, mape_values, width, label=f"{metric} MAPE")
        ax.bar_label(rects, padding=3, fmt='%.1f%%', rotation=90, size=8)

    # Make the plot look nice.
    ax.set_ylabel('Mean Absolute Percentage Error (MAPE %)')
    ax.set_title('LLM Performance Comparison: Recipe Analysis Accuracy')
    ax.set_xticks(x)
    ax.set_xticklabels(model_labels, rotation=15, ha="right")
    ax.legend(loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    
    # Save the plot to a file.
    plt.savefig('model_performance_comparison.png', dpi=300)
    print("Model performance plot saved to model_performance_comparison.png")
    ax.set_title("")
    plt.savefig('model_performance_comparison_no_title.png', dpi=300)
    print("Model performance plot (no title) saved to model_performance_comparison_no_title.png")
    plt.close(fig)

def percentage_error(actual, expected):
    # Simple formula for percentage error. Handles cases where the correct answer is zero.
    if expected == 0 and actual == 0: return 0.0
    if expected == 0: return 1.0 # Represents 100% error if we get a value but expected zero.
    return abs((actual - expected) / expected)

# --- This is where the script actually runs ---
def main():
    # Puts all the functions together to run the whole analysis from start to finish.
    
    # Step 1: Get everything ready.
    if not API_KEY:
        print("Error: SPOONACULAR_API_KEY environment variable not set.")
        return
    analyzer = RecipeAnalyzer(api_key=API_KEY)
    os.makedirs(API_RESPONSE_DIR, exist_ok=True)
    for model in MODEL_NAMES:
        os.makedirs(os.path.join(API_RESPONSE_DIR, model), exist_ok=True)

    # Step 2: Run the API calls and collect the data.
    raw_errors = collect_recipe_errors(analyzer)

    # Step 3: Calculate the final average errors.
    final_results = calculate_aggregate_metrics(raw_errors)
    
    # Step 4: Save and print the results.
    if not final_results:
        print("\nNo data was successfully collected. Cannot generate analysis.")
        return
        
    print("\n--- Analysis Complete ---")
    save_results_to_json(final_results, RESULTS_FILENAME)
    print_summary_to_console(final_results)
    
    # Step 5: Create the comparison chart.
    plot_model_performance(final_results)

if __name__ == "__main__":
    main()