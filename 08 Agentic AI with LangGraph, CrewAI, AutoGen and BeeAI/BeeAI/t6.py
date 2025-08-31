import asyncio
import logging
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool

async def wikipedia_enhanced_agent_example():
    """
    RequirementAgent with Wikipedia - Research Enhancement and tracking
    
    Adding WikipediaTool provides access to Wikipedia summaries for contextual research.
    Same query - but now with research capability.
    Moreover, middleware is used to track all tool usage.
    """
    llm = ChatModel.from_name("watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", ChatModelParameters(temperature=0))
    
    # SAME SYSTEM PROMPT as Example 1
    SYSTEM_INSTRUCTIONS = """You are an expert cybersecurity analyst specializing in threat assessment and risk analysis.

Your methodology:
1. Analyze the threat landscape systematically
2. Research authoritative sources when available
3. Provide comprehensive risk assessment with actionable recommendations
4. Focus on practical, implementable security measures"""
    
    # RequirementAgent with Wikipedia research capability
    wikipedia_agent = RequirementAgent(
        llm=llm,
        tools=[WikipediaTool()],  # Added research capability
        memory=UnconstrainedMemory(),
        instructions=SYSTEM_INSTRUCTIONS,
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
        requirements=[ConditionalRequirement(WikipediaTool, max_invocations=2)]
    )
    
    # SAME QUERY as Example 1
    ANALYSIS_QUERY = """Analyze the cybersecurity risks of quantum computing for financial institutions. 
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
    
    result = await wikipedia_agent.run(ANALYSIS_QUERY)
    print(f"\n📖 Research-Enhanced Analysis:\n{result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await wikipedia_enhanced_agent_example()

if __name__ == "__main__":
    asyncio.run(main())

"""
Output::

