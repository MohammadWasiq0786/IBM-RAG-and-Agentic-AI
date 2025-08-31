import asyncio
import logging
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.agents.experimental.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.handoff import HandoffTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool

async def multi_agent_travel_planner_with_language():
    """
    Advanced Multi-Agent Travel Planning System with Language Expert
    
    This system demonstrates:
    1. Specialized agent roles and coordination
    2. Tool-based inter-agent communication
    3. Requirements-based execution control
    4. Language and cultural expertise integration
    5. Comprehensive travel planning workflow
    """
    
    # Initialize the language model
    llm = ChatModel.from_name(
        "watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", 
        ChatModelParameters(temperature=0)
    )
    
    # === AGENT 1: DESTINATION RESEARCH EXPERT ===
    destination_expert = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="""You are a Destination Research Expert specializing in comprehensive travel destination analysis.

        Your expertise:
        - Landmarks and tourist activities
        - Best times to visit and seasonal considerations
        - Transportation options and accessibility
        - Safety considerations and travel advisories

        Always provide detailed, factual information with clear source attribution.""",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=5,
                consecutive_allowed=False
            ),
            ConditionalRequirement(
                WikipediaTool,
                only_after=[ThinkTool],
                min_invocations=1,
                max_invocations=4,
                consecutive_allowed=False
            ),
        ]
    )
    
    # === AGENT 2: TRAVEL METEOROLOGIST ===
    travel_meteorologist = RequirementAgent(
        llm=llm,
        tools=[OpenMeteoTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="""You are a Travel Meteorologist specializing in weather analysis for travel planning.

        Your expertise:
        - Climate patterns and seasonal weather analysis
        - Travel-specific weather recommendations
        - Packing suggestions based on weather forecasts
        - Activity planning based on weather conditions
        - Regional climate variations and microclimates
        - Weather-related travel risks and precautions

        Focus on actionable weather guidance for travelers.""",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=2
            ),
            ConditionalRequirement(
                OpenMeteoTool,
                only_after=[ThinkTool],
                min_invocations=1,
                max_invocations=1
            )
        ]
    )
    
    # === AGENT 3: LANGUAGE & CULTURAL EXPERT ===
    language_and_culture_expert = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool(), ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="""You are a Language & Cultural Expert specializing in linguistic and cultural guidance for travelers.

        Your expertise:
        - Local languages and dialects spoken in destinations
        - Essential phrases and communication tips for travelers
        - Cultural etiquette, customs, and social norms
        - Religious and cultural sensitivities to be aware of
        - Local communication styles and business etiquette
        - Cultural festivals, events, and local celebrations
        - Dining customs, tipping practices, and social interactions

        Always emphasize cultural sensitivity and respectful travel practices.""",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                min_invocations=1,
                max_invocations=3,
                consecutive_allowed=False
            ),
        ]
    )
    
    # === AGENT 4: TRAVEL COORDINATOR (MAIN INTERFACE) ===
    # Create handoff tools for coordination with unique names
    handoff_to_destination = HandoffTool(
        destination_expert,
        name="DestinationResearch",
        description="Consult our Destination Research Expert for comprehensive information about travel destinations, attractions, and practical travel guidance."
    )
    handoff_to_weather = HandoffTool(
        travel_meteorologist,
        name="WeatherPlanning", 
        description="Consult our Travel Meteorologist for weather forecasts, climate analysis, and weather-appropriate travel recommendations."
    )
    handoff_to_language = HandoffTool(
        language_and_culture_expert,
        name="LanguageCulturalGuidance",
        description="Consult our Language & Cultural Expert for essential phrases, cultural etiquette, and communication guidance for respectful travel."
    )
    
    travel_coordinator = RequirementAgent(
        llm=llm,
        tools=[handoff_to_destination, handoff_to_weather, handoff_to_language, ThinkTool()],
        memory=UnconstrainedMemory(),
        instructions="""You are the Travel Coordinator, the main interface for comprehensive travel planning.

        Your role:
        - Understand traveler requirements and preferences
        - Coordinate with specialized expert agents as needed
        - Synthesize information from multiple sources
        - Create comprehensive, actionable travel recommendations
        - Ensure all aspects of travel planning are covered

        Available Expert Agents:
        - Destination Expert: Practical destination information
        - Travel Meteorologist: Weather analysis and climate recommendations  
        - Language Expert: Language tips, cultural etiquette, and communication guidance

        Coordination Process:
        1. Think about what information is needed for comprehensive travel planning
        2. Delegate specific queries to appropriate expert agents using handoff tools
        3. Gather insights from multiple specialists
        4. Synthesize information into cohesive travel recommendations
        5. Provide a complete travel planning summary

        Always ensure travelers receive well-rounded guidance covering destinations and landmarks, weather, and cultural considerations.""",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(ThinkTool, consecutive_allowed=False),
            AskPermissionRequirement(["DestinationResearch", "WeatherPlanning", "LanguageCulturalGuidance"])
        ]
    )
    

    query = """I'm planning a 2-week cultural immersion trip to Japan (Tokyo and Osaka) as a first-time visitor. 
    I want to experience traditional culture, visit historical sites, and interact with locals. 
    I speak only English and want to be respectful of Japanese customs. 
    What should I know about the destination, weather expectations, and language/cultural tips?"""
    
    result = await travel_coordinator.run(query)
    print(f"\n📋 Comprehensive Travel Plan:\n{result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await multi_agent_travel_planner_with_language()

if __name__ == "__main__":
    asyncio.run(main())


"""
Output::

--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["DestinationResearch", "WeatherPlanning", "LanguageCulturalGuidance"], "thoughts": "To plan a comprehensive trip to Japan, I need to gather information about the destination, weather, and cultural/language aspects. I'll start by researching Tokyo and Osaka."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ HandoffTool[DestinationResearch][start]: {"input": {"input": {"task": "Tokyo and Osaka cultural immersion trip historical sites and traditional culture"}}}
The agent wants to use the 'DestinationResearch tool.'
Input: {'input': {'task': 'Tokyo and Osaka cultural immersion trip historical sites and traditional culture'}, 'options': None}
Do you allow it? (yes/no): yes
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Destination Expert for historical sites and traditional culture in Tokyo and Osaka"], "thoughts": "To get detailed information about historical sites and traditional culture in Tokyo and Osaka, I will consult the Destination Expert."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Tokyo historical sites"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Use Destination Expert to get information on historical sites and traditional culture in Tokyo and Osaka"], "thoughts": "Since Wikipedia search didn't yield results, I'll directly consult the Destination Expert for detailed information on historical sites and traditional culture in both cities."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Japan weather August"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Consult Travel Meteorologist for weather information"], "thoughts": "Since the Wikipedia search for weather information didn't work, I'll consult the Travel Meteorologist for detailed weather expectations in Tokyo and Osaka during the trip period."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Japanese cultural etiquette"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Consult Language Expert for cultural etiquette and language tips"], "thoughts": "Since the Wikipedia search didn't provide the needed cultural etiquette information, I'll consult the Language Expert for guidance on cultural etiquette and language tips for interacting with locals in Japan."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "### Comprehensive Travel Planning Summary for Japan Trip\n\n#### Destination Information\nFor a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:\n- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.\n- Osaka: Explore Osaka Castle and the Dotonbori area.\n\n#### Weather Expectations\nLate August is hot and humid in Japan, with temperatures often reaching above 30°C (86°F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.\n\n#### Language and Cultural Tips\n- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).\n- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.\n- Dress modestly when visiting temples and shrines.\n- Understand that tipping is not customary and may be considered rude in some situations.\n\nBy being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
<-- 🛠️ HandoffTool[DestinationResearch][finish]: "### Comprehensive Travel Planning Summary for Japan Trip\n\n#### Destination Information\nFor a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:\n- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.\n- Osaka: Explore Osaka Castle and the Dotonbori area.\n\n#### Weather Expectations\nLate August is hot and humid in Japan, with temperatures often reaching above 30°C (86°F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.\n\n#### Language and Cultural Tips\n- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).\n- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.\n- Dress modestly when visiting temples and shrines.\n- Understand that tipping is not customary and may be considered rude in some situations.\n\nBy being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan."
--> 🛠️ HandoffTool[WeatherPlanning][start]: {"input": {"input": {"task": "Tokyo and Osaka weather forecast for late August"}}}
The agent wants to use the 'WeatherPlanning tool.'
Input: {'input': {'task': 'Tokyo and Osaka weather forecast for late August'}, 'options': None}
Do you allow it? (yes/no): yes
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["OpenMeteoTool"], "thoughts": "To provide a weather forecast for Tokyo and Osaka in late August, I'll use the OpenMeteoTool to retrieve the relevant weather data."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ OpenMeteoTool[OpenMeteoTool][start]: {"input": {"input": {"country": "Japan", "end_date": "2025-09-05", "location_name": "Tokyo", "start_date": "2025-08-25", "temperature_unit": "celsius"}}}
<-- 🛠️ OpenMeteoTool[OpenMeteoTool][finish]: {"latitude": 35.7, "longitude": 139.6875, "generationtime_ms": 0.11646747589111328, "utc_offset_seconds": 0, "timezone": "GMT", "timezone_abbreviation": "GMT", "elevation": 40.0, "current_units": {"time": "iso8601", "interval": "seconds", "temperature_2m": "°C", "rain": "mm", "relative_humidity_2m": "%", "wind_speed_10m": "km/h"}, "current": {"time": "2025-08-30T09:30", "interval": 900, "temperature_2m": 30.5, "rain": 0.0, "relative_humidity_2m": 71, "wind_speed_10m": 5.6}, "daily_units": {"time": "iso8601", "temperature_2m_max": "°C", "temperature_2m_min": "°C", "rain_sum": "mm"}, "daily": {"time": ["2025-08-25", "2025-08-26", "2025-08-27", "2025-08-28", "2025-08-29", "2025-08-30", "2025-08-31", "2025-09-01", "2025-09-02", "2025-09-03", "2025-09-04", "2025-09-05"], "temperature_2m_max": [33.3, 32.8, 33.8, 30.8, 31.2, 35.5, 33.9, 32.5, 33.8, 34.1, 26.8, 37.3], "temperature_2m_min": [24.5, 26.0, 24.9, 22.4, 24.5, 25.3, 25.7, 25.5, 27.4, 25.6, 24.2, 26.5], "rain_sum": [4.0, 0.0, 0.4, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 22.5, 0.0]}}
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["OpenMeteoTool"], "thoughts": "I have the weather data for Tokyo. Now, I need to retrieve the weather forecast for Osaka in late August."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "### Comprehensive Travel Planning Summary for Japan Trip\n\n#### Destination Information\nFor a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:\n- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.\n- Osaka: Explore Osaka Castle and the Dotonbori area.\n\n#### Weather Expectations\nLate August is hot and humid in Japan, with temperatures often reaching above 30\u00176C (86\u00176F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.\n\n#### Language and Cultural Tips\n- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).\n- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.\n- Dress modestly when visiting temples and shrines.\n- Understand that tipping is not customary and may be considered rude in some situations.\n\nBy being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
<-- 🛠️ HandoffTool[WeatherPlanning][finish]: "### Comprehensive Travel Planning Summary for Japan Trip\n\n#### Destination Information\nFor a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:\n- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.\n- Osaka: Explore Osaka Castle and the Dotonbori area.\n\n#### Weather Expectations\nLate August is hot and humid in Japan, with temperatures often reaching above 30\u00176C (86\u00176F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.\n\n#### Language and Cultural Tips\n- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).\n- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.\n- Dress modestly when visiting temples and shrines.\n- Understand that tipping is not customary and may be considered rude in some situations.\n\nBy being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan."
--> 🛠️ HandoffTool[LanguageCulturalGuidance][start]: {"input": {"input": {"task": "Essential Japanese phrases and cultural etiquette for respectful travel in Tokyo and Osaka"}}}
The agent wants to use the 'LanguageCulturalGuidance tool.'
Input: {'input': {'task': 'Essential Japanese phrases and cultural etiquette for respectful travel in Tokyo and Osaka'}, 'options': None}
Do you allow it? (yes/no): yes
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["LanguageCulturalGuidance"], "thoughts": "To provide essential Japanese phrases and cultural etiquette, I'll need to gather information on language tips and cultural norms for Tokyo and Osaka."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"query": "Japanese culture etiquette", "full_text': false": true}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"query": "Japanese culture", "full_text': false": true}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: [{"title": "Culture of Japan", "description": "Japanese culture has changed greatly over the millennia, from the country's prehistoric Jōmon period, to its contemporary modern culture, which absorbs influences from Asia and other regions of the world.\nSince the Jomon period, ancestral groups like the Yayoi and Kofun, who arrived to Japan from Korea and China, respectively, have shaped Japanese culture. Rice cultivation and centralized leadership were introduced by these groups, shaping Japanese culture. Chinese dynasties, particularly the Tang dynasty, have influenced Japanese culture throughout history and brought it into the Sinosphere. After 220 years of isolation, the Meiji era opened Japan to Western influences, enriching and diversifying Japanese culture. Popular culture shows how much contemporary Japanese culture influences the world.", "url": "https://en.wikipedia.org/wiki/Culture_of_Japan"}]
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "### Essential Japanese Phrases and Cultural Etiquette for Tokyo and Osaka\n\n#### Basic Phrases:\n- **Konnichiwa** (hello)\n- **Arigatou** (thank you)\n- **Sumimasen** (excuse me)\n- **Ohayou gozaimasu** (good morning)\n- **Konbanwa** (good evening)\n\n#### Cultural Etiquette:\n1. **Bowing**: A common greeting in Japan. The depth and duration of the bow indicate respect.\n2. **Dress Modestly**: Especially when visiting temples and shrines. Avoid revealing clothing.\n3. **Tipping Culture**: Not customary and may be considered rude in some situations.\n4. **Respect for Elders**: Show deference to older individuals, as respect for elders is deeply ingrained in Japanese culture.\n5. **Table Manners**: Wait for the host to start eating before you begin. Chopsticks should not be left standing upright in your rice bowl, as this resembles a funeral ritual.\n\nBy learning these phrases and respecting cultural norms, you'll have a more enriching and respectful experience during your cultural immersion trip to Tokyo and Osaka."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
<-- 🛠️ HandoffTool[LanguageCulturalGuidance][finish]: "### Essential Japanese Phrases and Cultural Etiquette for Tokyo and Osaka\n\n#### Basic Phrases:\n- **Konnichiwa** (hello)\n- **Arigatou** (thank you)\n- **Sumimasen** (excuse me)\n- **Ohayou gozaimasu** (good morning)\n- **Konbanwa** (good evening)\n\n#### Cultural Etiquette:\n1. **Bowing**: A common greeting in Japan. The depth and duration of the bow indicate respect.\n2. **Dress Modestly**: Especially when visiting temples and shrines. Avoid revealing clothing.\n3. **Tipping Culture**: Not customary and may be considered rude in some situations.\n4. **Respect for Elders**: Show deference to older individuals, as respect for elders is deeply ingrained in Japanese culture.\n5. **Table Manners**: Wait for the host to start eating before you begin. Chopsticks should not be left standing upright in your rice bowl, as this resembles a funeral ritual.\n\nBy learning these phrases and respecting cultural norms, you'll have a more enriching and respectful experience during your cultural immersion trip to Tokyo and Osaka."
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "### Comprehensive Travel Planning Summary for Japan Trip\n\n#### Destination Information\nFor a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:\n- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.\n- Osaka: Explore Osaka Castle and the Dotonbori area.\n\n#### Weather Expectations\nLate August is hot and humid in Japan, with temperatures often reaching above 30°C (86°F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.\n\n#### Language and Cultural Tips\n- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).\n- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.\n- Dress modestly when visiting temples and shrines.\n- Understand that tipping is not customary and may be considered rude in some situations.\n\nBy being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"

📋 Comprehensive Travel Plan:
### Comprehensive Travel Planning Summary for Japan Trip

#### Destination Information
For a 2-week cultural immersion trip to Tokyo and Osaka, you can expect a rich experience of traditional culture and historical sites. Key destinations include:
- Tokyo: Visit the Meiji Shrine, Senso-ji Temple, and the Imperial Palace.
- Osaka: Explore Osaka Castle and the Dotonbori area.

#### Weather Expectations
Late August is hot and humid in Japan, with temperatures often reaching above 30°C (86°F). Expect occasional rain showers and typhoons. Pack light, breathable clothing and stay hydrated.

#### Language and Cultural Tips
- Learn basic Japanese phrases like 'konnichiwa' (hello), 'arigatou' (thank you), and 'sumimasen' (excuse me).
- Respect for elders and tradition is deeply ingrained; bow upon greeting as a sign of respect.
- Dress modestly when visiting temples and shrines.
- Understand that tipping is not customary and may be considered rude in some situations.

By being mindful of these aspects, you'll be well-prepared for a respectful and enriching cultural immersion experience in Japan.
"""