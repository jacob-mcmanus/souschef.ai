import requests
import json
import networkx as nx
import re
import time
from fuzzywuzzy import fuzz

API_KEY = "API KEY"
INPUT_GML = "enhanced_graph.gml"
OUTPUT_GML = "ingredient_substitutions_enriched.gml"
OUTPUT_TXT = "ingredient_substitutions_enriched.txt"

# Nutrients to extract
NUTRIENT_IDS = {
    1257: "trans_fat",
    1293: "polyunsat_fat",
    1292: "monounsat_fat",
    1258: "sat_fat",
    1253: "cholesterol",
    1093: "sodium",
    1005: "carbs",
    1079: "fiber",
    2000: "sugars",
    1003: "protein",
    1104: "vit_a",
    1162: "vit_c",
    1087: "calcium",
    1089: "iron",
    1008: "calories"
}

# Load the graph
G = nx.read_gml(INPUT_GML)

# Cache for USDA results
usda_cache = {}


def search_usda(ingredient):
    if ingredient in usda_cache:
        return usda_cache[ingredient]

    url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"generalSearchInput": ingredient}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        parsed = response.json()
        best_id, best_score = None, 0
        for item in parsed.get("foods", []):
            score = fuzz.token_set_ratio(ingredient, item.get("description", ""))
            if score > best_score:
                best_score = score
                best_id = item.get("fdcId")
        usda_cache[ingredient] = best_id
        return best_id
    except Exception as e:
        print(f"[!] USDA search failed for '{ingredient}': {e}")
        return None


def fetch_nutrients(fdc_id):
    url = f"https://api.nal.usda.gov/fdc/v1/{fdc_id}?api_key={API_KEY}"
    try:
        response = requests.get(url)
        parsed = response.json()
        result = {v: 0 for v in NUTRIENT_IDS.values()}
        for item in parsed.get("foodNutrients", []):
            nid = item.get("nutrient", {}).get("id")
            if nid in NUTRIENT_IDS:
                result[NUTRIENT_IDS[nid]] = item.get("amount", 0)
        return result
    except Exception as e:
        print(f"[!] Nutrient fetch failed for FDC ID {fdc_id}: {e}")
        return {v: 0 for v in NUTRIENT_IDS.values()}


def enrich_single(name):
    if name in usda_cache and usda_cache[name] is None:
        return None

    fdc_id = search_usda(name)
    if not fdc_id:
        return None

    return fetch_nutrients(fdc_id)


def combine_nutrients(nutrient_dicts):
    if not nutrient_dicts:
        return {v: 0 for v in NUTRIENT_IDS.values()}
    total = {k: 0 for k in NUTRIENT_IDS.values()}
    for nd in nutrient_dicts:
        for k, v in nd.items():
            total[k] += v
    return {k: round(v / len(nutrient_dicts), 2) for k, v in total.items()}


# Enrich all nodes
for node in G.nodes:
    name = G.nodes[node].get("name", node).lower()
    print(f"{name}")

    # Handle compound ingredients
    if '+' in name:
        components = name.split('+')
        nutrients_list = []
        for comp in components:
            nd = enrich_single(comp.strip())
            if nd:
                nutrients_list.append(nd)
        nutrition = combine_nutrients(nutrients_list)
    else:
        nutrition = enrich_single(name)
        if not nutrition:
            print(f"No data found for {name}")
            continue

    allergens = []
    if any(term in name for term in ["wheat", "barley", "farina"]):
        allergens.append("gluten")

    G.nodes[node]["nutrition"] = nutrition
    G.nodes[node]["allergens"] = allergens

    print(f"{name}: {len(nutrition)} nutrients")
    time.sleep(0.3)

# Save enriched files
nx.write_gml(G, OUTPUT_GML)
print(f"Saved enriched graph to {OUTPUT_GML}")

with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write(f"Ingredient Substitution Graph: {len(G.nodes)} ingredients, {len(G.edges)} edges\n\n")
    for u, v, data in G.edges(data=True):
        f.write(f"{u} ↔ {v}")
        if 'ratio' in data:
            f.write(f" [ratio: {data['ratio']}]")
        if 'note' in data:
            f.write(f" - {data['note']}")
        f.write("\n")

print(f"Saved enriched text file to {OUTPUT_TXT}")