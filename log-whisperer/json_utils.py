"""Utilities for parsing LLM JSON responses."""

import json
import re


def extract_and_fix_json(text: str) -> dict:
    """
    Extract and fix JSON from LLM response text.
    
    Handles common issues:
    - Markdown code blocks
    - Text before/after JSON
    - Unescaped newlines in strings
    - Single quotes instead of double quotes
    - Incomplete/truncated JSON
    """
    original_text = text
    
    # Remove markdown code blocks - handle both ```json and ```
    text = text.strip()
    if text.startswith("```"):
        # Remove the opening ```json or ```
        lines = text.split('\n', 1)
        if len(lines) > 1:
            text = lines[1]
        else:
            text = text[3:]  # Just remove ```
        
        # Remove closing ```
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    
    # Extract JSON object if embedded in text
    if not text.startswith('{'):
        start = text.find('{')
        if start != -1:
            text = text[start:]
        else:
            raise ValueError(f"No JSON object found in text: {original_text[:200]}")
    
    # Check if JSON is complete (has closing brace)
    open_braces = text.count('{')
    close_braces = text.count('}')
    
    if open_braces > close_braces:
        # JSON is incomplete, try to fix it
        # Find the last complete field
        
        # Strategy 1: Find last complete string value
        last_quote_pos = -1
        quote_count = 0
        for i, char in enumerate(text):
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                quote_count += 1
                if quote_count % 2 == 0:  # Closing quote
                    last_quote_pos = i
        
        if last_quote_pos > 0:
            # Truncate after the last complete string
            text = text[:last_quote_pos + 1]
            
            # Remove trailing comma if present
            text = text.rstrip().rstrip(',')
            
            # Close any open arrays
            open_brackets = text.count('[')
            close_brackets = text.count(']')
            text += ']' * (open_brackets - close_brackets)
            
            # Close any open objects
            open_braces = text.count('{')
            close_braces = text.count('}')
            text += '}' * (open_braces - close_braces)
    
    # Try parsing as-is first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try fixing escaped characters
    try:
        # More aggressive string fixing
        def fix_string(match):
            content = match.group(1)
            # Fix common escape issues
            content = content.replace('\n', '\\n')
            content = content.replace('\t', '\\t')
            content = content.replace('\r', '\\r')
            # Fix backslashes
            content = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', content)
            return f'"{content}"'
        
        # Match strings including escaped quotes
        fixed = re.sub(r'"((?:[^"\\]|\\.)*)(?:"|\Z)', fix_string, text)
        
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    
    # Try removing all whitespace
    try:
        cleaned = ' '.join(text.split())
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON after multiple attempts. Error: {e}\nText preview: {text[:300]}")


def safe_parse_json(text: str, fallback: dict = None) -> dict:
    """
    Safely parse JSON with fallback.
    
    Args:
        text: Text containing JSON
        fallback: Dict to return if parsing fails
        
    Returns:
        Parsed dict or fallback
    """
    try:
        return extract_and_fix_json(text)
    except Exception as e:
        if fallback is not None:
            return fallback
        raise
