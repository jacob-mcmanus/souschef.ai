from llm import LLM, recipe_parser as rp
from recipe_analyzer import *
from IngredientFinder import batch_substitution_report

def main():
    # Initiate LLM
    llm = LLM.Gemma_2B_LLM()
    
    # Load Analyzer
    api_key = None
    with open('api_key.txt', 'r') as file: 
        api_key = file.read()
    analyzer = RecipeAnalyzer(api_key)
    
    # Get user recipe here [would be from user input in full model]
    with open("recipe.txt", "r", encoding="utf-8") as f:
        raw_input_text = f.read()

    # Pre process user input
    prompt = rp.pre_process_input(raw_input_text)

    # Get response from LLM
    response = llm.run(prompt)

    # Extract json from LLM
    recipe_json = rp.extract_json_from_output(response)
    
    # Print JSON for Debugging Purposes
    rp.print_JSON(recipe_json)
    
    # Run Analyzer and print values
    values = analyzer.analyze_recipe(recipe_json)
    
    print(values)
    print("")

    #print substitutions
    print(batch_substitution_report(recipe_json))
            
if __name__ == "__main__":
    main()
