import re
from typing import List, Dict

def to_float(num_str: str) -> float:
    """
    Safely convert extracted numeric strings to float.
    Handles cases like '4.8.' or '12.1..'
    """
    return float(num_str.strip().replace("..", ".").rstrip("."))

def extract_lab_results(texts: List[str]) -> List[Dict]:
    """
    Extract lab test name, value, unit, and reference range from normalized text.
    """

    results = []

    pattern = re.compile(
        r"The (.+?) level is ([\d\.]+)\s*([a-zA-Z/%\.]+).*?range is ([\d\.]+)[–\-]([\d\.]+)",
        re.IGNORECASE,
    )

    for text in texts:
        matches = pattern.findall(text)
        for test, value, unit, min_r, max_r in matches:
            try:
                value_f = to_float(value)
                min_f = to_float(min_r)
                max_f = to_float(max_r)
            except ValueError:
                continue 

            status = "Normal"
            if value < min_r or value > max_r:
                status = "Out of Range"

            results.append(
                {
                    "test": test.title(),
                    "value": f"{value} {unit}",
                    "range": f"{min_r}–{max_r} {unit}",
                    "status": status,
                }
            )

    return results
