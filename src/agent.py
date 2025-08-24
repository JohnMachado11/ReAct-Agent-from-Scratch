from utils import extract_action_and_action_input
from prompts import chat_history
from tools import tools_str
from tools import (
    calculator_add, 
    calculator_divide, 
    calculator_multiply, 
    calculator_subtract, 
    llm_knowledge,
    internet_search)

from dotenv import load_dotenv
from tavily import TavilyClient
from openai import OpenAI
import os

load_dotenv()


# Initialize OpenAI client with API Key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Initialize Tavily (internet search) client with API Key 
tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))

# ---------------------  Main ReAct loop  ---------------------
iterations = 1
while True:

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=chat_history,
        stop=["Observation:"] # Halt generation at "Observation:" so the LLM doesn’t hallucinate results. We’ll run the tool and inject its actual output.
    )

    response_text = completion.choices[0].message.content
    print("-" * 80)
    print(f"ReAct Loop #{iterations}\n")
    print(response_text)

    action, action_input = extract_action_and_action_input(response_text)

    # Check if the model proposed an action
    if action:
        print(f"\n-- Taking the action of '{action}' --")

        # Dispatch to tool implementations
        if action == "calculator_add":
            a, b = action_input
            action_result = calculator_add(a, b)
        elif action == "calculator_subtract":
            a, b = action_input
            action_result = calculator_subtract(a, b)
        elif action == "calculator_multiply":
            a, b = action_input
            action_result = calculator_multiply(a, b)
        elif action == "calculator_divide":
            a, b = action_input
            action_result = calculator_divide(a, b)
        elif action == "llm_knowledge":
            action_result = llm_knowledge(client, action_input)
        elif action == "internet_search":
            action_result = internet_search(tavily_client, action_input)
        
        print(f"\nObservation:", action_result)

        # Feed observation back into chat history
        result = [
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": f"Observation: {action_result}"}
        ]
        chat_history.extend(result)

        print("-" * 80, "\n")
        iterations += 1
    else:
        # Check for final answer or re-prompt
        if "Final Answer:" in response_text:
            print("\n-- Final answer detected. Stopping. --\n")
            chat_history.append({"role": "assistant", "content": response_text})
            break
        else:
            print("-- No valid action or action input detected. Re-prompting. --")
            result = [
                {"role": "assistant", "content": response_text},
                {"role": "user", "content": (
                    "You did not follow the required format. "
                    "You must provide a valid Action and Action Input. "
                    f"The action must be one of {tools_str}. "
                    "Try again and follow the format carefully."
                )}
            ]
            chat_history.extend(result)
            iterations += 1
            continue