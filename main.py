import base64
import tkinter as tk
from tkinter import scrolledtext
import json
import threading
from llm import LLM, recipe_parser as rp
from recipe_analyzer import RecipeAnalyzer
from IngredientFinder import batch_substitution_report

class SousChefAI:
    """
    The main class for the Sous-Chef.ai application.
    """
    def __init__(self, root):
        """
        Initializes the SousChefAI application, sets up the GUI,
        and loads the necessary backend models.
        """
        self.root = root
        self.root.title("Sous-Chef.ai Nutrition Analyzer")
        self.root.geometry("550x480")

        self.BG_COLOR = "#5F8575"  # A muted green (same as presentation)
        self.FG_COLOR = "#FFFFFF"  # White text for contrast
        self.root.config(bg=self.BG_COLOR)

        # Initialize the LLM for parsing recipe text.
        self.llm = LLM.Gemma_2B_LLM()
        # Initialize the RecipeAnalyzer for fetching nutritional data.
        self.calculator = RecipeAnalyzer(api_key=<key>)
        
        # This will store the detailed nutritional data for the details popup.
        self.full_nutrition_data = None
        self.recipe_json = None
        # Build the user interface.
        self._create_widgets()

    def _create_widgets(self):
        """Creates and places all the Tkinter widgets in the window."""
        # Use a main frame to hold all widgets for better padding and organization.
        main_frame = tk.Frame(self.root, padx=15, pady=15, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Area ---
        input_label = tk.Label(main_frame, text="Enter Recipe Text:", font=("Helvetica", 12, "bold"), bg=self.BG_COLOR, fg=self.FG_COLOR)
        input_label.pack(anchor="w")
        # multi-line input with scrolled text
        self.input_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD, font=("Helvetica", 10))
        self.input_text.pack(fill=tk.X, pady=(5, 10))

        # --- Analyze Button ---
        self.analyze_button = tk.Button(main_frame, text="Analyze Recipe", font=("Helvetica", 12, "bold"), command=self.process_recipe)
        self.analyze_button.pack(pady=5)

        # --- Output Area ---
        # A separate frame for results helps to visually group the output.
        results_frame = tk.Frame(main_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, bg=self.BG_COLOR)
        results_frame.pack(fill=tk.X, pady=(15, 5))
        results_frame.columnconfigure(1, weight=1) # Allows the value column to expand.

        self.result_labels = {}
        fields = ["Calories", "Protein", "Fat", "Carbohydrates", "Estimated Price"]
        for i, field in enumerate(fields):
            # The field name label ("Calories:", for example).
            label = tk.Label(results_frame, text=f"{field}:", font=("Helvetica", 10, "bold"), bg=self.BG_COLOR, fg=self.FG_COLOR)
            label.grid(row=i, column=0, sticky="w", pady=2)
            
            # The corresponding value label
            value_label = tk.Label(results_frame, text="-", font=("Helvetica", 10), bg=self.BG_COLOR, fg=self.FG_COLOR)
            value_label.grid(row=i, column=1, sticky="w", pady=2)
            self.result_labels[field] = value_label

        # --- Details Button ---
        # This button is initially disabled and is enabled only after a successful analysis.
        self.details_button = tk.Button(main_frame, text="View Full Nutrition", state=tk.DISABLED, command=self.show_full_nutrition)
        self.details_button.pack(pady=10)
        self.substitutions_button = tk.Button(main_frame, text="View Substitutions", state=tk.DISABLED, command=self.show_substitutions)
        self.substitutions_button.pack(pady=10)

    def process_recipe(self):
        """
        Initiates the recipe analysis process in a background thread to keep the
        GUI responsive.
        """
        # Disable the button and update UI to indicate processing has started.
        self.analyze_button.config(state=tk.DISABLED, text="Analyzing...")
        self.details_button.config(state=tk.DISABLED)
        for label in self.result_labels.values():
            label.config(text="...")
            
        # Get the full text from the input widget.
        raw_input_text = self.input_text.get("1.0", tk.END)
        # Sanitize the input by removing Windows-style carriage returns ('\r')
        # and then stripping leading/trailing whitespace.
        sanitized_text = raw_input_text.replace('\r', '').strip()
        
        if not sanitized_text:
            self._update_summary_labels({"error": "Please enter a recipe."})
            self.analyze_button.config(state=tk.NORMAL, text="Analyze Recipe")
            return
            
        # Running the analysis in a separate thread to prevent the GUI from freezing during the potentially long-running network and LLM calls.
        threading.Thread(target=self.run_analysis_logic, args=(sanitized_text,)).start()
        
    def run_analysis_logic(self, raw_input_text):
        """
        Contains the core analysis logic that runs in the background thread.
        This method performs the LLM parsing and API calls.
        """
        try:
            # Step 1: Pre-process the input and run the LLM to parse ingredients.
            prompt = rp.pre_process_input(raw_input_text)
            response = self.llm.run(prompt)
            recipe_json = rp.extract_json_from_output(response)
            self.recipe_json = recipe_json
            # Step 2: Use the parsed JSON to get nutritional data.
            recipe_analysis = self.calculator.analyze_recipe(recipe_json)
        except Exception as e:
            # Catch any exceptions during the process to display an error.
            recipe_analysis = {"error": f"An error occurred: {e}"}
        
        # When the background task is complete, schedule the GUI update on the
        # main thread
        self.root.after(0, self._update_summary_labels, recipe_analysis)

    def _update_summary_labels(self, analysis_data):
        """
        Safely updates the main GUI labels with the analysis results. This method
        is always called on the main GUI thread.
        """
        # Re-enable the analyze button now that the process is complete.
        self.analyze_button.config(state=tk.NORMAL, text="Analyze Recipe")
        
        if "error" in analysis_data:
            # If an error occurred, display it and reset labels.
            for label in self.result_labels.values(): label.config(text="-")
            self.result_labels["Calories"].config(text=analysis_data["error"])
            return

        # Populate the labels with the retrieved data.
        summary = analysis_data.get("summary", {})
        self.result_labels["Calories"].config(text=f"{summary.get('Calories', '0')} kcal")
        self.result_labels["Protein"].config(text=f"{summary.get('Protein', '0')} g")
        self.result_labels["Fat"].config(text=f"{summary.get('Fat', '0')} g")
        self.result_labels["Carbohydrates"].config(text=f"{summary.get('Carbohydrates', '0')} g")
        self.result_labels["Estimated Price"].config(text=analysis_data.get("price", "$0.00"))
        
        # Store the full data and enable the details button.
        self.full_nutrition_data = analysis_data.get("full_data")
        if self.full_nutrition_data:
            self.details_button.config(state=tk.NORMAL)
        if self.recipe_json:
            self.substitutions_button.config(state=tk.NORMAL)

    def show_full_nutrition(self):
        """Opens a new Toplevel window to display all nutritional details."""
        if not self.full_nutrition_data:
            return

        # Create a new, separate window for the details.
        popup = tk.Toplevel(self.root)
        popup.title("Full Nutritional Details")
        popup.geometry("400x500")
        
        # Display the long list of nutrients using scrollable text box
        text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=("Courier New", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Format the JSON data
        formatted_text = json.dumps(self.full_nutrition_data, indent=2)
        text_area.insert(tk.END, formatted_text)
        # Disable editing of the text area
        text_area.config(state=tk.DISABLED)

    def show_substitutions(self):
        """Opens a new Toplevel window to display all nutritional details."""
        if not self.recipe_json:
            return

        # Create a new, separate window for the details.
        popup = tk.Toplevel(self.root)
        popup.title("Alternative Ingredients")
        popup.geometry("400x500")

        text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=("Courier New", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        formatted_text = batch_substitution_report(self.recipe_json)
        text_area.insert(tk.END, formatted_text)
        # Disable editing of the text area
        text_area.config(state=tk.DISABLED)

    def start(self):
        """Starts the Tkinter main event loop."""
        self.root.mainloop()

def main():
    """The main entry point for the application."""
    # Create the root Tkinter window.
    main_window = tk.Tk()
    # Create SousChefAI instance
    app = SousChefAI(main_window)
    # Start it
    app.start()

if __name__ == "__main__":
    main()
