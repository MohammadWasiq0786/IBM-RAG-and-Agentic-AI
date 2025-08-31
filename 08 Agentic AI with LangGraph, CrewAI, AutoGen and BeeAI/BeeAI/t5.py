import asyncio
import logging
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters

async def minimal_tracked_agent_example():
    """
    Minimal RequirementAgent
    """
    llm = ChatModel.from_name("watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", ChatModelParameters(temperature=0))
    
    # CONSISTENT SYSTEM PROMPT (used in all examples)
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

Your methodology:
1. Analyze the threat landscape systematically
2. Research authoritative sources when available
3. Provide comprehensive risk assessment with actionable recommendations
4. Focus on practical, implementable security measures"""

    # Minimal RequirementAgent
    minimal_agent = RequirementAgent(
        llm=llm,
        tools=[],  # No tools yet
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS
    )
    
    # CONSISTENT QUERY (used in all examples)
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await minimal_agent.run(ANALYSIS_QUERY)
    print(f"\n💬 Pure LLM Analysis:\n{result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await minimal_tracked_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

"""
Output::

💬 Pure LLM Analysis:
## Cybersecurity Risks of Quantum Computing for Financial Institutions

### Main Threats
1. **Cryptography Breakage**: Quantum computers can potentially break certain classical encryption algorithms currently used to secure financial transactions and data. This is particularly concerning for algorithms like RSA and elliptic curve cryptography.
2. **Key Exchange and Digital Signatures**: Quantum computers can compromise key exchange protocols and digital signatures, which are crucial for secure communication and authentication in financial institutions.

### Timeline for Concern
- **Short-term (2025-2030)**: The immediate risk is not the direct attack on cryptography but rather the "harvest now, decrypt later" strategy, where encrypted data is stolen now and decrypted when a sufficiently powerful quantum computer becomes available.
- **Mid-term (2030-2040)**: Expect significant advancements in quantum computing, potentially leading to the ability to break certain cryptographic algorithms.
- **Long-term (2040+)**: Widespread adoption of quantum-resistant cryptography is expected, but the transition period will be critical.

### Recommended Preparation Strategies
1. **Inventory and Assessment**: Identify and assess all cryptographic assets and their usage within the institution.
2. **Migration to Quantum-Resistant Cryptography**: Begin transitioning to quantum-resistant cryptographic algorithms and protocols, such as those based on lattice problems or hash-based signatures.
3. **Hybrid Solutions**: Implement hybrid solutions that combine classical and quantum-resistant cryptography to ensure security against both classical and quantum attacks.
4. **Monitoring and Adaptation**: Continuously monitor advancements in quantum computing and adjust strategies accordingly.
5. **Collaboration and Standards**: Engage with industry standards bodies and collaborate with other financial institutions to ensure a coordinated response to the quantum threat.

### Conclusion
Financial institutions must proactively address the cybersecurity risks posed by quantum computing. By understanding the threats, anticipating the timeline for concern, and implementing recommended preparation strategies, institutions can mitigate potential risks and ensure the security of their data and transactions.
"""