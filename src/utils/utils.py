import json
import re
from typing import List


def extract_json_to_str(str):
    """Extract JSON content from triple-backtick markdown-style blocks."""
    json_match = re.search(r"```json\n(.*?)```", str, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    else:
        # Fall back if no backticks
        return json.loads(str)


def extract_json(text: str) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between \`\`\`json and \`\`\` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    # Define the regular expression pattern to match JSON blocks
    pattern = r"\`\`\`json(.*?)\`\`\`"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {text}")
