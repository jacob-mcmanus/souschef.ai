import requests
from bs4 import BeautifulSoup
import networkx as nx
import time
from collections import deque
from urllib.parse import urljoin

BASE_URL = "http://www.foodsubs.com/"
SITEMAP_URL = urljoin(BASE_URL, "sitemap.html")
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Directed graph to preserve substitution direction
G = nx.DiGraph()

def get_all_page_links_from_sitemap():
    res = requests.get(SITEMAP_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/ingredients/" in href:
            full_url = urljoin(BASE_URL, href.strip())
            links.add(full_url)
    print(f"Found {len(links)} ingredient pages to scrape.")
    return sorted(list(links))

def process_page(url, scraped_pages, pages_to_scrape):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        main_ingredient = url.split("/")[-1].replace("-", " ").lower()
        G.add_node(main_ingredient, name=main_ingredient, allergens=[], nutrition={})

        for card in soup.select(".sortable-row.card"):
            sub_ingredients = []
            note = ""
            ratio = ""

            body = card.select_one(".card-body")
            if not body:
                continue
            rows = body.select(".row")

            for row in rows:
                sub_detail = row.select_one(".sub-details")
                if sub_detail:
                    ing_tag = sub_detail.select_one("a")
                    if ing_tag:
                        ing_name = ing_tag.get_text(strip=True).lower()
                        amount = sub_detail.get_text(strip=True).replace(ing_name, "").strip()
                        sub_ingredients.append((amount, ing_name))

                        # Get the full link to the ingredient and queue it
                        sub_url = ing_tag.get("href", "").strip()
                        full_url = urljoin(BASE_URL, sub_url)
                        if full_url not in scraped_pages and full_url not in pages_to_scrape:
                            pages_to_scrape.append(full_url)

                ratio_col = row.select_one(".col-md-3:nth-of-type(2)")
                if ratio_col and '=' in ratio_col.text:
                    ratio = ratio_col.text.strip()

            note_tag = card.select_one(".substitute-note-content")
            if note_tag:
                note = note_tag.get_text(strip=True)

            if len(sub_ingredients) == 1:
                amount, sub = sub_ingredients[0]
                if sub not in G:
                    G.add_node(sub, name=sub, allergens=[], nutrition={})
                full_ratio = f"{amount} = {ratio}" if ratio else amount
                G.add_edge(main_ingredient, sub, source=url, ratio=full_ratio, note=note)
                print(f"{main_ingredient} -> {sub} | ratio: {full_ratio} | note: {note}")

            elif len(sub_ingredients) > 1:
                combo_names = [ing for _, ing in sub_ingredients]
                combo_node = "+".join(combo_names)
                G.add_node(combo_node, name=combo_node, is_combo=True, allergens=[], nutrition={})

                full_ratio = ratio if ratio else ""
                G.add_edge(main_ingredient, combo_node, source=url, ratio=full_ratio, note=note)
                print(f"-> Added combo: {combo_node} <- {main_ingredient} | ratio: = {ratio} | note: {note}")

                for _, component in sub_ingredients:
                    if component not in G:
                        G.add_node(component, name=component, allergens=[], nutrition={})
                    G.add_edge(combo_node, component, relation="combo_component")

    except Exception as e:
        print(f"[!] Error processing {url}: {e}")

def main():
    global pages_to_scrape
    pages_to_scrape = deque(get_all_page_links_from_sitemap())
    scraped_pages = set()

    while pages_to_scrape:
        url = pages_to_scrape.popleft()
        if url in scraped_pages:
            continue

        print(f"[{len(scraped_pages)+1}] Scraping {url}")
        process_page(url, scraped_pages, pages_to_scrape)
        scraped_pages.add(url)
        time.sleep(0.25)  # Safe pause, reduce if needed

    print(f"\nGraph contains {len(G.nodes)} nodes and {len(G.edges)} edges.")
    nx.write_gml(G, "../../GraphTesting/ingredient_substitutions_enriched.gml")

if __name__ == "__main__":
    main()