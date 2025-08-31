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
    """
    RequirementAgent with Systematic Reasoning - ThinkTool + WikipediaTool
    
    Adding ThinkTool enables structured reasoning alongside research.
    Same query, same tracking - now with visible thinking process.
    """
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
            ConditionalRequirement(ThinkTool, max_invocations=2),
            ConditionalRequirement(WikipediaTool, max_invocations=2)
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

--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["Wikipedia"], "thoughts": "To analyze the cybersecurity risks of quantum computing for financial institutions, I need to understand the current state of quantum computing and its potential impact on cryptography. I'll start by searching for information on quantum computing and its risks."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Quantum computing risks to cryptography"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: []
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"full_text": false, "query": "Quantum computing"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: [{"title": "Quantum computing", "description": "A quantum computer is a (real or theoretical) computer that uses quantum mechanical phenomena in an essential way: it exploits superposed and entangled states, and the intrinsically non-deterministic outcomes of quantum measurements, as features of its computation. Quantum computers can be viewed as sampling from quantum systems that evolve in ways classically described as operating on an enormous number of possibilities simultaneously, though still subject to strict computational constraints. By contrast, ordinary (\"classical\") computers operate according to deterministic rules. Any classical computer can, in principle, be replicated by a (classical) mechanical device such as a Turing machine, with only polynomial overhead in time. Quantum computers, on the other hand are believed to require exponentially more resources to simulate classically. It is widely believed that a scalable quantum computer could perform some calculations exponentially faster than any classical computer. Theoretically, a large-scale quantum computer could break some widely used public-key cryptographic schemes and aid physicists in performing physical simulations. However, current hardware implementations of quantum computation are largely experimental and only suitable for specialized tasks.\nThe basic unit of information in quantum computing, the qubit (or \"quantum bit\"), serves the same function as the bit in ordinary or \"classical\" computing. However, unlike a classical bit, which can be in one of two states (a binary), a qubit can exist in a superposition of its two \"basis\" states, a state that is in an abstract sense \"between\" the two basis states. When measuring a qubit, the result is a probabilistic output of a classical bit. If a quantum computer manipulates the qubit in a particular way, wave interference effects can amplify the desired measurement results. The design of quantum algorithms involves creating procedures that allow a quantum computer to perform calculations efficiently and quickly.\nQuantum computers are not yet practical for real-world applications. Physically engineering high-quality qubits has proven to be challenging. If a physical qubit is not sufficiently isolated from its environment, it suffers from quantum decoherence, introducing noise into calculations. National governments have invested heavily in experimental research aimed at developing scalable qubits with longer coherence times and lower error rates. Example implementations include superconductors (which isolate an electrical current by eliminating electrical resistance) and ion traps (which confine a single atomic particle using electromagnetic fields).  Researchers have claimed, and are widely believed to be correct, that certain quantum devices can outperform classical computers on narrowly defined tasks, a milestone referred to as quantum advantage or quantum supremacy. These tasks are not necessarily useful for real-world applications.", "url": "https://en.wikipedia.org/wiki/Quantum_computing"}]
--> 🛠️ ThinkTool[think][start]: {"input": {"input": {"next_step": ["final_answer"], "thoughts": "Quantum computing poses a significant risk to financial institutions due to its potential to break certain cryptographic schemes. The main threats include the potential for quantum computers to factor large numbers exponentially faster than classical computers, thereby breaking RSA and elliptic curve cryptography. This could compromise the security of financial transactions and data. The timeline for concern is generally considered to be within the next 5-10 years, as significant advancements are being made in quantum computing hardware. Recommended preparation strategies include implementing quantum-resistant cryptographic algorithms, such as lattice-based cryptography, and developing a migration plan for existing cryptographic systems."}}}
<-- 🛠️ ThinkTool[think][finish]: "OK"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Breakage**: Quantum computers can potentially break certain public-key cryptographic schemes, such as RSA and elliptic curve cryptography, by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.\n2. **Key Exchange and Digital Signatures**: Quantum computers can also break certain key exchange and digital signature schemes, potentially allowing attackers to intercept and alter sensitive information.\n\n### Timeline for Concern\nThe timeline for concern is generally considered to be within the next 5-10 years, as significant advancements are being made in quantum computing hardware. It is expected that a large-scale quantum computer will be capable of breaking RSA-2048 by 2030.\n\n### Recommended Preparation Strategies\n1. **Implement Quantum-Resistant Cryptographic Algorithms**: Financial institutions should consider implementing quantum-resistant cryptographic algorithms, such as lattice-based cryptography, hash-based signatures, and code-based cryptography.\n2. **Develop a Migration Plan**: Develop a migration plan for existing cryptographic systems to quantum-resistant cryptography.\n3. **Monitor Quantum Computing Advancements**: Continuously monitor advancements in quantum computing and assess the potential risks to their cryptographic systems.\n4. **Diversify Cryptographic Algorithms**: Consider diversifying cryptographic algorithms to reduce dependence on a single algorithm or type of algorithm.\n5. **Collaborate with Industry and Regulatory Bodies**: Collaborate with industry and regulatory bodies to stay informed about the latest developments and recommendations for quantum-resistant cryptography.\n\nBy taking proactive steps to prepare for the potential risks of quantum computing, financial institutions can reduce their exposure to these risks and ensure the long-term security of their systems and data.", "name": "final_answer", "parameters": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Breakage**: Quantum computers can potentially break certain public-key cryptographic schemes, such as RSA and elliptic curve cryptography, by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.\n2. **Key Exchange and Digital Signatures**: Quantum computers can also break certain key exchange and digital signature schemes, potentially allowing attackers to intercept and alter sensitive information.\n\n### Timeline for Concern\nThe timeline for concern is generally considered to be within the next 5-10 years, as significant advancements are being made in quantum computing hardware. It is expected that a large-scale quantum computer will be capable of breaking RSA-2048 by 2030.\n\n### Recommended Preparation Strategies\n1. **Implement Quantum-Resistant Cryptographic Algorithms**: Financial institutions should consider implementing quantum-resistant cryptographic algorithms, such as lattice-based cryptography, hash-based signatures, and code-based cryptography.\n2. **Develop a Migration Plan**: Develop a migration plan for existing cryptographic systems to quantum-resistant cryptography.\n3. **Monitor Quantum Computing Advancements**: Continuously monitor advancements in quantum computing and assess the potential risks to their cryptographic systems.\n4. **Diversify Cryptographic Algorithms**: Consider diversifying cryptographic algorithms to reduce dependence on a single algorithm or type of algorithm.\n5. **Collaborate with Industry and Regulatory Bodies**: Collaborate with industry and regulatory bodies to stay informed about the latest developments and recommendations for quantum-resistant cryptography.\n\nBy taking proactive steps to prepare for the potential risks of quantum computing, financial institutions can reduce their exposure to these risks and ensure the long-term security of their systems and data."}}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"

