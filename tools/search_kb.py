import asyncio

async def search_kb(query: str):
    """
    Policy & FAQ semantic search tool [cite: 90-91].
    """
    # Realistic mock behavior: slightly delay to simulate search [cite: 99]
    await asyncio.sleep(0.2)
    
    # Mock knowledge base data
    kb_data = {
        "refund": "Refunds are allowed within 30 days of delivery[cite: 93].",
        "warranty": "Standard electronics have a 1-year limited warranty[cite: 89]."
    }
    
    # Simple keyword match for the mock
    for key in kb_data:
        if key in query.lower():
            return {"result": kb_data[key]}
            
    return {"result": "No specific policy found. Escalate if necessary[cite: 98]."}