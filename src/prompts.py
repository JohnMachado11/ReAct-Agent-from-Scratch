from tools import tools_str, llm_tools
from datetime import datetime
from pprint import pp


current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

react_system_prompt = f"""
    You have access to the following tools:
    {llm_tools}

    Current date and time: {current_dt}

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
    3. The tool 'internet_search' must be used whenever the question requires fresh, up-to-date, or external information
        (e.g., current events, breaking news, live data, or anything the model cannot reliably know).
        - Action Input for 'internet_search' must always be a plain string query, not a tuple.
        - Example:
            Action: internet_search
            Action Input: "What is the current stock price of Toyota?"
    4. If a question asks for the current date or time, DO NOT search the internet as this is already provided in your system prompt.
    5. You must always provide both:
        - Action: one of {tools_str}
        - Action Input: formatted correctly.
        Do not invent your own action phrases (e.g. 'I will convert...'). That is not valid.
    6. Write control lines exactly as plain text (no markdown/bold): 'Thought:', 'Action:', 'Action Input:', 'Observation:', and 'Final Answer:'.
"""

user_prompt = """
Goal: Produce a final number and a brief explanation, using realistic financial conversions and up-to-date data.

Steps:
1) From up-to-date public sources, identify the latest publicly reported reward/bounty (USD) for Nicolás Maduro. Extract the numeric USD amount (N_USD) and the announcement month and year (ANN_DATE).
2) In a separate observation, write ONE concise sentence explaining what the reward refers to (no numbers, no math).
3) Obtain the U.S. CPI-U (all items, 1982-84=100) for ANN_DATE and for the current month. Call them CPI_then and CPI_now.
4) Inflation-adjust N_USD into today's dollars:
    a. compute the factor F = CPI_now ÷ CPI_then
    b. compute the adjusted amount N_USD_adj = N_USD x F
    (Keep full precision; round only when requested.)
5) Obtain the latest market USD→VES exchange rate; call it R (VES per 1 USD).
6) Convert the adjusted bounty to VES: N_VES = N_USD_adj x R. (Round to the nearest whole VES at reporting time, not here.)
7) From up-to-date public sources, find the official Venezuelan minimum monthly salary S_VES (in VES).
8) Compute affordability in wages:
    a. months = N_VES ÷ S_VES
    b. years = months ÷ 12
9) From up-to-date public sources, find the latest Brent crude oil price B (USD per barrel).
10) Compute how many barrels could be purchased with N_USD_adj: barrels = N_USD_adj ÷ B. (Round to the nearest whole barrel at reporting time.)
11) From up-to-date public sources, find the current 6-month U.S. Treasury bill yield Y (percent).
12) Estimate one year of interest if the adjusted bounty were invested at Y (simple approximation):
    a. d = Y ÷ 100
    b. I_USD = N_USD_adj x d
13) In a separate observation, write ONE sentence (no numbers) explaining one reason the above conversions/estimates can change over time (e.g., exchange-rate volatility, oil price swings, CPI revisions).
14) List the external source domains you used across steps 1, 3, 5, 7, 9, and 11 as an ordered list of domains only (e.g., example.com).
15) Provide:
    - Final Answer: (a) N_USD_adj in USD with commas, (b) N_VES with commas, (c) barrels as an integer, (d) years at minimum salary rounded to one decimal, and (e) I_USD in USD with commas.
    - Include the sentence from step 2 verbatim, followed by the sentence from step 13.
    - Then include the ordered list of domains from step 14.
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


# user_prompt = """
#     Let's go on a journey of reasoning, math, and creativity:

#     1. Begin by telling me a joke related to artificial intelligence.
#     2. Identify and list all numerical values that appear in or are implied by the joke. This includes anything that can be interpreted as a number (e.g., “twice” implies 2).
#     3. Combine those numbers into a single total.
#     4. Take the punchline of the joke, count how many characters it contains, and multiply that number with your previous total.
#     5. Next, count all the vowels in the full joke and divide your last result by that number.
#     6. Now consider how many years it has been since 1990 and subtract that from your current result.
#     7. Add the value of pi (approx. 3.14) to what you have now.
#     8. Multiply the new value by the number of distinct capabilities or tools you have access to.
#     9. Imagine this final number represents the internal temperature of a robot in Celsius. Would such a temperature be survivable or fatal for a robot? Think carefully and explain.
#     10. Take the number of words in your explanation and add that to your result.

#     Provide your final answer, and briefly walk through how you got there.
# """

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