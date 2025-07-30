import networkx as nx
import requests
from bs4 import BeautifulSoup
import re
import time

def slugify(name):
    # Lowercase, replace spaces and dots with dashes
    name = name.lower().replace(" ", "-").replace(".", "-").replace("---", "-")
    # Keep Unicode letters (including accents), numbers, and dashes
    return re.sub(r"[^\w\-]", "", name, flags=re.UNICODE)
def get_substitutions(ingredient):
    def fetch_soup(slug):
        url = f"https://foodsubs.com/ingredients/{slug}"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                return soup, url
            else:
                return None, url
        except Exception:
            return None, url

    tried_slugs = []
    base_slug = slugify(ingredient)
    tried_slugs.append(base_slug)

    soup, url = fetch_soup(base_slug)

    # Try singular fallback
    if not soup and base_slug.endswith('s'):
        singular_slug = base_slug[:-1]
        if singular_slug not in tried_slugs:
            soup, url = fetch_soup(singular_slug)
            tried_slugs.append(singular_slug)
            if soup:
                print(f"[Retrying with singular] Found substitutions at: {url}")

    # Try plural fallback
    if not soup:
        plural_slug = base_slug + 's'
        if plural_slug not in tried_slugs:
            soup, url = fetch_soup(plural_slug)
            tried_slugs.append(plural_slug)
            if soup:
                print(f"[Retrying with plural] Found substitutions at: {url}")

    if not soup:
        print(f"[404] Skipped {ingredient} ({url})")
        return []

    # Parse substitutions
    subs = []
    for tag in soup.find_all("li"):
        if "Substitute" in tag.text:
            text = tag.text.split("Substitute", 1)[-1].strip(": ")
            candidates = re.split(r",| or ", text)
            for c in candidates:
                clean = c.strip().split(" (")[0]
                if clean and clean.lower() != ingredient.lower():
                    subs.append(clean)
    return list(set(subs))
def update_gml_with_missing_nodes(gml_path, output_path):
    G = nx.read_gml(gml_path)

    if not isinstance(G, nx.DiGraph):
        G = G.to_directed()

    for node in G.nodes:
        if G.out_degree(node) == 0:
            print(f"Fetching substitutions for: {node}")
            subs = get_substitutions(node)
            for sub in subs:
                if sub not in G:
                    G.add_node(sub)
                G.add_edge(node, sub)
            time.sleep(.5)  # avoid hammering the server

    nx.write_gml(G, output_path)
    print(f"Updated GML written to {output_path}")

update_gml_with_missing_nodes("ingredient_substitutions_enriched.gml", "enhanced_graph.gml")