from llm import LLM, recipe_parser as rp
import json

def main():
    
    #llm = LLM.Mistral_LLM()
    llm = LLM.Gemma_LLM()
    
    # Get user recipe here
    with open("recipe.txt", "r", encoding="utf-8") as f:
        raw_input_text = f.read()

    # Pre process user input
    #raw_input_text = input("Paste recipe ingredients:\n")
    prompt = rp.pre_process_input(raw_input_text)

    response = llm.run(prompt)

    parsed_json = rp.extract_json_from_output(response)
    
    rp.print_JSON(parsed_json)

if __name__ == "__main__":
    main()
