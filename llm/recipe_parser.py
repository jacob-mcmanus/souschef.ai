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
    prompt_template = f"""
    You are an expert recipe parser. Your task is to extract ingredients from the provided text into a structured JSON array.

    ### Rules
    1.  **ingredient**: Use the lowercase, singular form of the ingredient name. (e.g., "2 large eggs" becomes "egg").
    2.  **quantity**: Provide the numeric quantity as a decimal. If there is no quantity available for the specific ingredient (e.g., "Pepper to taste"), set the quantity as 0.
    3.  **unit**: Use the lowercase, singular form of the unit (e.g., "cups" becomes "cup"). If there is no unit available for the specific ingredient (e.g., "Pepper to taste"), the value must be `null`.


    ### Example
    **Example Input Text:**
        2 large eggs
        1/2 cup all-purpose flour
        1 Teaspoon of Salt
        Pepper to Taste

    **Example Output JSON:**
        ```json
        [
        {{
            "ingredient": "egg",
            "quantity": 2,
            "unit": "large"
        }},
        {{
            "ingredient": "all-purpose flour",
            "quantity": 0.5,
            "unit": "cup"
        }},
        {{
            "ingredient": "salt",
            "quantity": 1,
            "unit": "teaspoon"
        }},
        {{
            "ingredient": "pepper",
            "quantity": 0,
            "unit": "null"
        }}
        ]
        ```
    """

    processed_recipe = unicode_fraction_to_float(recipe)
    
    final_prompt = (
        prompt_template +
        "\n### Recipe to Parse\n" +
        f"**Input Text:**\n{processed_recipe.strip()}\n\n" +
        "(Respond ONLY with the JSON array. No explanation, no markdown, no extra text. Remember to convert all fractions into the corresponding decimal values.) Output:\n"
    )

    return final_prompt

def extract_json_from_output(text):
    # Find the position of "Output:"
    output_idx = text.find("Output:")
    if output_idx != -1:
        text = text[output_idx + len("Output:") :]
    # Now extract the first JSON array after Output:
    try:
        json_block = re.search(r"\[.*?\]", text, re.DOTALL).group()
        return json.loads(json_block)
    except Exception:
        return text  # fallback to raw output
    
def print_JSON(json_text):
    print("\nParsed JSON:\n", json.dumps(json_text, indent=2))