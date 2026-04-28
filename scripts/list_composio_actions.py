#!/usr/bin/env python3
"""List available Composio actions"""

import json
import sys
sys.path.insert(0, '/mnt/data/openclaw/workspace/.composio')

from composio_helper import api_post

# List available actions
result = api_post("v2/actions/list", {})
print("Available actions:")
if isinstance(result, dict) and "items" in result:
    for action in result["items"][:20]:
        print(f"  - {action.get('name', 'N/A')}")
else:
    print(json.dumps(result, indent=2))
