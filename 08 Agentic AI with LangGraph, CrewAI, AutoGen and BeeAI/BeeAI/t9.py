import asyncio
import logging
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool

async def reasoning_enhanced_agent_example():
    llm = ChatModel.from_name("watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", ChatModelParameters(temperature=0))
    
    # SAME SYSTEM PROMPT as previous examples
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

Your methodology:
1. Analyze the threat landscape systematically
2. Research authoritative sources when available
3. Provide comprehensive risk assessment with actionable recommendations
4. Focus on practical, implementable security measures"""
    
    # RequirementAgent with reasoning + research capability
    reasoning_agent = RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), WikipediaTool()],  # Thinking + Research
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,  # Thinking required first
                force_after=Tool,  # Force reasoning after every tool call
                min_invocations=1,  # At least once
                max_invocations=5,  # Max number of invocations
                consecutive_allowed=False  # No repeated thinking
            ),
            #ConditionalRequirement(WikipediaTool, max_invocations=2)
        ]
    )
    
    # SAME QUERY as previous examples
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await reasoning_agent.run(ANALYSIS_QUERY)
    print(f"\n🧠 Reasoning + Research Analysis:\n{result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await reasoning_enhanced_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

"""
Output::

--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Wikipedia"], "thoughts": "To analyze the cybersecurity risks of quantum computing for financial institutions, I need to understand the current state of quantum computing, its potential threats to current cryptographic systems, and the timeline for when these threats might become relevant. I will start by searching for information on quantum computing and its impact on cryptography."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": true, "query": "quantum computing impact on cryptography"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["final_answer"], "thoughts": "Since I cannot directly access external information, I will rely on my existing knowledge to provide an analysis of the cybersecurity risks of quantum computing for financial institutions, including the main threats, timeline for concern, and recommended preparation strategies."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Vulnerability**: Quantum computers can potentially break certain classical encryption algorithms currently in use, such as RSA and elliptic curve cryptography, by solving complex mathematical problems more efficiently. This could compromise the confidentiality and integrity of financial data.\n2. **Key Exchange and Digital Signatures**: Quantum computers can potentially break certain key exchange protocols and digital signature schemes, threatening the security of financial transactions and communications.\n\n### Timeline for Concern\n- **Short-term (0-5 years)**: The immediate risk is low as large-scale, error-corrected quantum computers are not yet available. However, the threat is real and growing.\n- **Mid-term (5-10 years)**: As quantum computing technology advances, the risk increases. Financial institutions should begin preparing for a post-quantum cryptography world.\n- **Long-term (10+ years)**: Widespread adoption of quantum computers could render current cryptographic systems obsolete, necessitating a comprehensive migration to quantum-resistant cryptography.\n\n### Recommended Preparation Strategies\n1. **Monitor Quantum Computing Advancements**: Keep abreast of developments in quantum computing and assess their potential impact on your institution's cybersecurity.\n2. **Inventory and Assess Cryptographic Assets**: Identify where and how cryptographic techniques are used within your organization.\n3. **Adopt Quantum-Resistant Cryptography**: Begin transitioning to cryptographic algorithms and protocols that are resistant to quantum attacks, such as lattice-based cryptography, hash-based signatures, and code-based cryptography.\n4. **Implement Hybrid Solutions**: Use hybrid cryptographic solutions that combine classical and quantum-resistant algorithms to ensure security against both classical and quantum threats.\n5. **Collaborate and Stay Informed**: Engage with industry groups, regulatory bodies, and cybersecurity communities to stay updated on best practices and guidelines for quantum-safe cryptography.\n6. **Develop a Migration Plan**: Create a strategic plan to migrate to quantum-resistant cryptography, including timelines, resource allocation, and testing protocols.\n\nBy understanding the threats posed by quantum computing and proactively preparing for them, financial institutions can mitigate the risks and ensure the long-term security of their data and transactions."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"

🧠 Reasoning + Research Analysis:
## Cybersecurity Risks of Quantum Computing for Financial Institutions

### Main Threats
1. **Cryptography Vulnerability**: Quantum computers can potentially break certain classical encryption algorithms currently in use, such as RSA and elliptic curve cryptography, by solving complex mathematical problems more efficiently. This could compromise the confidentiality and integrity of financial data.
2. **Key Exchange and Digital Signatures**: Quantum computers can potentially break certain key exchange protocols and digital signature schemes, threatening the security of financial transactions and communications.

### Timeline for Concern
- **Short-term (0-5 years)**: The immediate risk is low as large-scale, error-corrected quantum computers are not yet available. However, the threat is real and growing.
- **Mid-term (5-10 years)**: As quantum computing technology advances, the risk increases. Financial institutions should begin preparing for a post-quantum cryptography world.
- **Long-term (10+ years)**: Widespread adoption of quantum computers could render current cryptographic systems obsolete, necessitating a comprehensive migration to quantum-resistant cryptography.

### Recommended Preparation Strategies
1. **Monitor Quantum Computing Advancements**: Keep abreast of developments in quantum computing and assess their potential impact on your institution's cybersecurity.
2. **Inventory and Assess Cryptographic Assets**: Identify where and how cryptographic techniques are used within your organization.
3. **Adopt Quantum-Resistant Cryptography**: Begin transitioning to cryptographic algorithms and protocols that are resistant to quantum attacks, such as lattice-based cryptography, hash-based signatures, and code-based cryptography.
4. **Implement Hybrid Solutions**: Use hybrid cryptographic solutions that combine classical and quantum-resistant algorithms to ensure security against both classical and quantum threats.
5. **Collaborate and Stay Informed**: Engage with industry groups, regulatory bodies, and cybersecurity communities to stay updated on best practices and guidelines for quantum-safe cryptography.
6. **Develop a Migration Plan**: Create a strategic plan to migrate to quantum-resistant cryptography, including timelines, resource allocation, and testing protocols.

By understanding the threats posed by quantum computing and proactively preparing for them, financial institutions can mitigate the risks and ensure the long-term security of their data and transactions.

"""