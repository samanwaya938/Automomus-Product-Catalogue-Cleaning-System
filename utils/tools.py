import json
import re


def extract_json(text: str) -> dict:
    """
    Extract and clean JSON block from LLM output.
    Removes markdown and inline comments.
    """
    try:
        # Extract code block content
        if "```json" in text:
            json_block = text.split("```json")[1].split("```")[0].strip()
        else:
            json_block = text.strip()

        # ❌ Remove JavaScript-style inline comments (// ...)
        json_block = re.sub(r"//.*", "", json_block)

        # ❌ Remove Python-style comments too (optional, rarely needed)
        json_block = re.sub(r"#.*", "", json_block)

        return json.loads(json_block)
    except Exception as e:
        print("❌ Failed to extract or parse JSON:\n", text)
        raise e