--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"query": "Quantum computing", "full_text:": "false"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: [{"title": "Quantum computing", "description": "A quantum computer is a (real or theoretical) computer that uses quantum mechanical phenomena in an essential way: it exploits superposed and entangled states, and the intrinsically non-deterministic outcomes of quantum measurements, as features of its computation. Quantum computers can be viewed as sampling from quantum systems that evolve in ways classically described as operating on an enormous number of possibilities simultaneously, though still subject to strict computational constraints. By contrast, ordinary (\"classical\") computers operate according to deterministic rules. Any classical computer can, in principle, be replicated by a (classical) mechanical device such as a Turing machine, with only polynomial overhead in time. Quantum computers, on the other hand are believed to require exponentially more resources to simulate classically. It is widely believed that a scalable quantum computer could perform some calculations exponentially faster than any classical computer. Theoretically, a large-scale quantum computer could break some widely used public-key cryptographic schemes and aid physicists in performing physical simulations. However, current hardware implementations of quantum computation are largely experimental and only suitable for specialized tasks.\nThe basic unit of information in quantum computing, the qubit (or \"quantum bit\"), serves the same function as the bit in ordinary or \"classical\" computing. However, unlike a classical bit, which can be in one of two states (a binary), a qubit can exist in a superposition of its two \"basis\" states, a state that is in an abstract sense \"between\" the two basis states. When measuring a qubit, the result is a probabilistic output of a classical bit. If a quantum computer manipulates the qubit in a particular way, wave interference effects can amplify the desired measurement results. The design of quantum algorithms involves creating procedures that allow a quantum computer to perform calculations efficiently and quickly.\nQuantum computers are not yet practical for real-world applications. Physically engineering high-quality qubits has proven to be challenging. If a physical qubit is not sufficiently isolated from its environment, it suffers from quantum decoherence, introducing noise into calculations. National governments have invested heavily in experimental research aimed at developing scalable qubits with longer coherence times and lower error rates. Example implementations include superconductors (which isolate an electrical current by eliminating electrical resistance) and ion traps (which confine a single atomic particle using electromagnetic fields).  Researchers have claimed, and are widely believed to be correct, that certain quantum devices can outperform classical computers on narrowly defined tasks, a milestone referred to as quantum advantage or quantum supremacy. These tasks are not necessarily useful for real-world applications.", "url": "https://en.wikipedia.org/wiki/Quantum_computing"}]
--> 🛠️ WikipediaTool[Wikipedia][start]: {"input": {"input": {"query": "Post-quantum cryptography", "full_text:": "false"}}}
<-- 🛠️ WikipediaTool[Wikipedia][finish]: [{"title": "Post-quantum cryptography", "description": "Post-quantum cryptography (PQC), sometimes referred to as quantum-proof, quantum-safe, or quantum-resistant, is the development of cryptographic algorithms (usually public-key algorithms) that are currently thought to be secure against a cryptanalytic attack by a quantum computer. Most widely used public-key algorithms rely on the difficulty of one of three mathematical problems: the integer factorization problem, the discrete logarithm problem or the elliptic-curve discrete logarithm problem. All of these problems could be easily solved on a sufficiently powerful quantum computer running Shor's algorithm or possibly alternatives.\nAs of 2025, quantum computers lack the processing power to break widely used cryptographic algorithms; however, because of the length of time required for migration to quantum-safe cryptography, cryptographers are already designing new algorithms to prepare for Y2Q or Q-Day, the day when current algorithms will be vulnerable to quantum computing attacks. Mosca's theorem provides the risk analysis framework that helps organizations identify how quickly they need to start migrating.\nTheir work has gained attention from academics and industry through the PQCrypto conference series hosted since 2006, several workshops on Quantum Safe Cryptography hosted by the European Telecommunications Standards Institute (ETSI), and the Institute for Quantum Computing. The rumoured existence of widespread harvest now, decrypt later programs has also been seen as a motivation for the early introduction of post-quantum algorithms, as data recorded now may still remain sensitive many years into the future.\nIn contrast to the threat quantum computing poses to current public-key algorithms, most current symmetric cryptographic algorithms and hash functions are considered to be relatively secure against attacks by quantum computers. While the quantum Grover's algorithm does speed up attacks against symmetric ciphers, doubling the key size can effectively counteract these attacks. Thus post-quantum symmetric cryptography does not need to differ significantly from current symmetric cryptography.\nIn 2024, the U.S. National Institute of Standards and Technology (NIST) released final versions of its first three Post-Quantum Cryptography Standards.", "url": "https://en.wikipedia.org/wiki/Post-quantum_cryptography"}]
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "## Cybersecurity Risks of Quantum Computing for Financial Institutions\n\n### Main Threats\n1. **Cryptography Breakage**: Quantum computers can potentially break certain classical encryption algorithms currently used to secure financial transactions and data. This is because quantum computers can efficiently solve problems like factoring large numbers (RSA) and discrete logarithms (elliptic curve cryptography), which are the basis for many cryptographic systems.\n2. **Data Confidentiality and Integrity**: If a sufficiently powerful quantum computer were to be built, it could potentially decrypt sensitive financial data that was encrypted with vulnerable algorithms, compromising confidentiality and integrity.\n\n### Timeline for Concern\n- **Short-term (2025-2030)**: The immediate risk is not the existence of quantum computers capable of breaking cryptography but rather the \"harvest now, decrypt later\" threat. Attackers could store encrypted data now and wait for a sufficiently powerful quantum computer to decrypt it in the future.\n- **Mid-term (2030-2040)**: As quantum computing technology advances, the risk of a practical quantum computer being used for malicious purposes increases. Financial institutions need to be prepared to migrate to quantum-safe cryptography before this happens.\n\n### Recommended Preparation Strategies\n1. **Inventory and Assessment**: Identify all cryptographic assets and assess their vulnerability to quantum attacks.\n2. **Migration to Post-Quantum Cryptography**: Begin migrating to cryptographic algorithms and protocols that are resistant to quantum attacks. The U.S. National Institute of Standards and Technology (NIST) has been leading efforts to standardize post-quantum cryptographic algorithms.\n3. **Hybrid Solutions**: Implement hybrid cryptographic solutions that combine classical and post-quantum cryptography to ensure security both now and in the future.\n4. **Stay Informed**: Keep up-to-date with the latest developments in quantum computing and post-quantum cryptography. Participate in industry forums and follow updates from standards organizations like NIST.\n5. **Quantum-Safe Communication**: For sensitive communications, consider implementing quantum-safe key exchange and encryption methods.\n\n### Actionable Recommendations\n- **Monitor Quantum Computing Advancements**: Regularly assess the current state of quantum computing capabilities.\n- **Develop a Migration Plan**: Create a roadmap for transitioning to post-quantum cryptography, prioritizing critical systems and data.\n- **Implement Quantum-Resistant Algorithms**: Start integrating quantum-resistant cryptographic algorithms into your systems, following guidelines from reputable sources like NIST.\n- **Educate and Train**: Ensure that your cybersecurity team is aware of the risks and prepared to implement post-quantum cryptographic solutions.\n\nBy taking proactive steps now, financial institutions can mitigate the risks posed by quantum computing and ensure the long-term security of their data and transactions."}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"

