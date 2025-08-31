import asyncio
import logging
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage, SystemMessage
# Initialize the chat model
async def basic_chat_example():
    # Create a chat model instance (works with OpenAI, WatsonX, etc.)
    llm = ChatModel.from_name("watsonx:ibm/granite-3-3-8b-instruct", ChatModelParameters(temperature=0))
    
    # Create a conversation about something everyone finds interesting
    messages = [
        SystemMessage(content="You are a helpful AI assistant and creative writing expert."),
        UserMessage(content="Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    ]
    
    # Generate response using create() method
    response = await llm.create(messages=messages)
    
    print("User: Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.")
    print(f"Assistant: {response.get_text_content()}")
    
    return response


# Run the basic chat example
async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    response = await basic_chat_example()
if __name__ == "__main__":
    asyncio.run(main())


# --------------------------------------------- #

"""
Output::

User: Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet.
Assistant: 1. **Eco-Friendly Gourmet Meal Kits Delivery Service**: A food delivery service that focuses on delivering organic, locally-sourced, and sustainably-packaged meal kits. The service would partner with local farmers and suppliers to ensure freshness and reduce carbon footprint. Customers can choose from a variety of gourmet recipes, and the service would provide step-by-step instructions along with pre-measured ingredients.

2. **Virtual Culinary School Food Delivery**: A business that combines online culinary education with meal delivery. Customers sign up for cooking classes led by professional chefs, and the necessary ingredients for the class are delivered to their doorstep. After the class, customers can cook along and enjoy their homemade meal.

3. **Personalized Nutrition Meal Plans Delivery**: A service that uses AI and genetic data to create personalized meal plans based on individual dietary needs, health goals, and food preferences. The service would deliver fully prepared meals tailored to each customer's unique nutritional requirements.

4. **Zero-Waste Meal Prep Delivery**: A food delivery service that focuses on zero-waste meal prep. Customers receive meal components in bulk, such as grains, proteins, and vegetables, packaged in reusable or compostable containers. The service would also provide instructions on how to prepare meals and minimize food waste.

5. **Cultural Cuisine Exchange Delivery**: A platform that connects home cooks from different cultural backgrounds to share their traditional recipes and meals with a broader audience. Customers can order meals from various cultural cuisines, supporting local home cooks and promoting cultural exchange.

6. **Time-Travel Meal Delivery**: A service that offers meals from different historical periods. Using extensive research and recreated recipes, the service delivers authentic meals from the Renaissance, Ancient Rome, Medieval Europe, etc. This unique concept would appeal to history buffs and food enthusiasts alike.

7. **Aquaponics Urban Farm Food Delivery**: A food delivery service that partners with urban aquaponic farms to deliver fresh, sustainably-grown produce and fish directly to customers' doors. The service would educate customers on the benefits of aquaponics and the importance of urban farming.

8. **Interactive Cooking Experience Delivery**: A food delivery service that combines live, interactive cooking classes with meal delivery. Customers can join a live class led by a professional chef, cook along in real-time, and enjoy their homemade meal with fellow participants.

9. **Vertical Farm Food Delivery**: A service that partners with vertical farming facilities to deliver fresh, pesticide-free produce grown in urban, eco-friendly farms. The service would emphasize sustainability and innovation in food production.

10. **Fusion Food Delivery**: A food delivery service that specializes in creating unique fusion dishes by blending elements from different cuisines. The menu would change regularly, allowing customers to explore new flavor combinations and culinary experiences.
"""