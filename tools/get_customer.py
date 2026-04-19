import asyncio
import json
import os

async def get_customer(email: str): # MUST be 'email' to match orchestrator
    path = os.path.join('mock', 'customers.json') # Use 'mock' singular
    try:
        with open(path, 'r') as f:
            customers = json.load(f)
            # Find customer by email
            for c in customers:
                if c.get('email') == email:
                    return c
    except Exception as e:
        return {"error": str(e)}
    return None