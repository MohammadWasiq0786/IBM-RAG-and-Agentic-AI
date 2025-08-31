# Create a file called result_limiter.py
from shared_functions import *

def test_result_limits():
    """Test how different result limits affect search quality"""
    print("📊 SIMILARITY SEARCH RESULT LIMITER")
    print("=" * 45)
    
    # Setup
    food_items = load_food_data('FoodDataSet.json')
    collection = create_similarity_search_collection("result_test")
    populate_similarity_collection(collection, food_items)
    
    # Test query
    query = "spicy chicken"
    print(f"🔍 Testing query: '{query}'\n")
    
    # Test different result limits
    result_limits = [1, 3, 5, 10]
    
    for limit in result_limits:
        print(f"📋 Getting top {limit} result(s):")
        print("-" * 30)
        
        results = perform_similarity_search(collection, query, limit)
        
        if results:
            for i, result in enumerate(results, 1):
                score = result['similarity_score']
                print(f"  {i}. {result['food_name']}")
                print(f"     Score: {score:.3f}")
                print(f"     Cuisine: {result['cuisine_type']}")
                print(f"     Calories: {result['food_calories_per_serving']}")
                print()
            
            # Show quality analysis
            scores = [r['similarity_score'] for r in results]
            avg_score = sum(scores) / len(scores)
            print(f"  📈 Average score: {avg_score:.3f}")
            print(f"  🎯 Best score: {max(scores):.3f}")
            if len(scores) > 1:
                print(f"  📉 Worst score: {min(scores):.3f}")
        else:
            print("  No results found!")
        
        print("=" * 45)
    
    # Interactive test with user input
    print("\n🎮 INTERACTIVE MODE:")
    print("Test your own queries with different result limits!")
    
    while True:
        user_query = input("\nEnter search query (or press Enter to exit): ").strip()
        if not user_query:
            break
        
        try:
            limit_input = input("How many results? (1-20): ").strip()
            limit = int(limit_input) if limit_input.isdigit() and 1 <= int(limit_input) <= 20 else 5
        except:
            limit = 5
        
        print(f"\n🔍 Searching for '{user_query}' (limit: {limit})")
        results = perform_similarity_search(collection, user_query, limit)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['food_name']} (Score: {result['similarity_score']:.3f})")
            
            # Show quality analysis
            scores = [r['similarity_score'] for r in results]
            avg_score = sum(scores) / len(scores)
            print()
            print(f"  📈 Average score: {avg_score:.3f}")
            print(f"  🎯 Best score: {max(scores):.3f}")
            if len(scores) > 1:
                print(f"  📉 Worst score: {min(scores):.3f}")
        else:
            print("No results found!")
    
    print("\n👋 Thanks for testing result limits!")

if __name__ == "__main__":
    test_result_limits()