import asyncio
import random

async def get_order(order_id: str):
    if "fail" in order_id or random.random() < 0.1:
        await asyncio.sleep(6) # Simulate timeout
        return {"error": "Timeout", "details": "Database connection slow"}
    return {"order_id": order_id, "status": "shipped", "customer_email": "user@example.com"}

async def check_refund_eligibility(order_id: str):
    # Logic-based mock
    return {"eligible": True, "reason": "Damaged item policy"}

async def issue_refund(order_id: str, amount: float):
    # Irreversible action [cite: 95]
    return {"status": "success", "refund_id": f"REF-{random.randint(100, 999)}"}

async def send_reply(ticket_id: str, message: str):
    return {"status": "sent", "ticket_id": ticket_id}