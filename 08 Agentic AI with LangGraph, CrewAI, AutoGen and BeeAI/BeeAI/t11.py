import asyncio
import logging
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools import StringToolOutput, Tool, ToolRunOptions
from beeai_framework.context import RunContext
from beeai_framework.emitter import Emitter
from beeai_framework.backend import ChatModel, ChatModelParameters
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from pydantic import BaseModel, Field
from typing import Any

# === REAL TOOL CREATION WITH OFFICIAL BEEAI TOOLS ===

class CalculatorInput(BaseModel):
    """Input model for basic mathematical calculations."""
    expression: str = Field(description="Mathematical expression using +, -, *, / (e.g., '10 + 5', '20 - 8', '4 * 6', '15 / 3')")

class SimpleCalculatorTool(Tool[CalculatorInput, ToolRunOptions, StringToolOutput]):
    """A simple calculator tool for basic arithmetic operations: add, subtract, multiply, divide."""
    name = "SimpleCalculator"
    description = "Performs basic arithmetic calculations: addition (+), subtraction (-), multiplication (*), and division (/)."
    input_schema = CalculatorInput

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        super().__init__(options)

    def _create_emitter(self) -> Emitter:
        return Emitter.root().child(
            namespace=["tool", "calculator", "basic"],
            creator=self,
        )

    def _safe_calculate(self, expression: str) -> float:
        """Safely evaluate basic arithmetic expressions."""
        # Remove spaces for processing
        expr = expression.replace(' ', '')
        
        # Only allow numbers, basic operators, parentheses, and decimal points
        allowed_chars = set('0123456789+-*/().')
        if not all(c in allowed_chars for c in expr):
            raise ValueError("Only numbers and basic operators (+, -, *, /, parentheses) are allowed")
        
        try:
            # Use eval with restricted environment for basic arithmetic only
            result = eval(expr, {"__builtins__": {}}, {})
            return float(result)
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed")
        except Exception as e:
            raise ValueError(f"Invalid arithmetic expression: {str(e)}")

    async def _run(
        self, input: CalculatorInput, options: ToolRunOptions | None, context: RunContext
    ) -> StringToolOutput:
        """Perform basic arithmetic calculations."""
        try:
            expression = input.expression.strip()
            
            # Perform calculation
            result = self._safe_calculate(expression)
            
            # Format result
            output = f"🧮 Simple Calculator\n"
            output += f"Expression: {expression}\n"
            output += f"Result: {result}\n"
            
            # Add operation type hint
            if '+' in expression:
                output += "Operation: Addition"
            elif '-' in expression:
                output += "Operation: Subtraction"
            elif '*' in expression:
                output += "Operation: Multiplication"
            elif '/' in expression:
                output += "Operation: Division"
            else:
                output += "Operation: Basic Arithmetic"
            
            return StringToolOutput(output)
            
        except ValueError as e:
            return StringToolOutput(f"❌ Calculation Error: {str(e)}")
        except Exception as e:
            return StringToolOutput(f"❌ Unexpected Error: {str(e)}")

async def calculator_agent_example():
    """RequirementAgent with SimpleCalculatorTool - Interactive Math Assistant"""
    
    llm = ChatModel.from_name("watsonx:meta-llama/llama-4-maverick-17b-128e-instruct-fp8", ChatModelParameters(temperature=0))
    
    # Create calculator agent with our custom tool
    calculator_agent = RequirementAgent(
        llm=llm,
        tools=[SimpleCalculatorTool()],
        memory=UnconstrainedMemory(),
        instructions="""You are a helpful math assistant. When users ask for calculations, 
        use the SimpleCalculator tool to provide accurate results. 
        Always show both the expression and the calculated result.""",
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )
    
    # Interactive examples - simulating human input
    math_queries = [
        "What is 15 + 27?",
        "Calculate 144 divided by 12",
        "I need to know what 8 times 9 equals",
        "What's (10 + 5) * 3 - 7?"
    ]
    
    for query in math_queries:
        print(f"\n👤 Human: {query}")
        result = await calculator_agent.run(query)
        print(f"🤖 Agent: {result.answer.text}")

async def main() -> None:
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    await calculator_agent_example()

if __name__ == "__main__":
    asyncio.run(main())


"""
Output::



👤 Human: What is 15 + 27?
--> 🛠️ SimpleCalculatorTool[SimpleCalculator][start]: {"input": {"input": {"expression": "15 + 27"}}}
<-- 🛠️ SimpleCalculatorTool[SimpleCalculator][finish]: "🧮 Simple Calculator\nExpression: 15 + 27\nResult: 42.0\nOperation: Addition"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "The result of 15 + 27 is 42.0"}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
🤖 Agent: The result of 15 + 27 is 42.0

👤 Human: Calculate 144 divided by 12
--> 🛠️ SimpleCalculatorTool[SimpleCalculator][start]: {"input": {"input": {"expression": "144 / 12"}}}
<-- 🛠️ SimpleCalculatorTool[SimpleCalculator][finish]: "🧮 Simple Calculator\nExpression: 144 / 12\nResult: 12.0\nOperation: Division"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "The result of 144 / 12 is 12.0"}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
🤖 Agent: The result of 144 / 12 is 12.0

👤 Human: I need to know what 8 times 9 equals
--> 🛠️ SimpleCalculatorTool[SimpleCalculator][start]: {"input": {"input": {"expression": "8 * 9"}}}
<-- 🛠️ SimpleCalculatorTool[SimpleCalculator][finish]: "🧮 Simple Calculator\nExpression: 8 * 9\nResult: 72.0\nOperation: Multiplication"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "The result of 8 * 9 is 72.0"}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
🤖 Agent: The result of 8 * 9 is 72.0

👤 Human: What's (10 + 5) * 3 - 7?
--> 🛠️ SimpleCalculatorTool[SimpleCalculator][start]: {"input": {"input": {"expression": "(10 + 5) * 3 - 7"}}}
<-- 🛠️ SimpleCalculatorTool[SimpleCalculator][finish]: "🧮 Simple Calculator\nExpression: (10 + 5) * 3 - 7\nResult: 38.0\nOperation: Addition"
--> 🛠️ FinalAnswerTool[final_answer][start]: {"input": {"input": {"response": "The result of (10 + 5) * 3 - 7 is 38.0"}}}
<-- 🛠️ FinalAnswerTool[final_answer][finish]: "Message has been sent"
🤖 Agent: The result of (10 + 5) * 3 - 7 is 38.0

"""