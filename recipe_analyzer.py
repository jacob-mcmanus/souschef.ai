import requests

class RecipeAnalyzer:
    """
    Calculates nutritional values and price for a recipe by fetching data from the
    Spoonacular API.
    """
    def __init__(self, api_key):
        """
        Initializes the RecipeAnalyzer with a Spoonacular API key.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")
        self.api_key = api_key
        self.base_url = "https://api.spoonacular.com/food/ingredients"
        self.session = requests.Session()

    def _get_ingredient_id(self, ingredient_name):
        """
        Searches for an ingredient by name to find its Spoonacular ID.
        """
        search_url = f"{self.base_url}/search"
        params = {"apiKey": self.api_key, "query": ingredient_name}
        
        # The response from this GET request will contain a list of possible
        # matches. We assume the first result is the most relevant.
        response = self.session.get(search_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        if data.get("results"):
            return data["results"][0]["id"]
        
        # If no results are found, inform the user and return None.
        print(f"Warning: Could not find an ID for ingredient: {ingredient_name}")
        return None

    def _get_ingredient_info(self, ingredient_id, amount, unit):
        """
        Retrieves detailed nutritional and cost info for a specific ingredient ID.
        """
        info_url = f"{self.base_url}/{ingredient_id}/information"
        params = {"apiKey": self.api_key, "amount": amount, "unit": unit}
        response = self.session.get(info_url, params=params)
        response.raise_for_status()
        return response.json()

    def analyze_recipe(self, llm_parsed_list):
        """
        Analyzes a full recipe for total nutrition and price by looking up each
        ingredient provided in a list of parsed ingredient dictionaries.
        """
        # Data structures to aggregate results across all ingredients.
        summary_nutrients = {"Calories": 0.0, "Protein": 0.0, "Fat": 0.0, "Carbohydrates": 0.0}
        all_nutrients = {}
        total_price_cents = 0

        print("--- Analyzing Recipe Nutrition & Price ---")
        for item in llm_parsed_list:
            # Skip items with no valid quantity, as they cannot be analyzed.
            if item.get('quantity', 0) <= 0:
                print(f"Skipping ingredient '{item.get('ingredient', 'unknown')}' due to zero or invalid quantity.")
                continue

            # Skip items with no valid unit, as they cannot be analyzed.
            if not item.get('unit'):
                print(f"Skipping ingredient '{item.get('ingredient', 'unknown')}' due to missing unit.")
                continue
            
            try:
                # Step 1: Get the unique ID for the ingredient.
                ingredient_id = self._get_ingredient_id(item['ingredient'])
                if not ingredient_id:
                    print(f"Skipping ingredient '{item.get('ingredient', 'unknown')}' unable to find ID.")
                    continue  # Skip if no ID was found.

                # Step 2: Use the ID to get detailed nutritional and cost data.
                info_data = self._get_ingredient_info(ingredient_id, item['quantity'], item['unit'])
                if not info_data:
                    print(f"Skipping ingredient '{item.get('ingredient', 'unknown')}' unable to find data.")
                    continue # Skip if no data found

                print(f"Successfully processed: {item['ingredient']}")
                
                # Accumulate the total cost. The API returns this value in cents.
                total_price_cents += info_data.get("estimatedCost", {}).get("value", 0)

                # Process and aggregate the nutritional data.
                if "nutrition" in info_data and "nutrients" in info_data["nutrition"]:
                    for nutrient in info_data["nutrition"]["nutrients"]:
                        name, amount, unit = nutrient.get("name"), nutrient.get("amount", 0), nutrient.get("unit", "")
                        
                        # Add to the high-level summary if it's a tracked nutrient.
                        if name in summary_nutrients:
                            summary_nutrients[name] += amount
                        
                        # Add to the comprehensive nutrient dictionary.
                        if name in all_nutrients:
                            all_nutrients[name]["amount"] += amount
                        else:
                            all_nutrients[name] = {"amount": amount, "unit": unit}
            
            except requests.exceptions.RequestException as e:
                # Handle network or API errors gracefully.
                print(f"Error processing '{item.get('ingredient', 'unknown item')}': {e}")
                continue
        
        print("--- Analysis Complete ---")
        
        # Format the final results
        formatted_summary = {name: f"{round(amount)}" for name, amount in summary_nutrients.items()}
        formatted_price = f"${total_price_cents / 100:.2f}"
        full_data_formatted = {
            name: f"{round(data['amount'], 2)} {data['unit']}" 
            for name, data in sorted(all_nutrients.items())
        }
        
        return {
            "summary": formatted_summary,
            "price": formatted_price,
            "full_data": full_data_formatted
        }