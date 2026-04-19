import asyncio
import re
from agent.state import AgentState
from agent.classifier import classify
from agent.resolver import auto_resolve

# Standardize imports to prevent ImportError [cite: 156]
from tools import get_customer, get_order, get_product, search_kb, escalate

async def safe_call(state, tool_fn, name, **kwargs):
    """
    Robust tool wrapper with timeout and retry logic[cite: 12, 71].
    Handles the mandatory 'Recover' requirement by awaiting async mocks[cite: 71].
    """
    retries = 2
    for i in range(retries):
        try:
            # wait_for handles the required tool timeouts [cite: 71]
            result = await asyncio.wait_for(
                tool_fn(**kwargs),
                timeout=2.0 
            )
            # Log tool calls and outcomes for the mandatory Audit Log [cite: 60, 61, 135]
            state.log_tool(name, kwargs, result)
            return result
        except Exception as e:
            # Failed tickets are logged, not ignored [cite: 107]
            state.log(f"Warning: {name} failed on attempt {i+1}: {str(e)}")
            
    return None

async def process_ticket_async(ticket):
    state = AgentState(ticket)
    
    # Robustly handle ID keys [cite: 150]
    t_id = ticket.get("ticket_id") or ticket.get("id") or "Unknown-ID"

    # NEW: Regex to extract Order ID (e.g., ORD-1001) from the ticket body
    # This ensures your tool calls aren't 'null' [cite: 49, 135]
    body_text = ticket.get("body", "") + ticket.get("message", "")
    order_match = re.search(r"ORD-\d+", body_text)
    order_id = order_match.group(0) if order_match else None
    
    customer_email = ticket.get("customer_email")

    # Phase 1: Ingest & Classify [cite: 50, 52]
    c = classify(ticket)
    state.log(f"Phase 1: Ticket classified as {c['category']} ({c['urgency']})")

    # Phase 2: The Tool Chain (MUST make at least 3 calls) [cite: 69, 70]
    # Chain: lookup user -> check order -> check product
    customer = await safe_call(state, get_customer, "get_customer", email=customer_email)
    order = await safe_call(state, get_order, "get_order", order_id=order_id)
    
    # Dynamically find product_id from the order details if available [cite: 84, 88]
    p_id = order.get("product_id") if (order and isinstance(order, dict)) else None
    product = await safe_call(state, get_product, "get_product", product_id=p_id)

    # Phase 3: Research Knowledge Base [cite: 90, 91]
    kb = await safe_call(state, search_kb, "search_kb", query=f"Policy for {c['category']}")

    # Phase 4: Decision Logic (Confidence Calibration) [cite: 75, 107, 150]
    # An agent must know what it doesn't know [cite: 107]
    can_resolve = (
        c.get("resolvable", False)
        and customer is not None
        and order is not None
        and "error" not in str(order)
    )

    if can_resolve:
        # Phase 5: Autonomously Resolve [cite: 55, 56]
        ok, msg = auto_resolve(c["category"], order, t_id)
        state.final_action = {"action": "resolved", "message": msg}
        state.log(f"Phase 2: Resolution success for {t_id}")
    else:
        # Phase 5: Escalate Intelligently [cite: 58, 59]
        # Hand off with a structured summary [cite: 59, 98]
        summary = f"Reason: Data missing or low confidence. Category: {c['category']}"
        escalate(t_id, summary, c["urgency"])
        state.final_action = {"action": "escalated", "reason": summary}
        state.log(f"Phase 2: Escalating {t_id} for human review")

    # Return result for the mandatory audit_log.json [cite: 60, 135, 141]
    return {
        "ticket_id": t_id,
        "reasoning": state.reasoning,
        "final_decision": state.final_action
    }