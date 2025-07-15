import os
import json

# This list contains all 50 recipes and their corresponding JSON data,
# updated to treat size adjectives as units.
recipes_data = [
    {
        "name": "Classic Pancakes",
        "recipe_text": """2 cups all-purpose flour
2 tablespoons sugar
1 tablespoon baking powder
1/2 teaspoon salt
2 large eggs
1 3/4 cups milk
1/4 cup unsalted butter, melted""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "cups"},
            {"ingredient": "sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "baking powder", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "milk", "quantity": 1.75, "unit": "cups"},
            {"ingredient": "unsalted butter", "quantity": 0.25, "unit": "cup"}
        ]
    },
    {
        "name": "Simple Tomato Soup",
        "recipe_text": """1 tablespoon olive oil
1 medium onion, chopped
2 cloves garlic, minced
1 (28 ounce) can crushed tomatoes
2 cups vegetable broth
1 teaspoon dried basil
1/2 cup heavy cream
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "olive oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "medium"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "crushed tomatoes", "quantity": 28, "unit": "ounce"},
            {"ingredient": "vegetable broth", "quantity": 2, "unit": "cups"},
            {"ingredient": "dried basil", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "heavy cream", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Guacamole",
        "recipe_text": """3 ripe avocados
1/2 small onion, finely chopped
1-2 serrano chiles, stems and seeds removed, minced
2 tablespoons cilantro, finely chopped
1 tablespoon fresh lime juice
1/2 teaspoon kosher salt
Pinch of ground cumin""",
        "json_data": [
            {"ingredient": "ripe avocado", "quantity": 3, "unit": None},
            {"ingredient": "onion", "quantity": 0.5, "unit": "small"},
            {"ingredient": "serrano chile", "quantity": 2, "unit": None},
            {"ingredient": "cilantro", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "fresh lime juice", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "kosher salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "ground cumin", "quantity": 1, "unit": "pinch"}
        ]
    },
    {
        "name": "Chocolate Chip Cookies",
        "recipe_text": """1 cup (2 sticks) unsalted butter, softened
3/4 cup granulated sugar
3/4 cup packed brown sugar
2 large eggs
1 teaspoon vanilla extract
2 1/4 cups all-purpose flour
1 teaspoon baking soda
1/2 teaspoon salt
2 cups semisweet chocolate chips""",
        "json_data": [
            {"ingredient": "unsalted butter", "quantity": 1, "unit": "cup"},
            {"ingredient": "granulated sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "packed brown sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "vanilla extract", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "all-purpose flour", "quantity": 2.25, "unit": "cups"},
            {"ingredient": "baking soda", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "semisweet chocolate chips", "quantity": 2, "unit": "cups"}
        ]
    },
    {
        "name": "Baked Salmon",
        "recipe_text": """1 (2 pound) salmon fillet
2 tablespoons olive oil
2 cloves garlic, minced
1 teaspoon dried herbs (such as dill or parsley)
Salt and freshly ground black pepper to taste
1 lemon, sliced""",
        "json_data": [
            {"ingredient": "salmon fillet", "quantity": 2, "unit": "pound"},
            {"ingredient": "olive oil", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "dried herbs", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"},
            {"ingredient": "lemon", "quantity": 1, "unit": None}
        ]
    },
    {
        "name": "Chicken Alfredo",
        "recipe_text": """1 pound fettuccine
1 pound boneless, skinless chicken breasts, cut into bite-sized pieces
2 tablespoons butter
2 cloves garlic, minced
1 1/2 cups heavy cream
1 1/2 cups grated Parmesan cheese
Salt and black pepper to taste
2 tablespoons chopped fresh parsley""",
        "json_data": [
            {"ingredient": "fettuccine", "quantity": 1, "unit": "pound"},
            {"ingredient": "boneless, skinless chicken breast", "quantity": 1, "unit": "pound"},
            {"ingredient": "butter", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "heavy cream", "quantity": 1.5, "unit": "cups"},
            {"ingredient": "grated parmesan cheese", "quantity": 1.5, "unit": "cups"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "black pepper", "quantity": None, "unit": "to taste"},
            {"ingredient": "chopped fresh parsley", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Beef Chili",
        "recipe_text": """1 tablespoon vegetable oil
1 large onion, chopped
2 pounds ground beef
3 cloves garlic, minced
2 tablespoons chili powder
1 tablespoon ground cumin
1 (28 ounce) can diced tomatoes, undrained
1 (15 ounce) can kidney beans, rinsed and drained
1 (15 ounce) can black beans, rinsed and drained
1 cup beef broth""",
        "json_data": [
            {"ingredient": "vegetable oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "large"},
            {"ingredient": "ground beef", "quantity": 2, "unit": "pounds"},
            {"ingredient": "garlic", "quantity": 3, "unit": "cloves"},
            {"ingredient": "chili powder", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "ground cumin", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "diced tomatoes", "quantity": 28, "unit": "ounce"},
            {"ingredient": "kidney beans", "quantity": 15, "unit": "ounce"},
            {"ingredient": "black beans", "quantity": 15, "unit": "ounce"},
            {"ingredient": "beef broth", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Classic Margarita",
        "recipe_text": """2 ounces blanco tequila
1 ounce lime juice, freshly squeezed
1/2 ounce orange liqueur
1/2 ounce agave syrup
Garnish: lime wheel
Garnish: kosher salt""",
        "json_data": [
            {"ingredient": "blanco tequila", "quantity": 2, "unit": "ounces"},
            {"ingredient": "lime juice", "quantity": 1, "unit": "ounce"},
            {"ingredient": "orange liqueur", "quantity": 0.5, "unit": "ounce"},
            {"ingredient": "agave syrup", "quantity": 0.5, "unit": "ounce"},
            {"ingredient": "lime wheel", "quantity": 1, "unit": "garnish"},
            {"ingredient": "kosher salt", "quantity": 1, "unit": "garnish"}
        ]
    },
    {
        "name": "Caesar Salad",
        "recipe_text": """1 large head of romaine lettuce, chopped
1 cup croutons
1/4 cup grated Parmesan cheese
For the dressing:
2 anchovy fillets, minced
2 cloves garlic, minced
1 egg yolk
1 tablespoon Dijon mustard
2 tablespoons fresh lemon juice
1/4 cup olive oil
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "romaine lettuce", "quantity": 1, "unit": "large head"},
            {"ingredient": "croutons", "quantity": 1, "unit": "cup"},
            {"ingredient": "grated parmesan cheese", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "anchovy fillet", "quantity": 2, "unit": None},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "egg yolk", "quantity": 1, "unit": None},
            {"ingredient": "dijon mustard", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "fresh lemon juice", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "olive oil", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Banana Bread",
        "recipe_text": """2 cups all-purpose flour
1 teaspoon baking soda
1/4 teaspoon salt
1/2 cup butter
3/4 cup brown sugar
2 eggs, beaten
2 1/3 cups mashed overripe bananas""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "cups"},
            {"ingredient": "baking soda", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "butter", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "brown sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "egg", "quantity": 2, "unit": None},
            {"ingredient": "mashed overripe banana", "quantity": 2.33, "unit": "cups"}
        ]
    },
    {
        "name": "Scrambled Eggs",
        "recipe_text": """4 large eggs
1/4 cup milk
2 tablespoons unsalted butter
Salt and freshly ground black pepper to taste""",
        "json_data": [
            {"ingredient": "egg", "quantity": 4, "unit": "large"},
            {"ingredient": "milk", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "unsalted butter", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Oatmeal",
        "recipe_text": """1/2 cup rolled oats
1 cup water or milk
1 pinch of salt
Optional toppings: brown sugar, maple syrup, fruits, nuts""",
        "json_data": [
            {"ingredient": "rolled oats", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "water or milk", "quantity": 1, "unit": "cup"},
            {"ingredient": "salt", "quantity": 1, "unit": "pinch"}
        ]
    },
    {
        "name": "French Toast",
        "recipe_text": """4 slices of bread
2 large eggs
1/2 cup milk
1 tablespoon granulated sugar
1 teaspoon vanilla extract
1/4 teaspoon ground cinnamon
2 tablespoons butter for frying""",
        "json_data": [
            {"ingredient": "bread", "quantity": 4, "unit": "slices"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "milk", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "granulated sugar", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "vanilla extract", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "ground cinnamon", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "butter", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Grilled Cheese Sandwich",
        "recipe_text": """2 slices of bread
2 slices of cheddar cheese
2 tablespoons butter, softened""",
        "json_data": [
            {"ingredient": "bread", "quantity": 2, "unit": "slices"},
            {"ingredient": "cheddar cheese", "quantity": 2, "unit": "slices"},
            {"ingredient": "butter", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Caprese Salad",
        "recipe_text": """2 large ripe tomatoes, sliced
8 ounces fresh mozzarella cheese, sliced
1/4 cup fresh basil leaves
2 tablespoons extra virgin olive oil
1 tablespoon balsamic glaze
Salt and freshly ground black pepper to taste""",
        "json_data": [
            {"ingredient": "ripe tomato", "quantity": 2, "unit": "large"},
            {"ingredient": "fresh mozzarella cheese", "quantity": 8, "unit": "ounces"},
            {"ingredient": "fresh basil leaves", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "extra virgin olive oil", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "balsamic glaze", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Spaghetti Carbonara",
        "recipe_text": """1 pound spaghetti
4 large egg yolks
1/2 cup grated Pecorino Romano cheese, plus more for serving
1/4 cup grated Parmesan cheese
4 ounces pancetta or guanciale, diced
2 cloves garlic, minced
Freshly ground black pepper""",
        "json_data": [
            {"ingredient": "spaghetti", "quantity": 1, "unit": "pound"},
            {"ingredient": "egg yolk", "quantity": 4, "unit": "large"},
            {"ingredient": "grated pecorino romano cheese", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "grated parmesan cheese", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "pancetta or guanciale", "quantity": 4, "unit": "ounces"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Chicken Noodle Soup",
        "recipe_text": """1 tablespoon olive oil
1 medium onion, chopped
2 carrots, chopped
2 celery stalks, chopped
2 cloves garlic, minced
8 cups chicken broth
1 pound boneless, skinless chicken breasts
4 ounces egg noodles
1/4 cup chopped fresh parsley
Salt and black pepper to taste""",
        "json_data": [
            {"ingredient": "olive oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "medium"},
            {"ingredient": "carrot", "quantity": 2, "unit": None},
            {"ingredient": "celery stalk", "quantity": 2, "unit": None},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "chicken broth", "quantity": 8, "unit": "cups"},
            {"ingredient": "boneless, skinless chicken breast", "quantity": 1, "unit": "pound"},
            {"ingredient": "egg noodles", "quantity": 4, "unit": "ounces"},
            {"ingredient": "chopped fresh parsley", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Mashed Potatoes",
        "recipe_text": """2 pounds russet potatoes, peeled and quartered
1/2 cup milk or cream
1/4 cup unsalted butter
Salt and freshly ground black pepper to taste""",
        "json_data": [
            {"ingredient": "russet potato", "quantity": 2, "unit": "pounds"},
            {"ingredient": "milk or cream", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "unsalted butter", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Brownies",
        "recipe_text": """1/2 cup unsalted butter, melted
1 cup granulated sugar
2 large eggs
1 teaspoon vanilla extract
1/3 cup unsweetened cocoa powder
1/2 cup all-purpose flour
1/4 teaspoon salt
1/4 teaspoon baking powder""",
        "json_data": [
            {"ingredient": "unsalted butter", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "granulated sugar", "quantity": 1, "unit": "cup"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "vanilla extract", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "unsweetened cocoa powder", "quantity": 0.33, "unit": "cup"},
            {"ingredient": "all-purpose flour", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "salt", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "baking powder", "quantity": 0.25, "unit": "teaspoon"}
        ]
    },
    {
        "name": "Apple Pie",
        "recipe_text": """1 recipe for a double-crust pie
6 cups thinly sliced, peeled apples (about 2 pounds)
3/4 cup granulated sugar
2 tablespoons all-purpose flour
1 teaspoon ground cinnamon
1/4 teaspoon ground nutmeg
1 tablespoon lemon juice
2 tablespoons unsalted butter""",
        "json_data": [
            {"ingredient": "double-crust pie", "quantity": 1, "unit": "recipe"},
            {"ingredient": "thinly sliced, peeled apple", "quantity": 6, "unit": "cups"},
            {"ingredient": "granulated sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "ground cinnamon", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "ground nutmeg", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "lemon juice", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "unsalted butter", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Pulled Pork",
        "recipe_text": """4 pound pork shoulder
2 tablespoons brown sugar
1 tablespoon paprika
2 teaspoons salt
1 teaspoon black pepper
1 cup barbecue sauce""",
        "json_data": [
            {"ingredient": "pork shoulder", "quantity": 4, "unit": "pound"},
            {"ingredient": "brown sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "paprika", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": 2, "unit": "teaspoons"},
            {"ingredient": "black pepper", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "barbecue sauce", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Coleslaw",
        "recipe_text": """1/2 cup mayonnaise
2 tablespoons apple cider vinegar
1 tablespoon sugar
1/2 teaspoon salt
1/4 teaspoon black pepper
4 cups shredded cabbage
1 cup shredded carrots""",
        "json_data": [
            {"ingredient": "mayonnaise", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "apple cider vinegar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "sugar", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "black pepper", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "shredded cabbage", "quantity": 4, "unit": "cups"},
            {"ingredient": "shredded carrot", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Macaroni and Cheese",
        "recipe_text": """1 pound elbow macaroni
1/4 cup unsalted butter
1/4 cup all-purpose flour
3 cups milk
2 cups shredded sharp cheddar cheese
1 cup shredded Gruyere cheese
1/2 teaspoon salt
1/4 teaspoon black pepper
1/4 teaspoon paprika""",
        "json_data": [
            {"ingredient": "elbow macaroni", "quantity": 1, "unit": "pound"},
            {"ingredient": "unsalted butter", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "all-purpose flour", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "milk", "quantity": 3, "unit": "cups"},
            {"ingredient": "shredded sharp cheddar cheese", "quantity": 2, "unit": "cups"},
            {"ingredient": "shredded gruyere cheese", "quantity": 1, "unit": "cup"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "black pepper", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "paprika", "quantity": 0.25, "unit": "teaspoon"}
        ]
    },
    {
        "name": "Beef Tacos",
        "recipe_text": """1 pound ground beef
1 tablespoon chili powder
1 teaspoon ground cumin
1/2 teaspoon salt
1/2 teaspoon garlic powder
1/2 teaspoon onion powder
1/4 cup water
8 hard taco shells
Toppings: shredded lettuce, diced tomatoes, shredded cheese, sour cream""",
        "json_data": [
            {"ingredient": "ground beef", "quantity": 1, "unit": "pound"},
            {"ingredient": "chili powder", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "ground cumin", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "garlic powder", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "onion powder", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "water", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "hard taco shell", "quantity": 8, "unit": None}
        ]
    },
    {
        "name": "Pico de Gallo",
        "recipe_text": """4 ripe Roma tomatoes, diced
1/2 medium white onion, finely chopped
1/2 cup chopped fresh cilantro
1 jalapeño, seeded and minced
2 tablespoons fresh lime juice
1/2 teaspoon salt""",
        "json_data": [
            {"ingredient": "ripe roma tomato", "quantity": 4, "unit": None},
            {"ingredient": "white onion", "quantity": 0.5, "unit": "medium"},
            {"ingredient": "chopped fresh cilantro", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "jalapeño", "quantity": 1, "unit": None},
            {"ingredient": "fresh lime juice", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"}
        ]
    },
    {
        "name": "Mango Salsa",
        "recipe_text": """2 ripe mangoes, diced
1/2 red onion, finely chopped
1/4 cup chopped fresh cilantro
1 jalapeño, seeded and minced
2 tablespoons lime juice
Pinch of salt""",
        "json_data": [
            {"ingredient": "ripe mango", "quantity": 2, "unit": None},
            {"ingredient": "red onion", "quantity": 0.5, "unit": None},
            {"ingredient": "chopped fresh cilantro", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "jalapeño", "quantity": 1, "unit": None},
            {"ingredient": "lime juice", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "salt", "quantity": 1, "unit": "pinch"}
        ]
    },
    {
        "name": "Strawberry Smoothie",
        "recipe_text": """1 cup frozen strawberries
1/2 cup plain yogurt
1/2 cup milk
1 tablespoon honey or maple syrup""",
        "json_data": [
            {"ingredient": "frozen strawberries", "quantity": 1, "unit": "cup"},
            {"ingredient": "plain yogurt", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "milk", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "honey or maple syrup", "quantity": 1, "unit": "tablespoon"}
        ]
    },
    {
        "name": "Blueberry Muffins",
        "recipe_text": """1 1/2 cups all-purpose flour
3/4 cup granulated sugar
2 teaspoons baking powder
1/2 teaspoon salt
1/3 cup vegetable oil
1 large egg
1/3 cup milk
1 cup fresh or frozen blueberries""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 1.5, "unit": "cups"},
            {"ingredient": "granulated sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "baking powder", "quantity": 2, "unit": "teaspoons"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "vegetable oil", "quantity": 0.33, "unit": "cup"},
            {"ingredient": "egg", "quantity": 1, "unit": "large"},
            {"ingredient": "milk", "quantity": 0.33, "unit": "cup"},
            {"ingredient": "fresh or frozen blueberries", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Pumpkin Pie",
        "recipe_text": """1 (15 ounce) can pumpkin puree
3/4 cup granulated sugar
1/2 teaspoon salt
1 teaspoon ground cinnamon
1/2 teaspoon ground ginger
1/4 teaspoon ground cloves
2 large eggs
1 (12 ounce) can evaporated milk
1 (9 inch) unbaked pie crust""",
        "json_data": [
            {"ingredient": "pumpkin puree", "quantity": 15, "unit": "ounce"},
            {"ingredient": "granulated sugar", "quantity": 0.75, "unit": "cup"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "ground cinnamon", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "ground ginger", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "ground cloves", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "evaporated milk", "quantity": 12, "unit": "ounce"},
            {"ingredient": "unbaked pie crust", "quantity": 9, "unit": "inch"}
        ]
    },
    {
        "name": "Butternut Squash Soup",
        "recipe_text": """1 medium butternut squash, peeled and cubed
1 tablespoon olive oil
1 medium onion, chopped
2 carrots, chopped
2 celery stalks, chopped
4 cups vegetable broth
1/2 teaspoon dried thyme
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "butternut squash", "quantity": 1, "unit": "medium"},
            {"ingredient": "olive oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "medium"},
            {"ingredient": "carrot", "quantity": 2, "unit": None},
            {"ingredient": "celery stalk", "quantity": 2, "unit": None},
            {"ingredient": "vegetable broth", "quantity": 4, "unit": "cups"},
            {"ingredient": "dried thyme", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Ratatouille",
        "recipe_text": """1/4 cup olive oil
1 large onion, thinly sliced
2 cloves garlic, minced
1 large eggplant, cut into 1-inch cubes
2 medium zucchini, cut into 1-inch cubes
1 red bell pepper, cut into 1-inch pieces
1 yellow bell pepper, cut into 1-inch pieces
4 ripe tomatoes, chopped
1 teaspoon dried herbs de Provence
Salt and freshly ground black pepper to taste""",
        "json_data": [
            {"ingredient": "olive oil", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "onion", "quantity": 1, "unit": "large"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "eggplant", "quantity": 1, "unit": "large"},
            {"ingredient": "zucchini", "quantity": 2, "unit": "medium"},
            {"ingredient": "red bell pepper", "quantity": 1, "unit": None},
            {"ingredient": "yellow bell pepper", "quantity": 1, "unit": None},
            {"ingredient": "ripe tomato", "quantity": 4, "unit": None},
            {"ingredient": "dried herbs de provence", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Lemonade",
        "recipe_text": """1 cup granulated sugar
1 cup water (for simple syrup)
1 cup fresh lemon juice (about 4-6 lemons)
3-4 cups cold water (to dilute)""",
        "json_data": [
            {"ingredient": "granulated sugar", "quantity": 1, "unit": "cup"},
            {"ingredient": "water", "quantity": 1, "unit": "cup"},
            {"ingredient": "fresh lemon juice", "quantity": 1, "unit": "cup"},
            {"ingredient": "cold water", "quantity": 4, "unit": "cups"}
        ]
    },
    {
        "name": "Iced Tea",
        "recipe_text": """6-8 black tea bags
4 cups boiling water
1/2 cup granulated sugar (optional)
4 cups cold water
Lemon slices for garnish""",
        "json_data": [
            {"ingredient": "black tea bag", "quantity": 8, "unit": None},
            {"ingredient": "boiling water", "quantity": 4, "unit": "cups"},
            {"ingredient": "granulated sugar", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "cold water", "quantity": 4, "unit": "cups"},
            {"ingredient": "lemon slices", "quantity": None, "unit": "for garnish"}
        ]
    },
    {
        "name": "Hot Chocolate",
        "recipe_text": """2 tablespoons unsweetened cocoa powder
2 tablespoons granulated sugar
1 cup milk
1/4 teaspoon vanilla extract
A pinch of salt""",
        "json_data": [
            {"ingredient": "unsweetened cocoa powder", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "granulated sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "milk", "quantity": 1, "unit": "cup"},
            {"ingredient": "vanilla extract", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 1, "unit": "pinch"}
        ]
    },
    {
        "name": "Classic Omelette",
        "recipe_text": """3 large eggs
2 tablespoons milk or water
Salt and freshly ground black pepper to taste
1 tablespoon unsalted butter
Optional fillings: cheese, chopped vegetables, cooked meat""",
        "json_data": [
            {"ingredient": "egg", "quantity": 3, "unit": "large"},
            {"ingredient": "milk or water", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"},
            {"ingredient": "unsalted butter", "quantity": 1, "unit": "tablespoon"}
        ]
    },
    {
        "name": "Crepes",
        "recipe_text": """1 cup all-purpose flour
2 large eggs
1/2 cup milk
1/2 cup water
1/4 teaspoon salt
2 tablespoons unsalted butter, melted""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 1, "unit": "cup"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "milk", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "water", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "salt", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "unsalted butter", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Waffles",
        "recipe_text": """2 cups all-purpose flour
2 tablespoons granulated sugar
1 tablespoon baking powder
1/2 teaspoon salt
2 large eggs, separated
1 3/4 cups milk
1/2 cup vegetable oil""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "cups"},
            {"ingredient": "granulated sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "baking powder", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "egg", "quantity": 2, "unit": "large"},
            {"ingredient": "milk", "quantity": 1.75, "unit": "cups"},
            {"ingredient": "vegetable oil", "quantity": 0.5, "unit": "cup"}
        ]
    },
    {
        "name": "Potato Salad",
        "recipe_text": """2 pounds Yukon Gold potatoes, peeled and cubed
1 cup mayonnaise
2 tablespoons white vinegar
1 tablespoon yellow mustard
1 teaspoon sugar
1/2 teaspoon salt
1/4 teaspoon black pepper
1 cup chopped celery
1/2 cup chopped red onion
2 hard-boiled eggs, chopped""",
        "json_data": [
            {"ingredient": "yukon gold potato", "quantity": 2, "unit": "pounds"},
            {"ingredient": "mayonnaise", "quantity": 1, "unit": "cup"},
            {"ingredient": "white vinegar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "yellow mustard", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "sugar", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "black pepper", "quantity": 0.25, "unit": "teaspoon"},
            {"ingredient": "chopped celery", "quantity": 1, "unit": "cup"},
            {"ingredient": "chopped red onion", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "hard-boiled egg", "quantity": 2, "unit": None}
        ]
    },
    {
        "name": "Cornbread",
        "recipe_text": """1 cup all-purpose flour
1 cup yellow cornmeal
2/3 cup granulated sugar
1 teaspoon salt
3 1/2 teaspoons baking powder
1/3 cup melted butter
1 large egg
1 cup milk""",
        "json_data": [
            {"ingredient": "all-purpose flour", "quantity": 1, "unit": "cup"},
            {"ingredient": "yellow cornmeal", "quantity": 1, "unit": "cup"},
            {"ingredient": "granulated sugar", "quantity": 0.67, "unit": "cup"},
            {"ingredient": "salt", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "baking powder", "quantity": 3.5, "unit": "teaspoons"},
            {"ingredient": "melted butter", "quantity": 0.33, "unit": "cup"},
            {"ingredient": "egg", "quantity": 1, "unit": "large"},
            {"ingredient": "milk", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Meatloaf",
        "recipe_text": """1 1/2 pounds ground beef
1 cup breadcrumbs
1/2 cup chopped onion
1/2 cup milk
1 large egg, beaten
1 tablespoon Worcestershire sauce
1 teaspoon salt
1/2 teaspoon black pepper
For the glaze:
1/4 cup ketchup
2 tablespoons brown sugar
1 tablespoon apple cider vinegar""",
        "json_data": [
            {"ingredient": "ground beef", "quantity": 1.5, "unit": "pounds"},
            {"ingredient": "breadcrumbs", "quantity": 1, "unit": "cup"},
            {"ingredient": "chopped onion", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "milk", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "egg", "quantity": 1, "unit": "large"},
            {"ingredient": "worcestershire sauce", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "black pepper", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "ketchup", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "brown sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "apple cider vinegar", "quantity": 1, "unit": "tablespoon"}
        ]
    },
    {
        "name": "Shepherd's Pie",
        "recipe_text": """1 tablespoon vegetable oil
1 large onion, chopped
2 carrots, chopped
1 pound ground lamb or beef
2 tablespoons all-purpose flour
1 cup beef broth
1 tablespoon tomato paste
1 teaspoon dried thyme
Salt and pepper to taste
2 pounds potatoes, peeled and quartered
1/4 cup milk
2 tablespoons butter""",
        "json_data": [
            {"ingredient": "vegetable oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "large"},
            {"ingredient": "carrot", "quantity": 2, "unit": None},
            {"ingredient": "ground lamb or beef", "quantity": 1, "unit": "pound"},
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "beef broth", "quantity": 1, "unit": "cup"},
            {"ingredient": "tomato paste", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "dried thyme", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"},
            {"ingredient": "potato", "quantity": 2, "unit": "pounds"},
            {"ingredient": "milk", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "butter", "quantity": 2, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Fish and Chips",
        "recipe_text": """1 1/2 pounds cod or haddock fillets
1 cup all-purpose flour
1 teaspoon baking powder
1/2 teaspoon salt
1 cup beer, cold
Vegetable oil for frying
4 large russet potatoes, cut into fries""",
        "json_data": [
            {"ingredient": "cod or haddock fillet", "quantity": 1.5, "unit": "pounds"},
            {"ingredient": "all-purpose flour", "quantity": 1, "unit": "cup"},
            {"ingredient": "baking powder", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "beer", "quantity": 1, "unit": "cup"},
            {"ingredient": "vegetable oil", "quantity": None, "unit": "for frying"},
            {"ingredient": "russet potato", "quantity": 4, "unit": "large"}
        ]
    },
    {
        "name": "Clam Chowder",
        "recipe_text": """4 slices bacon, chopped
1 large onion, chopped
2 celery stalks, chopped
2 tablespoons all-purpose flour
2 cups clam juice
2 cups peeled and diced potatoes
2 (6.5 ounce) cans chopped clams, undrained
2 cups half-and-half
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "bacon", "quantity": 4, "unit": "slices"},
            {"ingredient": "onion", "quantity": 1, "unit": "large"},
            {"ingredient": "celery stalk", "quantity": 2, "unit": None},
            {"ingredient": "all-purpose flour", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "clam juice", "quantity": 2, "unit": "cups"},
            {"ingredient": "peeled and diced potato", "quantity": 2, "unit": "cups"},
            {"ingredient": "chopped clams", "quantity": 13, "unit": "ounce"},
            {"ingredient": "half-and-half", "quantity": 2, "unit": "cups"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Minestrone Soup",
        "recipe_text": """1 tablespoon olive oil
1 medium onion, chopped
2 carrots, chopped
2 celery stalks, chopped
2 cloves garlic, minced
1 (28 ounce) can diced tomatoes, undrained
4 cups vegetable broth
1 (15 ounce) can kidney beans, rinsed and drained
1 (15 ounce) can great northern beans, rinsed and drained
1 cup small pasta
1 zucchini, chopped
1/2 cup chopped fresh parsley
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "olive oil", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "onion", "quantity": 1, "unit": "medium"},
            {"ingredient": "carrot", "quantity": 2, "unit": None},
            {"ingredient": "celery stalk", "quantity": 2, "unit": None},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "diced tomatoes", "quantity": 28, "unit": "ounce"},
            {"ingredient": "vegetable broth", "quantity": 4, "unit": "cups"},
            {"ingredient": "kidney beans", "quantity": 15, "unit": "ounce"},
            {"ingredient": "great northern beans", "quantity": 15, "unit": "ounce"},
            {"ingredient": "small pasta", "quantity": 1, "unit": "cup"},
            {"ingredient": "zucchini", "quantity": 1, "unit": None},
            {"ingredient": "chopped fresh parsley", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Hummus",
        "recipe_text": """1 (15 ounce) can chickpeas, rinsed and drained
1/4 cup fresh lemon juice
1/4 cup tahini
2 cloves garlic, minced
2 tablespoons olive oil
1/2 teaspoon ground cumin
Salt to taste
2-3 tablespoons water""",
        "json_data": [
            {"ingredient": "chickpeas", "quantity": 15, "unit": "ounce"},
            {"ingredient": "fresh lemon juice", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "tahini", "quantity": 0.25, "unit": "cup"},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "olive oil", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "ground cumin", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "water", "quantity": 3, "unit": "tablespoons"}
        ]
    },
    {
        "name": "Tzatziki Sauce",
        "recipe_text": """1 cup plain Greek yogurt
1/2 cucumber, peeled, seeded, and grated
2 cloves garlic, minced
1 tablespoon fresh lemon juice
1 tablespoon chopped fresh dill
Salt and pepper to taste""",
        "json_data": [
            {"ingredient": "plain greek yogurt", "quantity": 1, "unit": "cup"},
            {"ingredient": "cucumber", "quantity": 0.5, "unit": None},
            {"ingredient": "garlic", "quantity": 2, "unit": "cloves"},
            {"ingredient": "fresh lemon juice", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "chopped fresh dill", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Pesto Pasta",
        "recipe_text": """1 pound pasta of your choice
2 cups fresh basil leaves
1/2 cup grated Parmesan cheese
1/2 cup olive oil
1/3 cup pine nuts
3 cloves garlic, minced
Salt and freshly ground black pepper to taste""",
        "json_data": [
            {"ingredient": "pasta", "quantity": 1, "unit": "pound"},
            {"ingredient": "fresh basil leaves", "quantity": 2, "unit": "cups"},
            {"ingredient": "grated parmesan cheese", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "olive oil", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "pine nuts", "quantity": 0.33, "unit": "cup"},
            {"ingredient": "garlic", "quantity": 3, "unit": "cloves"},
            {"ingredient": "salt", "quantity": None, "unit": "to taste"},
            {"ingredient": "freshly ground black pepper", "quantity": None, "unit": "to taste"}
        ]
    },
    {
        "name": "Lasagna",
        "recipe_text": """1 pound sweet Italian sausage
1 pound lean ground beef
1 large white onion, chopped
3 cloves garlic, minced
1 (28 ounce) can crushed tomatoes
2 (6 ounce) cans tomato paste
2 (6.5 ounce) cans canned tomato sauce
1/2 cup water
2 tablespoons sugar
1 1/2 teaspoons dried basil leaves
1/2 teaspoon fennel seeds
1 teaspoon Italian seasoning
1 pound lasagna noodles
16 ounces ricotta cheese
1 large egg
1/2 cup grated Parmesan cheese
1 1/2 pounds mozzarella cheese, sliced""",
        "json_data": [
            {"ingredient": "sweet italian sausage", "quantity": 1, "unit": "pound"},
            {"ingredient": "lean ground beef", "quantity": 1, "unit": "pound"},
            {"ingredient": "white onion", "quantity": 1, "unit": "large"},
            {"ingredient": "garlic", "quantity": 3, "unit": "cloves"},
            {"ingredient": "crushed tomatoes", "quantity": 28, "unit": "ounce"},
            {"ingredient": "tomato paste", "quantity": 12, "unit": "ounce"},
            {"ingredient": "canned tomato sauce", "quantity": 13, "unit": "ounce"},
            {"ingredient": "water", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "sugar", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "dried basil leaves", "quantity": 1.5, "unit": "teaspoons"},
            {"ingredient": "fennel seeds", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "italian seasoning", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "lasagna noodles", "quantity": 1, "unit": "pound"},
            {"ingredient": "ricotta cheese", "quantity": 16, "unit": "ounces"},
            {"ingredient": "egg", "quantity": 1, "unit": "large"},
            {"ingredient": "grated parmesan cheese", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "mozzarella cheese", "quantity": 1.5, "unit": "pounds"}
        ]
    },
    {
        "name": "Chicken Parmesan",
        "recipe_text": """2 boneless, skinless chicken breasts
1 cup Italian-style bread crumbs
1/2 cup grated Parmesan cheese
1 large egg, beaten
1/2 cup all-purpose flour
2 tablespoons olive oil
1 cup marinara sauce
1 cup shredded mozzarella cheese""",
        "json_data": [
            {"ingredient": "boneless, skinless chicken breast", "quantity": 2, "unit": None},
            {"ingredient": "italian-style bread crumbs", "quantity": 1, "unit": "cup"},
            {"ingredient": "grated parmesan cheese", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "egg", "quantity": 1, "unit": "large"},
            {"ingredient": "all-purpose flour", "quantity": 0.5, "unit": "cup"},
            {"ingredient": "olive oil", "quantity": 2, "unit": "tablespoons"},
            {"ingredient": "marinara sauce", "quantity": 1, "unit": "cup"},
            {"ingredient": "shredded mozzarella cheese", "quantity": 1, "unit": "cup"}
        ]
    },
    {
        "name": "Fajitas",
        "recipe_text": """1 1/2 pounds boneless, skinless chicken breasts, sliced
1 large onion, sliced
2 bell peppers (any color), sliced
3 tablespoons olive oil
1 tablespoon chili powder
1 teaspoon ground cumin
1/2 teaspoon paprika
1/2 teaspoon salt
1/2 teaspoon black pepper
8-10 flour tortillas
Toppings: sour cream, guacamole, salsa, shredded cheese""",
        "json_data": [
            {"ingredient": "boneless, skinless chicken breast", "quantity": 1.5, "unit": "pounds"},
            {"ingredient": "onion", "quantity": 1, "unit": "large"},
            {"ingredient": "bell pepper", "quantity": 2, "unit": None},
            {"ingredient": "olive oil", "quantity": 3, "unit": "tablespoons"},
            {"ingredient": "chili powder", "quantity": 1, "unit": "tablespoon"},
            {"ingredient": "ground cumin", "quantity": 1, "unit": "teaspoon"},
            {"ingredient": "paprika", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "salt", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "black pepper", "quantity": 0.5, "unit": "teaspoon"},
            {"ingredient": "flour tortilla", "quantity": 10, "unit": None}
        ]
    }
]

def create_recipe_files():
    """
    Creates 'recipe_in' and 'json_out' directories and populates them
    with recipe and JSON files from the recipes_data list.
    """
    # Define directory names
    recipe_dir = "recipe_in"
    json_dir = "json_out"

    # Create directories if they don't exist
    os.makedirs(recipe_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    # Loop through the data and create files
    for i, data in enumerate(recipes_data, 1):
        recipe_filename = os.path.join(recipe_dir, f"recipe_{i}.txt")
        json_filename = os.path.join(json_dir, f"recipe_{i}.json")

        # Write the recipe text file
        with open(recipe_filename, "w", encoding="utf-8") as f:
            f.write(data["recipe_text"])

        # Write the JSON data file
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data["json_data"], f, indent=4)
            
        print(f"Created {recipe_filename} and {json_filename}")

    print("\nFile creation complete.")
    print(f"Total recipes created: {len(recipes_data)}")

if __name__ == "__main__":
    create_recipe_files()
