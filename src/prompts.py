from tools import tools_str, llm_tools

from pprint import pp


react_system_prompt = f"""
    You have access to the following tools:
    {llm_tools}

    You must use the following format:
        Question: The input question you must answer.
        Thought: You should always think about what to do.
        Action: The action to take, should only be one of {tools_str}.
        Action Input: The input to the action.
        Observation: The result of the action.
        ... (The Thought/Action/Observation can repeat any number of times)
        Thought: I now know the final answer!
        Final Answer: The answer to the original input question.

        ** Example **
        Question: What is 5 + 5?
        Thought: I need to add the two numbers 5 and 5 together.
        Action: calculator_add
        Action Input: (5, 5)
        Observation: 10
        Thought: I now know the final answer!
        Final Answer: 10

    ** Important Details **
    1. **All** arithmetic (adding, subtracting, multiplying, dividing) must be done with calculator tools.
        - When you use one of these calculator tools, you **must** supply a Python tuple of exactly two numbers, e.g.:
            Action Input: (8, 42)
        - Never output a single number as the Action Input for a calculator tool.
    2. The tool 'llm_knowledge' is only for generating or retrieving textual content, **never** use it for any arithmetic.
    3. You must always provide both:
        - Action: one of {tools_str}
        - Action Input: formatted correctly.
        Do not invent your own action phrases (e.g. 'I will convert...'). That is not valid.
"""

user_prompt = """
    Let's go on a journey of reasoning, math, and creativity:

    1. Begin by telling me a joke related to artificial intelligence.
    2. Identify and list all numerical values that appear in or are implied by the joke. This includes anything that can be interpreted as a number (e.g., “twice” implies 2).
    3. Combine those numbers into a single total.
    4. Take the punchline of the joke, count how many characters it contains, and multiply that number with your previous total.
    5. Next, count all the vowels in the full joke and divide your last result by that number.
    6. Now consider how many years it has been since 1990 and subtract that from your current result.
    7. Add the value of pi (approx. 3.14) to what you have now.
    8. Multiply the new value by the number of distinct capabilities or tools you have access to.
    9. Imagine this final number represents the internal temperature of a robot in Celsius. Would such a temperature be survivable or fatal for a robot? Think carefully and explain.
    10. Take the number of words in your explanation and add that to your result.

    Provide your final answer, and briefly walk through how you got there.
"""

chat_history = [
    {
        "role": "system",
        "content": react_system_prompt
    },
    {
        "role": "user",
        "content": f"""
        Question: {user_prompt}
        """
    }
]


if __name__ == "__main__":
    pp(chat_history)


# user_prompt = "Calculate 5 + 5 + 25"

# user_prompt = "Calculate 5 * 5"

# user_prompt = "Calculate 5 - 5"

# user_prompt = "Calculate 4 / 2"

# user_prompt = "((8+12) x 3-10) ÷ 2+7"

# user_prompt = "(((6 + 4) * 5 - (18 / 3) + 7) / 2 + (9 * 2 - 4)) - ((10 + 2  * 3) ÷ 4) + 15"

# user_prompt = "Convert the joke 'Why did the AI go broke? It couldn't find its cache!' into ASCII values. Sum all those ASCII values up together. Then add 42 to it in the end."

# user_prompt = """
#    (2 + 3 - 1 + 4 * 2 - 6 / 2 + 5 - 2 + 3 * 1) + 
#    (4 * 2 + 6 - 5 + 3 / 1 - 2 + 8 - 4 + 1 * 2) + 
#    (7 - 3 + 2 * 2 - 1 + 5 / 1 + 6 - 4 + 3 * 2) + 
#    (9 / 3 + 2 + 4 - 5 + 6 * 1 - 3 + 8 - 2 + 1) + 
#    (3 + 6 * 2 - 7 + 1 / 1 + 4 - 2 + 5 + 3 - 1) + 
#    (2 + 8 - 3 * 1 + 6 / 2 + 7 - 4 + 1 + 5 - 2) + 
#    (4 * 1 + 2 - 3 + 7 / 1 + 5 - 6 + 3 + 2 - 1) + 
#    (9 - 5 + 4 * 2 - 3 / 1 + 6 - 2 + 8 - 4 + 1) + 
#    (2 + 3 * 1 - 1 + 5 / 1 + 7 - 6 + 2 + 4 - 3) + 
#    (6 / 2 + 8 - 5 + 3 * 1 - 1 + 7 - 4 + 2 + 1)
# """