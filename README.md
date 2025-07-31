# Sous-Chef.ai

**An LLM-powered nutritional analyzer and ingredient substitution tool for recipes.**

Sous-Chef.ai is a desktop application that takes any recipe text, intelligently parses the ingredients using a local Large Language Model (LLM), and provides a detailed nutritional analysis, estimated cost, and smart ingredient substitutions.

## Features

-   **Intelligent Recipe Parsing**: Paste any recipe, and a local LLM (like Gemma or Llama) will extract the ingredients, quantities, and units into a structured format.
-   **Comprehensive Nutritional Analysis**: Get a summary of key macronutrients (Calories, Protein, Fat, Carbs) and a detailed breakdown of over 20 vitamins and minerals.
-   **Price Estimation**: Calculates the estimated cost of all ingredients for the recipe.
-   **Smart Ingredient Substitutions**: Find alternatives for any ingredient. The system can suggest healthier, lower-calorie, or allergen-free options based on a comprehensive food substitution graph.
-   **Responsive UI**: A simple and clean user interface built with Tkinter.
-   **Extensible & Modular**: Easily swap out LLMs or update the substitution data.

## How It Works

1.  **Input**: The user pastes raw recipe text into the UI. NOTE: Make sure to remove any unknown characters. Unfortunately, we have ran into issues when pasting multiple lines.
2.  **LLM Parsing**: The text is sent to a local LLM, which has been prompted to act as an expert recipe parser. It returns a structured JSON list of ingredients.
3.  **Nutritional & Price Analysis**: The structured list is processed by the `RecipeAnalyzer`, which queries the Spoonacular API for each ingredient to fetch detailed nutritional data and cost information.
4.  **Substitution Engine**: The `IngredientFinder` uses a pre-built NetworkX graph of food relationships to find and rank potential substitutions for ingredients in the original recipe.
5.  **Display**: The results are displayed back to the user in a clear, easy-to-read format, with options to view detailed reports.

## Project Structure
```
.
├── main.py                   # Main Tkinter GUI application
├── recipe_analyzer.py        # Handles Spoonacular API calls for nutrition/price
├── IngredientFinder.py       # Finds ingredient substitutions using the graph
├── llm/
│   ├── LLM.py                # Wrapper classes for different LLMs
│   └── recipe_parser.py      # Pre-processes text and parses LLM output
├── ingredient_allergens_vegan_tagged.gml # Data for the substitution graph
├── api_key.txt               # Stores your Spoonacular API key
├── test_LLMs.py              # Script to evaluate LLM parsing performance
├── test_values.py            # Script to evaluate end-to-end analysis accuracy
└── ...
```

## Setup and Installation

### Prerequisites

-   Python 3.8+
-   A CUDA-enabled GPU is needed running the local LLMs

### Install Dependencies

This project has several dependencies. You can create a `requirements.txt` file with the content below and install them all at once.

**`requirements.txt`:**
```txt
requests
networkx
rapidfuzz
inflect
torch
transformers
matplotlib
numpy
beautifulsoup4
```

**Installation command:**
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key

The application uses the Spoonacular API for nutritional data.

1.  Get a free API key from the Spoonacular API website.
2.  Create a file named `api_key.txt` in the root of the project directory.
3.  Paste your API key into this file and save it.
NOTE: There is a 150 token a day limit. Each ingredient uses 4 tokens.

### 5. Download the Graph Data

The ingredient substitution feature relies on a pre-built graph file. Make sure `ingredient_allergens_vegan_tagged.gml` is present in the root directory of the project.

## Usage

To run the main application, execute the `main.py` script:

```bash
python main.py
```

1.  Paste your recipe text into the input box.
2.  Click the "Analyze Recipe" button.
3.  View the summary of nutrition and price.
4.  Click "View Full Nutrition" or "View Substitutions" for more detailed information in a new window.

## For Developers: Running Evaluations

The repository includes scripts to test the performance of the system:

-   **Evaluate LLM Parsing**: `test_LLMs.py` runs a set of test recipes through different LLMs and calculates F1 scores, accuracy, and inference time for ingredient parsing.
-   **Evaluate Nutritional Accuracy**: `test_values.py` evaluates the end-to-end accuracy of the system by comparing the final nutritional values against a ground-truth dataset.
-   **Evaluate Knowledge Graph Efficacy**: `TestSub.py` evaluates the efficacy of the graph search for finding ingredient substitutions against the Spoonacular API alternative.