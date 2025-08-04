import ast
import re


def clean_parentheses(s):
    """
    Remove unmatched closing parentheses at the end of the string.

    When a string contains more closing parentheses than opening ones,
    this function strips off excess ')' characters from the end until
    the parentheses are balanced.

    Args:
        s (str): Input string possibly containing extra ')'.

    Returns:
        str: The cleaned string with balanced parentheses.
    """

    # Count how many open vs. close parens
    opens = s.count("(")
    closes = s.count(")")
    # If there are extra closes at the end, strip them off
    while closes > opens and s.endswith(")"):
        s = s[:-1]
        closes -= 1
    return s


def extract_action_and_action_input(text):
    """
    Parse an LLM response for a tool action and its input.

    This function searches the given text for lines starting with
    'Action:' and 'Action Input:'. If both are found, it extracts
    the tool name (action) and the argument string. For calculator
    tools (all except 'llm_knowledge'), it will clean up any excess
    parentheses and evaluate the argument as a Python literal.

    Args:
        text (str): The LLM response text containing tool directives.

    Returns:
        tuple[str, Any] or (None, None):
            - action (str): The tool name to call.
            - action_input (Any): The parsed argument(s) for the tool.
              For calculator tools, this will be a Python object (e.g.,
              tuple or list). For 'llm_knowledge', it will be a raw string.
            If the required directives are missing or parsing fails,
            returns (None, None) to indicate an invalid format.
    """

    # Search for 'Action:' and 'Action Input:' lines
    action_match = re.search(r"Action: (.*)", text)
    action_input_match = re.search(r"Action Input: (.*)", text)

    # Proceed only if both are present
    if action_match and action_input_match:
        action = action_match.group(1).strip()
        action_input = action_input_match.group(1).strip()

        # For calculator tools, parse Python literal after cleaning parentheses
        if action != "llm_knowledge":
            try:
                raw = clean_parentheses(action_input)
                action_input = ast.literal_eval(raw)
            except Exception as e:
                print(f"Failed to parse action_input: {action_input} — {e}")
                return None, None

        # Return the tool name and its input argument
        return action, action_input

    # Missing either 'Action:' or 'Action Input:' invalid format
    return None, None