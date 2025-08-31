import asyncio
import logging
from pydantic import BaseModel, Field
from typing import List
from beeai_framework.backend import ChatModel, ChatModelParameters, UserMessage, SystemMessage

# Define a structured output for business planning
class BusinessPlan(BaseModel):
    """A comprehensive business plan structure."""
    business_name: str = Field(description="Catchy name for the business")
    elevator_pitch: str = Field(description="30-second description of the business")
    target_market: str = Field(description="Primary target audience")
    unique_value_proposition: str = Field(description="What makes this business special")
    revenue_streams: List[str] = Field(description="Ways the business will make money")
    startup_costs: str = Field(description="Estimated initial investment needed")
    key_success_factors: List[str] = Field(description="Critical elements for success")

async def structured_output_example():
    llm = ChatModel.from_name("openai:gpt-5-nano", ChatModelParameters(temperature=0))
    
    messages = [
        SystemMessage(content="You are an expert business consultant and entrepreneur."),
        UserMessage(content="Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    ]
    
    # Generate structured response using create_structure() method
    response = await llm.create_structure(
        schema=BusinessPlan,
        messages=messages
    )
    
    print("User: Create a business plan for a mobile app that helps people find and book unique local experiences in their city.")
    print("\n🚀 AI-Generated Business Plan:")
    print(f"💡 Business Name: {response.object['business_name']}")
    print(f"🎯 Elevator Pitch: {response.object['elevator_pitch']}")
    print(f"👥 Target Market: {response.object['target_market']}")
    print(f"⭐ Unique Value Proposition: {response.object['unique_value_proposition']}")
    print(f"💰 Revenue Streams: {', '.join(response.object['revenue_streams'])}")
    print(f"💵 Startup Costs: {response.object['startup_costs']}")
    print(f"🔑 Key Success Factors:")
    for factor in response.object['key_success_factors']:
        print(f"  - {factor}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL) # Suppress unwanted warnings
    await structured_output_example()

if __name__ == "__main__":
    asyncio.run(main())


"""
Output::

User: Create a business plan for a mobile app that helps people find and book unique local experiences in their city.

🚀 AI-Generated Business Plan:
💡 Business Name: CityPulse Experiences
🎯 Elevator Pitch: CityPulse Experiences is a mobile app that helps locals and travelers discover and instantly book unique, authentic experiences in their city—think hidden-gem tours, hands-on workshops, intimate tastings, and pop-up events—curated by vetted locals. With real-time availability, seamless checkout, and personalized recommendations, everyday moments become unforgettable adventures.
👥 Target Market: Urban residents and short-stay travelers seeking authentic, local experiences; early adopters of mobile booking apps; hosts offering distinctive experiences in their city.
⭐ Unique Value Proposition: Locally curated, vetted experiences with real-time availability, transparent pricing, and trusted hosts, plus personalized discovery that goes beyond generic tours. Safe, seamless booking makes it easy to unlock authentic city moments you can’t find on mass-market platforms.
💰 Revenue Streams: Booking commissions on reservations (percentage of each booking), Host listing fees or subscriptions for premium exposure, Featured or boosted listings for high-visibility experiences, In-app advertising and partnerships with venues and brands, B2B offerings: corporate/group experiences and gift cards, Data insights and market reports sold to partner businesses (aggregated, anonymized)
💵 Startup Costs: Estimated initial investment: USD 600,000–900,000. Breakdown (high level): MVP development for iOS/Android and backend (USD 300k–500k); product design and UX (USD 50k–100k); host onboarding, content curation, and safety infrastructure (USD 50k–100k); legal, compliance, and payments setup (USD 20k–60k); initial marketing and growth campaigns (USD 100k–200k); operations, team salaries, and contingencies for 12 months (USD 80k–120k).
🔑 Key Success Factors:
  - Strong, vetted host network with a smooth onboarding process
  - High-quality, unique experiences that differentiate from mass-market tours
  - Fast, secure payments with real-time availability and instant booking
  - Personalized discovery and intelligent recommendations
  - Robust trust, safety, and review systems
  - Active partnerships with local venues, organizers, and brands
  - Scalable marketing, referral programs, and content-driven growth
  - Transparent pricing, clear policies, and responsive customer support

"""