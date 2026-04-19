import asyncio
import json
import os

async def get_order(order_id: str):
    # FIX: Ensure path matches your 'mock' folder name
    path = os.path.join('mock', 'orders.json') 
    try:
        with open(path, 'r') as f:
            orders = json.load(f)
            for o in orders:
                if o.get('order_id') == order_id:
                    return o
    except Exception as e:
        return {"error": str(e)}
    return None