🧠 Reasoning + Research Analysis:
## Cybersecurity Risks of Quantum Computing for Financial Institutions

### Main Threats
1. **Cryptography Breakage**: Quantum computers can potentially break certain public-key cryptographic schemes, such as RSA and elliptic curve cryptography, by factoring large numbers exponentially faster than classical computers. This could compromise the security of financial transactions and data.
2. **Key Exchange and Digital Signatures**: Quantum computers can also break certain key exchange and digital signature schemes, potentially allowing attackers to intercept and alter sensitive information.

### Timeline for Concern
The timeline for concern is generally considered to be within the next 5-10 years, as significant advancements are being made in quantum computing hardware. It is expected that a large-scale quantum computer will be capable of breaking RSA-2048 by 2030.

### Recommended Preparation Strategies
1. **Implement Quantum-Resistant Cryptographic Algorithms**: Financial institutions should consider implementing quantum-resistant cryptographic algorithms, such as lattice-based cryptography, hash-based signatures, and code-based cryptography.
2. **Develop a Migration Plan**: Develop a migration plan for existing cryptographic systems to quantum-resistant cryptography.
3. **Monitor Quantum Computing Advancements**: Continuously monitor advancements in quantum computing and assess the potential risks to their cryptographic systems.
4. **Diversify Cryptographic Algorithms**: Consider diversifying cryptographic algorithms to reduce dependence on a single algorithm or type of algorithm.
5. **Collaborate with Industry and Regulatory Bodies**: Collaborate with industry and regulatory bodies to stay informed about the latest developments and recommendations for quantum-resistant cryptography.

By taking proactive steps to prepare for the potential risks of quantum computing, financial institutions can reduce their exposure to these risks and ensure the long-term security of their systems and data.
"""