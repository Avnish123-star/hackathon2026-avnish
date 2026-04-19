import re

def classify(ticket):
    # Combine subject and body for a full search
    text = f"{ticket.get('subject', '')} {ticket.get('body', '')}".lower()
    
    # Priority keywords based on your JSON's 'expected_action'
    if any(k in text for k in ["refund", "money", "dispute", "return", "back"]):
        return {"category": "Refund", "urgency": "High", "resolvable": True}
    
    elif any(k in text for k in ["broken", "defect", "working", "cracked", "wobbles", "damaged"]):
        return {"category": "Technical", "urgency": "High", "resolvable": True}
        
    elif any(k in text for k in ["where", "status", "delivered", "transit", "track"]):
        return {"category": "Shipping", "urgency": "Medium", "resolvable": True}
    
    return {"category": "General", "urgency": "Low", "resolvable": False}