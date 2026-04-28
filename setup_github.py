#!/usr/bin/env python3
from composio import Composio
from composio.client.enums import Action

client = Composio(api_key='ak_hMY622y3ORsaH2IpDOrJ')

# Get the action
action = client.actions.get(action=Action.GITHUB_CREATE_A_REPO_FOR_THE_AUTHENTICATED_USER)
print(f"Action found: {action}")

# Execute GitHub repo creation
result = client.actions.execute(
    action=Action.GITHUB_CREATE_A_REPO_FOR_THE_AUTHENTICATED_USER,
    params={
        'name': 'tani-bot',
        'description': 'Hybrid ML + LLM agricultural assistant for Indonesia - yield prediction, planting optimization, conversational AI',
        'private': False,
        'auto_init': True
    },
    entity_id='default'
)

print("\nGitHub Repo Creation Result:")
print(result)
