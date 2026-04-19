import asyncio
import random

# Ensure the function name matches the import exactly
async def get_product(product_id: str):
    """
    Fetches Product metadata, category, and warranty [cite: 88, 89]
    """
    # Simulate a realistic mock delay or failure [cite: 99]
    await asyncio.sleep(0.1) 
    
    # Example mock data
    products = {
        "p1": {"name": "Wireless Mouse", "category": "Electronics", "warranty": "1 year"},
        "p2": {"name": "Keyboard", "category": "Electronics", "warranty": "2 years"}
    }
    
    return products.get(product_id, {"error": "Product not found"})