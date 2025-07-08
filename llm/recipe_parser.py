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
    prompt = """
    Extract the following ingredient list into structured JSON. For each ingredient, extract:

    - ingredient: name (normalized)
    - quantity: in decimal format
    - unit: cups, teaspoons, etc.

    Input:
    """
    recipe = unicode_fraction_to_float(recipe)
    return prompt + recipe.strip() + "\n\nOutput:\n"

def extract_json_from_output(text):
    # Try to isolate the first JSON block
    try:
        json_block = re.search(r"\[.*?\]", text, re.DOTALL).group()
        return json.loads(json_block)
    except Exception:
        return text  # fallback to raw output
    
def print_JSON(json_text):
    print("\nParsed JSON:\n", json.dumps(json_text, indent=2))