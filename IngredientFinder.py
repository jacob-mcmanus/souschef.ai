import networkx as nx
from rapidfuzz import process, fuzz
import ast
import inflect
import json


p = inflect.engine()

def safe_eval(s):
    try:
        return ast.literal_eval(s)
    except Exception:
        return s

G = nx.read_gml("ingredient_allergens_vegan_tagged.gml", destringizer=safe_eval)
ingredient_names = set(G.nodes)

def normalize_input(s):
    return s.replace(",", "").strip().lower()

def best_match(query, choices, threshold=80):
    result = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    if result and result[1] >= threshold:
        return result[0]
    return None

def plural_fallback(name):
    alt = p.plural(name) if not p.singular_noun(name) else p.singular_noun(name)
    return alt if alt and alt in ingredient_names else None

def substring_fallback(name):
    matches = [n for n in ingredient_names if name in n]
    return min(matches, key=len) if matches else None

def match_ingredient(user_input):
    base = normalize_input(user_input)

    match = best_match(base, ingredient_names)
    if match:
        return match

    plural = plural_fallback(base)
    if plural:
        return plural

    match = substring_fallback(base)
    if match:
        return match

    plural = p.plural(base) if not p.singular_noun(base) else p.singular_noun(base)
    if plural:
        match = substring_fallback(plural)
        if match:
            return match

    words = base.split()
    if len(words) > 1:
        last_word = words[-1]
        return match_ingredient(last_word)

    return None
def get_substitutions(ingredient, max_depth=1):
    if ingredient not in G:
        return []
    reachable = nx.single_source_shortest_path_length(G, ingredient, cutoff=max_depth)
    return sorted(set(reachable.keys()) - {ingredient})

def nutrition_score(nutrition):
    if not nutrition or not isinstance(nutrition, dict):
        return 0, 0, 0  # ratio, micro_total, calories
    protein = nutrition.get("protein", 0)
    calories = nutrition.get("calories", 0)
    if calories <= 0:
        return 0, 0, calories
    ratio = protein / calories
    micronutrients = ["vit_a", "vit_c", "iron", "calcium", "fiber"]
    micro_total = sum(nutrition.get(n, 0) for n in micronutrients)
    return round(ratio, 3), round(micro_total, 2), round(calories, 1)


def pick_best_substitution(original, candidates):
    best = None
    best_score = -1
    best_reason = ""
    best_note = ""
    best_ratio = ""
    orig_data = G.nodes[original]
    orig_nutrition = orig_data.get("nutrition", {})
    orig_allergens = orig_data.get("allergens", [])
    orig_ratio, orig_micro, orig_cal = nutrition_score(orig_nutrition)

    for sub in candidates:
        sub_data = G.nodes.get(sub, {})
        if sub_data.get("is_combo", False):
            continue
        sub_nutrition = sub_data.get("nutrition", {})
        sub_allergens = sub_data.get("allergens", [])
        ratio, micro, cal = nutrition_score(sub_nutrition)
        reason = ""
        score = 0

        if orig_allergens and not sub_allergens:
            score += 7
            reason = "allergen-free alternative"

        if ratio > orig_ratio + 0.05:
            score += 5
            reason = "better protein/calorie ratio"

        if micro > orig_micro + 5:
            score += 2
            reason = "better micronutrient profile"

        if cal < orig_cal * 0.5:
            score += 3
            reason = "lower calorie alternative"

        if original in sub or any(word in sub for word in original.split()):
            score += 1

        if score > best_score:
            best = sub
            best_score = score
            best_reason = reason
            edge_data = G.get_edge_data(original, sub, default={})
            best_note = edge_data.get("note", "")
            best_ratio = edge_data.get("ratio", "")

    if best:
        return best, best_reason, best_note, best_ratio

    for sub in candidates:
        if G.nodes[sub].get("is_combo", False):
            edge_data = G.get_edge_data(original, sub, default={})
            return sub, "default (combo substitution)", edge_data.get("note", ""), edge_data.get("ratio", "")

    if candidates:
        fallback = candidates[0]
        edge_data = G.get_edge_data(original, fallback, default={})
        return fallback, "default (first substitution)", edge_data.get("note", ""), edge_data.get("ratio", "")

    return None, "", "", ""
def batch_substitution_report(json_inout):
    inputs = extract_ingredients(json_inout)
    output_lines = []
    for original_input in inputs:
        matched = match_ingredient(original_input)
        if not matched:
            output_lines.append(f"{original_input} -> No close match found")
            continue

        substitutions = get_substitutions(matched, max_depth=1)
        if not substitutions:
            plural = plural_fallback(matched)
            if plural:
                substitutions = get_substitutions(plural, max_depth=1)

        if not substitutions:
            output_lines.append(f"{original_input} -> No substitutions found")
            continue

        best, reason, note, ratio = pick_best_substitution(matched, substitutions)
        if best:
            output_lines.append(f"{original_input} -> {best}")
            if ratio:
                output_lines.append(f"  Ratio: {ratio}")
            if note:
                output_lines.append(f"  Note: {note}")
        else:
            output_lines.append(f"{original_input} -> Substitutions found but no best match")
    return "\n".join(output_lines)

def extract_ingredients(json_string):
    try:
        data = json.loads(json_string)
        return [item["ingredient"] for item in data if "ingredient" in item]
    except json.JSONDecodeError:
        print("Invalid JSON input.")
        return []

def main():
    json_input = '''
    [
        {
            "ingredient": "butter",
            "quantity": "1",
            "unit": "cup"
        },
        {
            "ingredient": "sugar",
            "quantity": "0.75",
            "unit": "cup"
        }
    ]
    '''
    print(batch_substitution_report(json_input))

if __name__ == "__main__":
    main()