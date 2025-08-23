from urllib.parse import urlparse
import textwrap
import ast
import re


def shorten(txt, width=600):
    """
    Collapse internal whitespace and truncate a block of text to a target width.

    This is used to ensure search snippets stay compact for LLM consumption.
    The function first normalizes whitespace (collapsing runs of spaces/newlines)
    and then truncates with an ellipsis if needed.

    Args:
        txt: The original text snippet (may be None/empty).
        width: Maximum character width for the returned string (default 600).

    Returns:
        A whitespace-normalized, possibly truncated string. Returns "" if 'txt' is falsy.
    """

    if not txt:
        return ""
    # collapse whitespace, then truncate
    return textwrap.shorten(" ".join(txt.split()), width=width, placeholder="...")


def domain(url):
    """
    Extract the network location (domain) from a URL.

    Useful for counting unique sources (e.g., "Websites searched: N") in formatted
    search results. If parsing fails, the input URL is returned as a best-effort fallback.

    Args:
        url: A URL string (may be empty or malformed).

    Returns:
        The domain (netloc) portion of the URL (e.g., "example.com"), or the original
        string if parsing fails or no netloc is present.
    """

    try:
        return urlparse(url).netloc or url
    except Exception:
        return url or ""


def format_internet_results(results,
                            header="\n-- Internet Search Results --",
                            max_items=3,
                            snippet_chars=600):
    """
    Convert Tavily "search()" results into a single **text-only**, LLM-friendly string.

    The output is intentionally plain text so it can be fed directly back into a ReAct
    observation. It includes a dynamic header with counts (unique websites and results),
    followed by per-result blocks with Title, optional Date, URL, and a shortened Content
    snippet.

    Example output:

        ---- Internet Search Results ----

        Websites searched: 3
        Results returned: 3

        Result 1: Example Headline
        Date: 2025-08-08
        URL: https://news.example.com/article
        Content: This is a concise snippet of the article …

        Result 2: Another Headline
        URL: https://second.example.org/...
        Content: …

    Args:
        results: A list of result dicts from Tavily (e.g., each with 'title', 'url', 'content')
        header:  Top-level heading for the formatted block.
        max_items: Maximum number of results to include (truncate beyond this).
        snippet_chars: Maximum length of the content snippet per result.

    Returns:
        A single formatted string suitable for an LLM observation. If no results are present,
        returns "<header>:\\n\\nNo search results found.".

    """

    # Ensure "results" is a list (fallback to empty) and cap to "max_items"
    results = (results or [])[:max_items]
    if not results:
        return f"{header}:\n\nNo search results found."

    # Count unique domains (for the "Websites searched" line)
    unique_domains = {domain(r.get("url", "")) for r in results if r.get("url")}

    # Start building the text block with a header and dynamic counts
    lines = [f"{header}\n",
             f"Websites searched: {len(unique_domains)}",
             f"Results returned: {len(results)}",
             ""]
    
    # Append each result as a compact, readable section
    for i, r in enumerate(results, start=1):
        # Fallbacks if a field is missing
        title   = r.get("title") or "(no title)"
        url     = r.get("url") or "(no url)"
        content = r.get("content") or r.get("raw_content") or ""

        # Collapse whitespace and truncate long snippets to keep the block compact
        snippet = shorten(content, width=snippet_chars)

        lines.append(f"Result {i}: {title}")
        lines.append(f"URL: {url}")
        lines.append(f"Content: {snippet}")
        lines.append("")  # blank line between items

    # Join everything into a single string; strip trailing newline
    return "\n".join(lines).rstrip()


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

    # Search for "Action:" and "Action Input:"" lines
    action_match = re.search(r"Action: (.*)", text)
    action_input_match = re.search(r"Action Input: (.*)", text)

    # Proceed only if both are present
    if action_match and action_input_match:
        action = action_match.group(1).strip()
        action_input = action_input_match.group(1).strip()

        # For calculator tools, parse Python literal after cleaning parentheses
        if action not in {"llm_knowledge", "internet_search"}:
            try:
                raw = clean_parentheses(action_input)
                action_input = ast.literal_eval(raw)
            except Exception as e:
                print(f"Failed to parse action_input: {action_input} — {e}")
                return None, None

        # Return the tool name and its input argument
        return action, action_input

    # Missing either "Action:" or "Action Input:" invalid format
    return None, None