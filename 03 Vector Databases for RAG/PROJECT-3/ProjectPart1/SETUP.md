# 

## Part 1 Task 1: A. Install the Required Packages

```bash
pip install numpy==2.3.1
pip install scipy==1.16.0
pip install chromadb==1.0.12
pip install sentence-transformers==4.1.0
pip install ibm-watsonx-ai==1.3.24
```

## Part 1 Task 1: B. Download the Food Dataset
```bash
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/sN1PIR8qp1SJ6K7syv72qQ/FoodDataSet.json
```

This dataset contains rich food information including:

* `food_id:` Unique identifier for each food item
* `food_name:` Name of the dish
* `food_description:` Detailed description of the food
* `food_calories_per_serving:` Caloric content per serving
* `food_nutritional_factors:` Breakdown of carbohydrates, protein, and fat
* `food_ingredients:` List of ingredients used
* `food_health_benefits:` Health benefits of the food
* `cooking_method:` How the food is prepared (baking, grilling, etc.)
* `cuisine_type:` Type of cuisine (American, Italian, etc.)
* `food_features:` Taste, texture, appearance, and serving details

Example food item structure:

```json
{
    "food_id": 1,
    "food_name": "Apple Pie",
    "food_description": "A classic dessert made with a buttery, flaky crust filled with tender, spiced apples.",
    "food_calories_per_serving": 320,
    "food_nutritional_factors": {
        "carbohydrates": "42g",
        "protein": "2g", 
        "fat": "16g"
    },
    "food_ingredients": ["Apples", "Flour", "Butter", "Sugar", "Cinnamon", "Nutmeg"],
    "food_health_benefits": "Rich in antioxidants and dietary fiber",
    "cooking_method": "Baking",
    "cuisine_type": "American",
    "food_features": {
        "taste": "sweet",
        "texture": "crisp and tender",
        "appearance": "golden brown",
        "preparation": "baked",
        "serving_type": "hot"
    }
}

```

## Part 2 Task 1: B. `shared_functions.py`

## Part 2 Task 2: A. Create the Interactive Search File `interactive_search.py`

#### Run the file
```bash
python3.11 interactive_search.py
```

```text
Try different search queries when prompted:
"chocolate dessert"
"Italian food"
"sweet treats"
```

## Part 3 Task 1: Building the Advanced Search System

### Create `advanced_search.py`

```bash
python3.11 advanced_search.py
```

```text
Test different search options:
Option 1: Basic search with "chocolate dessert"
Option 2: Cuisine search for "sweet" in "American" cuisine
Option 3: Calorie search for "dessert" under 300 calories
Option 4: Combined Filters - Use multiple filters together
Option 5: Run the demonstration mode
Option 6: Show the help menu
Option 7: Quit – Exit the program
```

## Part 4 Task 1: Building the RAG Chatbot System

### Understanding RAG Architecture
Before implementing the code, let's understand what makes this a true RAG system:

1. **Retrieval Phase:** Search the vector database for relevant food items based on user query
2. **Context Building:** Extract and structure relevant information from search results
3. **Augmented Generation:** Pass both the user query and retrieved context to an LLM
4. **Response Generation:** The LLM generates a natural, contextual response using the retrieved information

### Create `enhanced_rag_chatbot.py`

#### Test Different Query Types:

* **Natural Language Queries:**

    * "I want something healthy and light for lunch"
    * "What Italian comfort food do you recommend?"
    * "I'm looking for protein-rich breakfast options under 300 calories"

* **Specific Preference Queries:**

    * "Spicy Asian dishes for dinner"
    * "Sweet desserts for a special occasion"
    * "Low-calorie snacks for weight management"

* **Complex Context Queries:**

    * "I'm feeling sick and want something soothing"
    * "Quick meal ideas for busy weeknight"
    * "Celebratory foods for a party"
    
* **Test the Comparison Feature:**
    * Type `compare` when prompted
    * First query: "chocolate dessert"
    * Second query: "healthy breakfast"
    * Observe how the AI analyzes the differences

* **Observe the RAG Process:**
    * Notice the "Searching vector database…" message (Retrieval)
    * See "Generating AI-powered response…" (Augmented Generation)
    * Compare the AI response with the detailed search results shown below


## Part 5: Testing and Comparing All Three Systems

#### Create `system_comparison.py`

#### Run the file
```bash
python3.11 system_comparison.py
```

## Practice Exercises
Now that you have built and tested all three food search systems, complete these practice exercises to deepen your understanding and extend the functionality.

### Exercise 1: Enhance the Interactive Search System
Modify the `interactive_search.py` file to add search history tracking. In essence, you want to keep track of user's previous searches and allow them to view history with a "history" command.

Hint: Add a global variable to store the history, and create new command handlers.

### Exercise 2: Build a Food Calorie Checker
Create an interactive tool in a new file called `calorie_checker.py` that helps users find foods within their calorie budget:

Ask user for their calorie budget - Get the maximum calories they want.

Let them search for foods and show if they fit the budget - Use filtered search to check calorie limits.

Goal: Build a complete interactive program that repeatedly asks for searches and shows budget-friendly results.

### Exercise 3: Query Different Result Counts
Practice controlling similarity search results by varying the number of results returned in a new file called `result_limiter.py`:

Test different result limits - Use the `n_results` parameter to get different amounts of results.

Compare result quality - See how result quality changes with more or fewer results.

Hint: Use the `perform_similarity_search()` function with different `n_results` values (1, 3, 5, 10).
