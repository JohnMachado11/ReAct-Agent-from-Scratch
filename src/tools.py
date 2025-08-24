from utils import format_internet_results


# Available tools and their descriptions
llm_tools = [
    {
        "name": "calculator_add",
        "description": "Add two numbers a and b. Both should be int or float. This tool cannot accept more than 2 numbers at a time."
    },
    {
        "name": "calculator_subtract",
        "description": "Subtract b from a. Both should be int or float. This tool cannot accept more than 2 numbers at a time."
    },
    {
        "name": "calculator_multiply",
        "description": "Multiply two numbers a and b. Both should be int or float. This tool cannot accept more than 2 numbers at a time."
    },
    {
        "name": "calculator_divide",
        "description": "Divide a by b. Both should be int or float; b must not be zero. This tool cannot accept more than 2 numbers at a time."
    },
    {
        "name": "llm_knowledge",
        "description": (
            "Use only for generating or retrieving *textual* content—"
            "facts, explanations, jokes, etc. **Do NOT** perform any arithmetic "
            "(adding, subtracting, multiplying, dividing)."
        )
    },
    {
        "name": "internet_search",
        "description": (
            "Search the internet for up-to-date, factual information. "
            "Always provide a plain string query as the Action Input "
            "(not a tuple). Use this tool whenever the answer requires "
            "current events, recent facts, or information beyond the model's "
            "built-in knowledge."
        )
    }
]

# List of all the tool names
tools_str = [tool["name"] for tool in llm_tools]

def calculator_add(a, b):
    """
    Add two numbers.

    Args:
        a (int | float): The first addend.
        b (int | float): The second addend.

    Returns:
        int | float: The sum of a and b.
    """
    print("     >> Invoking calculator_add")

    return a + b


def calculator_subtract(a, b):
    """
    Subtract b from a.

    Args:
        a (int | float): The minuend.
        b (int | float): The subtrahend.

    Returns:
        int | float: The difference a - b.
    """
    print("     >> Invoking calculator_subtract")

    return a - b


def calculator_multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a (int | float): The first factor.
        b (int | float): The second factor.

    Returns:
        int | float: The product of a and b.
    """
    print("     >> Invoking calculator_multiply")

    return a * b


def calculator_divide(a, b):
    """
    Divide a by b.

    Args:
        a (int | float): The dividend.
        b (int | float): The divisor. Must not be zero.

    Returns:
        float | str: The quotient a / b, or an error message if b is zero.
    """
    print("     >> Invoking calculator_divide")

    if b == 0:
        return "Can't divide by Zero"
    
    return a / b


def llm_knowledge(client, input):
    """
    Use GPT-4o for text generation without arithmetic.
    """
    print("     >> Invoking llm_knowledge")

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "Answer the question but do not **ever** perform any arithmetic."},
            {"role": "user", "content": input}
        ]
    )

    return completion.choices[0].message.content


def internet_search(client, input):
    """
    Use Tavily to search the internet.
    """
    print("     >> Invoking internet_search")

    response = client.search(
        query=input,
        max_results=3,
        search_depth="basic",
        include_images=False,
        include_image_descriptions=False,
        include_answer=False,
        include_raw_content=False
    )

    results = response.get("results", [])

    formatted = format_internet_results(results, header="\n-- Internet Search Results --", max_items=3, snippet_chars=600)
    return formatted