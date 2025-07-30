import networkx as nx

INPUT_GML = "ingredient_substitutions_enriched.gml"
OUTPUT_GML = "ingredient_allergens_vegan_tagged.gml"
OUTPUT_TXT = "ingredient_allergens_vegan_summary.txt"

# Allergen keyword mapping
ALLERGEN_KEYWORDS = {
    "gluten": [
        "wheat", "barley", "rye", "spelt", "semolina", "durum", "farina", "malt", "triticale",
        "bread", "bagel", "bun", "roll", "biscuit", "cracker", "pasta", "noodle", "flour", "couscous", "breadcrumbs",
        "toast", "cake", "pie", "pastry", "tortilla"
    ],
    "dairy": ["milk", "butter", "cheese", "cream", "ghee", "casein", "whey", "yogurt", "curds"],
    "egg": ["egg", "albumen", "mayonnaise", "aioli"],
    "soy": ["soy", "soya", "edamame", "miso", "tofu", "tempeh", "soybean"],
    "peanut": ["peanut", "groundnut", "goober"],
    "tree_nut": ["almond", "cashew", "walnut", "hazelnut", "pecan", "pistachio", "macadamia", "brazil nut"],
    "fish": ["anchovy", "bass", "catfish", "cod", "flounder", "grouper", "haddock", "hake", "halibut", "herring", "mackerel", "perch", "pollock", "salmon", "sardine", "snapper", "sole", "tilapia", "trout", "tuna"],
    "shellfish": ["shrimp", "prawn", "crab", "lobster", "clam", "mussel", "scallop", "oyster", "crawfish", "crayfish", "cockle"],
    "sesame": ["sesame", "tahini"],
    "mustard": ["mustard"],
    "celery": ["celery"],
    "sulfite": ["sulfite", "sulphite", "sulfur dioxide"],
    "lupin": ["lupin"]
}

# Non-vegan keyword triggers
NON_VEGAN_KEYWORDS = [
    "beef", "pork", "chicken", "turkey", "duck", "lamb", "veal",
    "egg", "milk", "butter", "cheese", "ghee", "cream", "yogurt", "casein", "whey",
    "fish", "anchovy", "tuna", "salmon", "cod", "trout",
    "shrimp", "crab", "lobster", "scallop", "clam", "oyster", "mussel",
    "honey", "gelatin", "lard", "broth", "animal fat", "bone", "suet"
]

def detect_allergens(name):
    name = name.lower()
    found = set()
    for allergen, keywords in ALLERGEN_KEYWORDS.items():
        if any(k in name for k in keywords):
            found.add(allergen)
    return sorted(found)

def is_vegan(name):
    name = name.lower()
    return not any(keyword in name for keyword in NON_VEGAN_KEYWORDS)

# Load the graph
G = nx.read_gml(INPUT_GML)

# Process each node
for node in G.nodes:
    name = G.nodes[node].get("name", node)
    G.nodes[node]["allergens"] = detect_allergens(name)
    G.nodes[node]["vegan"] = is_vegan(name)

# Save enriched graph
nx.write_gml(G, OUTPUT_GML)
print(f"Saved allergen+vegan-tagged graph to {OUTPUT_GML}")

# Save summary text
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write("Ingredient Allergen and Vegan Summary:\n\n")
    for node in G.nodes:
        name = G.nodes[node].get("name", node)
        allergens = G.nodes[node].get("allergens", [])
        vegan = G.nodes[node].get("vegan", True)
        f.write(f"{name}: Vegan={vegan}, Allergens={', '.join(allergens) if allergens else 'None'}\n")

print(f"Saved allergen+vegan summary to {OUTPUT_TXT}")