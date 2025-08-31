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

async def controlled_execution_example():
    """
    RequirementAgent with Controlled Execution - Requirements System
    
    Requirements provide precise control over tool execution order and behavior.
    Same query, same tracking - but now with strict execution rules.
    """
    llm = ChatModel.from_name("watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", ChatModelParameters(temperature=0))
    
    # SAME SYSTEM PROMPT as previous examples
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

Your methodology:
1. Analyze the threat landscape systematically
2. Research authoritative sources when available
3. Provide comprehensive risk assessment with actionable recommendations
4. Focus on practical, implementable security measures"""
    
    # RequirementAgent with strict execution control
    controlled_agent = RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), WikipediaTool()],
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        
        # REQUIREMENTS: Declarative control over execution flow
        requirements=[
            # MUST start with systematic thinking
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,  # Thinking required first
                min_invocations=1,  # At least once
                max_invocations=3,  # Max number of invocations
                consecutive_allowed=False  # No repeated thinking
            ),
            # Wikipedia research only after thinking
            ConditionalRequirement(
                WikipediaTool,
                only_after=[ThinkTool],  # Only after thinking
                min_invocations=1,  # Must research at least once
                max_invocations=2  # Max number of research calls
            )
        ]
    )
    
    # SAME QUERY as all previous examples
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await controlled_agent.run(ANALYSIS_QUERY)
    print(f"\n🔧 Controlled Execution Analysis:\n{result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await controlled_execution_example()

if __name__ == "__main__":
    asyncio.run(main())

"""
Output::

--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Wikipedia"], "thoughts": "To analyze the cybersecurity risks of quantum computing for financial institutions, I need to understand the current state of quantum computing, its potential threats, and the timeline for when these threats might become relevant. I will start by searching for information on quantum computing and its impact on cybersecurity."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Quantum computing cybersecurity risks financial institutions"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Quantum computing"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: [{"title": "Quantum computing", "description": "A quantum computer is a (real or theoretical) computer that uses quantum mechanical phenomena in an essential way: it exploits superposed and entangled states, and the intrinsically non-deterministic outcomes of quantum measurements, as features of its computation. Quantum computers can be viewed as sampling from quantum systems that evolve in ways classically described as operating on an enormous number of possibilities simultaneously, though still subject to strict computational constraints. By contrast, ordinary (\"classical\") computers operate according to deterministic rules. Any classical computer can, in principle, be replicated by a (classical) mechanical device such as a Turing machine, with only polynomial overhead in time. Quantum computers, on the other hand are believed to require exponentially more resources to simulate classically. It is widely believed that a scalable quantum computer could perform some calculations exponentially faster than any classical computer. Theoretically, a large-scale quantum computer could break some widely used public-key cryptographic schemes and aid physicists in performing physical simulations. However, current hardware implementations of quantum computation are largely experimental and only suitable for specialized tasks.\nThe basic unit of information in quantum computing, the qubit (or \"quantum bit\"), serves the same function as the bit in ordinary or \"classical\" computing. However, unlike a classical bit, which can be in one of two states (a binary), a qubit can exist in a superposition of its two \"basis\" states, a state that is in an abstract sense \"between\" the two basis states. When measuring a qubit, the result is a probabilistic output of a classical bit. If a quantum computer manipulates the qubit in a particular way, wave interference effects can amplify the desired measurement results. The design of quantum algorithms involves creating procedures that allow a quantum computer to perform calculations efficiently and quickly.\nQuantum computers are not yet practical for real-world applications. Physically engineering high-quality qubits has proven to be challenging. If a physical qubit is not sufficiently isolated from its environment, it suffers from quantum decoherence, introducing noise into calculations. National governments have invested heavily in experimental research aimed at developing scalable qubits with longer coherence times and lower error rates. Example implementations include superconductors (which isolate an electrical current by eliminating electrical resistance) and ion traps (which confine a single atomic particle using electromagnetic fields).  Researchers have claimed, and are widely believed to be correct, that certain quantum devices can outperform classical computers on narrowly defined tasks, a milestone referred to as quantum advantage or quantum supremacy. These tasks are not necessarily useful for real-world applications.", "url": "https://en.wikipedia.org/wiki/Quantum_computing"}]
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["final_answer"], "thoughts": "Quantum computing poses a significant risk to financial institutions due to its potential to break certain cryptographic schemes. The main threats include the ability of quantum computers to factor large numbers exponentially faster than classical computers, which could compromise public-key cryptography. The timeline for concern is tied to the development of practical, large-scale quantum computers. Preparation strategies include transitioning to quantum-resistant cryptographic algorithms and protocols."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Compromise**: Quantum computers can potentially break certain public-key cryptographic algorithms (e.g., RSA, ECC) by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.\n2. **Key Exchange and Digital Signatures**: Quantum computers can break certain key exchange protocols and digital signature schemes, undermining the integrity and authenticity of financial communications.\n\n### Timeline for Concern\n- **Short-term (5-10 years)**: Expect significant advancements in quantum computing, but large-scale, practical quantum computers are still in development.\n- **Mid-term (10-20 years)**: As quantum technology matures, the risk to current cryptographic systems will increase. Financial institutions should begin preparing for a post-quantum cryptography world.\n\n### Recommended Preparation Strategies\n1. **Quantum-Resistant Cryptography**: Transition to cryptographic algorithms and protocols resistant to quantum attacks, such as:\n   - Lattice-based cryptography\n   - Code-based cryptography\n   - Hash-based signatures\n   - Multivariate cryptography\n2. **Hybrid Solutions**: Implement hybrid cryptographic solutions that combine classical and quantum-resistant algorithms to ensure security against both classical and quantum threats.\n3. **Monitoring and Adaptation**: Continuously monitor advancements in quantum computing and post-quantum cryptography. Be prepared to adapt security measures as new standards and technologies emerge.\n4. **Collaboration and Standards**: Engage with industry consortia, regulatory bodies, and standards organizations to stay informed about best practices and evolving standards for quantum-safe cryptography.\n5. **Inventory and Assessment**: Conduct an inventory of cryptographic assets and assess their vulnerability to quantum attacks. Prioritize the migration of critical systems to quantum-resistant cryptography.\n\nBy understanding the risks and proactively preparing for the advent of quantum computing, financial institutions can mitigate potential cybersecurity threats and ensure the long-term security of their operations.", "name": "final_answer", "parameters": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Compromise**: Quantum computers can potentially break certain public-key cryptographic algorithms (e.g., RSA, ECC) by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.\n2. **Key Exchange and Digital Signatures**: Quantum computers can break certain key exchange protocols and digital signature schemes, undermining the integrity and authenticity of financial communications.\n\n### Timeline for Concern\n- **Short-term (5-10 years)**: Expect significant advancements in quantum computing, but large-scale, practical quantum computers are still in development.\n- **Mid-term (10-20 years)**: As quantum technology matures, the risk to current cryptographic systems will increase. Financial institutions should begin preparing for a post-quantum cryptography world.\n\n### Recommended Preparation Strategies\n1. **Quantum-Resistant Cryptography**: Transition to cryptographic algorithms and protocols resistant to quantum attacks, such as:\n   - Lattice-based cryptography\n   - Code-based cryptography\n   - Hash-based signatures\n   - Multivariate cryptography\n2. **Hybrid Solutions**: Implement hybrid cryptographic solutions that combine classical and quantum-resistant algorithms to ensure security against both classical and quantum threats.\n3. **Monitoring and Adaptation**: Continuously monitor advancements in quantum computing and post-quantum cryptography. Be prepared to adapt security measures as new standards and technologies emerge.\n4. **Collaboration and Standards**: Engage with industry consortia, regulatory bodies, and standards organizations to stay informed about best practices and evolving standards for quantum-safe cryptography.\n5. **Inventory and Assessment**: Conduct an inventory of cryptographic assets and assess their vulnerability to quantum attacks. Prioritize the migration of critical systems to quantum-resistant cryptography.\n\nBy understanding the risks and proactively preparing for the advent of quantum computing, financial institutions can mitigate potential cybersecurity threats and ensure the long-term security of their operations."}}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"