📖 Research-Enhanced Analysis:
## Cybersecurity Risks of Quantum Computing for Financial Institutions

### Main Threats
1. **Cryptography Breakage**: Quantum computers can potentially break certain classical encryption algorithms currently used to secure financial transactions and data. This is because quantum computers can efficiently solve problems like factoring large numbers (RSA) and discrete logarithms (elliptic curve cryptography), which are the basis for many cryptographic systems.
2. **Data Confidentiality and Integrity**: If a sufficiently powerful quantum computer were to be built, it could potentially decrypt sensitive financial data that was encrypted with vulnerable algorithms, compromising confidentiality and integrity.

### Timeline for Concern
- **Short-term (2025-2030)**: The immediate risk is not the existence of quantum computers capable of breaking cryptography but rather the "harvest now, decrypt later" threat. Attackers could store encrypted data now and wait for a sufficiently powerful quantum computer to decrypt it in the future.
- **Mid-term (2030-2040)**: As quantum computing technology advances, the risk of a practical quantum computer being used for malicious purposes increases. Financial institutions need to be prepared to migrate to quantum-safe cryptography before this happens.

### Recommended Preparation Strategies
1. **Inventory and Assessment**: Identify all cryptographic assets and assess their vulnerability to quantum attacks.
2. **Migration to Post-Quantum Cryptography**: Begin migrating to cryptographic algorithms and protocols that are resistant to quantum attacks. The U.S. National Institute of Standards and Technology (NIST) has been leading efforts to standardize post-quantum cryptographic algorithms.
3. **Hybrid Solutions**: Implement hybrid cryptographic solutions that combine classical and post-quantum cryptography to ensure security both now and in the future.
4. **Stay Informed**: Keep up-to-date with the latest developments in quantum computing and post-quantum cryptography. Participate in industry forums and follow updates from standards organizations like NIST.
5. **Quantum-Safe Communication**: For sensitive communications, consider implementing quantum-safe key exchange and encryption methods.

### Actionable Recommendations
- **Monitor Quantum Computing Advancements**: Regularly assess the current state of quantum computing capabilities.
- **Develop a Migration Plan**: Create a roadmap for transitioning to post-quantum cryptography, prioritizing critical systems and data.
- **Implement Quantum-Resistant Algorithms**: Start integrating quantum-resistant cryptographic algorithms into your systems, following guidelines from reputable sources like NIST.
- **Educate and Train**: Ensure that your cybersecurity team is aware of the risks and prepared to implement post-quantum cryptographic solutions.

By taking proactive steps now, financial institutions can mitigate the risks posed by quantum computing and ensure the long-term security of their data and transactions.
"""