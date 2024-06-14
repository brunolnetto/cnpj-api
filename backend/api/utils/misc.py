import json
import re

def string_to_json(string: str) -> dict:
    string=string.replace("'", '\"')
    string = re.sub(r'\bNone\b', 'null', string)
    
    return json.loads(string)