🔧 Controlled Execution Analysis:
## Cybersecurity Risks of Quantum Computing for Financial Institutions

### Main Threats
1. **Cryptography Compromise**: Quantum computers can potentially break certain public-key cryptographic algorithms (e.g., RSA, ECC) by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.
2. **Key Exchange and Digital Signatures**: Quantum computers can break certain key exchange protocols and digital signature schemes, undermining the integrity and authenticity of financial communications.

### Timeline for Concern
- **Short-term (5-10 years)**: Expect significant advancements in quantum computing, but large-scale, practical quantum computers are still in development.
- **Mid-term (10-20 years)**: As quantum technology matures, the risk to current cryptographic systems will increase. Financial institutions should begin preparing for a post-quantum cryptography world.

### Recommended Preparation Strategies
1. **Quantum-Resistant Cryptography**: Transition to cryptographic algorithms and protocols resistant to quantum attacks, such as:
   - Lattice-based cryptography
   - Code-based cryptography
   - Hash-based signatures
   - Multivariate cryptography
2. **Hybrid Solutions**: Implement hybrid cryptographic solutions that combine classical and quantum-resistant algorithms to ensure security against both classical and quantum threats.
3. **Monitoring and Adaptation**: Continuously monitor advancements in quantum computing and post-quantum cryptography. Be prepared to adapt security measures as new standards and technologies emerge.
4. **Collaboration and Standards**: Engage with industry consortia, regulatory bodies, and standards organizations to stay informed about best practices and evolving standards for quantum-safe cryptography.
5. **Inventory and Assessment**: Conduct an inventory of cryptographic assets and assess their vulnerability to quantum attacks. Prioritize the migration of critical systems to quantum-resistant cryptography.

By understanding the risks and proactively preparing for the advent of quantum computing, financial institutions can mitigate potential cybersecurity threats and ensure the long-term security of their operations.

"""