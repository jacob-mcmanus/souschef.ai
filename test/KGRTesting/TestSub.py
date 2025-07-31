import random
from IngredientFinder import (
    match_ingredient,
    get_substitutions,
    pick_best_substitution,
    plural_fallback,
    G
)
import requests
SPOONACULAR_KEY = "API KEY"


ingredient_names = [n for n in G.nodes if not G.nodes[n].get("is_combo", False)]

user_inputs = [
    "chicken breast", "ground beef", "sour cream", "cream cheese", "greek yogurt", "almond milk", "whole milk",
    "cheddar cheese", "cottage cheese", "mozzarella", "parmesan", "ricotta", "goat cheese", "blue cheese", "brie",
    "feta", "butter", "unsalted butter", "margarine", "olive oil", "canola oil", "vegetable oil", "coconut oil",
    "ghee", "lard", "mayonnaise", "vegan mayo", "egg", "egg whites", "egg yolk", "hard boiled egg", "honey",
    "maple syrup", "molasses", "brown sugar", "white sugar", "powdered sugar", "corn syrup", "agave", "stevia",
    "banana", "apple", "pear", "mango", "papaya", "pineapple", "kiwi", "peach", "plum", "nectarine", "grape",
    "blueberry", "strawberry", "raspberry", "blackberry", "cranberry", "fig", "date", "raisin", "cherry",
    "lemon", "lime", "orange", "clementine", "grapefruit", "tomato", "cucumber", "lettuce", "romaine", "spinach",
    "kale", "chard", "cabbage", "carrot", "zucchini", "potato", "sweet potato", "yam", "broccoli", "cauliflower",
    "onion", "shallot", "garlic", "mushroom", "cremini", "portobello", "tofu", "tempeh", "seitan", "tvp",
    "beef broth", "chicken stock", "vegetable stock", "bone broth", "gelatin", "whipping cream", "evaporated milk",
    "condensed milk", "powdered milk", "ice cream", "yogurt", "soy yogurt", "almond yogurt", "coconut yogurt",
    "toast", "bread", "bagel", "croissant", "tortilla", "naan", "pita", "cracker", "roll", "bun", "muffin",
    "cupcake", "cake", "cookie", "brownie", "pastry", "granola", "protein bar", "energy bar", "oats", "cereal",
    "rice", "white rice", "brown rice", "quinoa", "couscous", "spaghetti", "penne", "macaroni", "lasagna", "ramen"
]

random.seed(42)
sample = random.sample(user_inputs, 100)
def test_spoonacular(user_inputs):
    successes = 0
    total_subs = 0
    failures = []

    for item in user_inputs:
        response = requests.get(
            "https://api.spoonacular.com/food/ingredients/substitutes",
            params={"ingredientName": item, "apiKey": SPOONACULAR_KEY}
        )
        if response.status_code != 200:
            failures.append(item)
            continue

        data = response.json()
        if data.get("status") == "failure" or not data.get("substitutes"):
            failures.append(item)
        else:
            subs = data["substitutes"]
            successes += 1
            total_subs += len(subs)

    total = len(user_inputs)
    percent = round((successes / total) * 100, 2)
    avg = round(total_subs / successes, 2) if successes else 0

    print("\n--- Spoonacular Results ---")
    print(f"Tested {total} user-style ingredient inputs.")
    print(f"{successes} returned a substitution.")
    print(f"Success rate: {percent}%")
    print(f"Average number of substitutions per successful input: {avg}")

    if failures:
        print("\nInputs with no match or substitution:")
        for f in failures:
            print(f" - {f}")


successes = 0
failures = []
total_subs = 0

for user_input in sample:
    matched = match_ingredient(user_input)
    substitutions = get_substitutions(matched, max_depth=1) if matched else []

    if not substitutions and matched:
        # Try plural/singular fallback of the match itself
        plural = plural_fallback(matched)
        if plural:
            fallback_subs = get_substitutions(plural, max_depth=1)
            if fallback_subs:
                matched = plural
                substitutions = fallback_subs

    if matched and substitutions:
        successes += 1
        total_subs += len(substitutions)
    else:
        failures.append(user_input)

total = len(sample)
percent = round((successes / total) * 100, 2)
avg_subs = round(total_subs / successes, 2) if successes > 0 else 0

print(f"Tested {total} user-style ingredient inputs.")
print(f"{successes} returned a substitution.")
print(f"Success rate: {percent}%")
print(f"Average number of substitutions per successful input: {avg_subs}")

if failures:
    print("\nInputs with no match or substitution:")
    for item in failures:
        print(f" - {item}")

test_spoonacular(sample)