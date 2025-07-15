from llm import LLM, recipe_parser as rp
from nutrition import db

def main():
    # Initiate LLM
    llm = LLM.Gemma_2B_LLM()
    
    # Get user recipe here
    with open("recipe.txt", "r", encoding="utf-8") as f:
        raw_input_text = f.read()

    # Pre process user input
    prompt = rp.pre_process_input(raw_input_text)

    # Get response from LLM
    response = llm.run(prompt)

    # Extract json from LLM
    recipe_json = rp.extract_json_from_output(response)
    
    rp.print_JSON(recipe_json)

if __name__ == "__main__":
    main()
