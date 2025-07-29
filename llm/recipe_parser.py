from fractions import Fraction
import re
import json

def unicode_fraction_to_float(text):
    fraction_map = {
        '½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4',
        '¾': '3/4', '⅕': '1/5', '⅖': '2/5', '⅗': '3/5',
        '⅘': '4/5', '⅙': '1/6', '⅚': '5/6', '⅛': '1/8',
        '⅜': '3/8', '⅝': '5/8', '⅞': '7/8'
    }
    for uf, frac in fraction_map.items():
        text = text.replace(uf, str(float(Fraction(frac))))
    return text

def pre_process_input(recipe):
    """
    Formats the raw recipe text for the LLM.
    """
    processed_recipe = unicode_fraction_to_float(recipe)
    
    final_prompt = (
        "You are an expert recipe parser. Extract the ingredients from the following text "
        "into a structured JSON array. \n"
        "Rules:\n"
        "1. 'ingredient' must be lowercase and singular (e.g., 'eggs' -> 'egg').\n"
        "2. 'quantity' MUST be a numeric decimal value. Do not use strings.\n"
        "3. If a quantity is ambiguous or non-numeric (e.g., 'to taste', 'a pinch', 'a dash'), the 'quantity' MUST be 0.\n"
        "4. If no quantity is specified at all, the 'quantity' MUST be 0.\n"
        "5. 'unit' must be lowercase and singular. If no unit is given, infer the most appropriate one (e.g., 'piece' for an egg, 'clove' for garlic, 'teaspoon' for powders, like salt and pepper).\n\n"
        f"Input Text:\n---\n{processed_recipe.strip()}\n---\n\n"
        "Respond ONLY with the JSON array. Do not include explanations or any extra text."
    )
    return final_prompt

def extract_json_from_output(text):
    # Extract the JSON Array
    try:
        json_block = re.search(r"\[.*?\]", text, re.DOTALL).group()
        return json.loads(json_block)
    except Exception:
        return text  # fallback to raw output
    
def print_JSON(json_text):
    print("\nParsed JSON:\n", json.dumps(json_text, indent=2))