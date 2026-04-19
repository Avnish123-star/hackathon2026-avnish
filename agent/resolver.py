from tools.check_refund import check_refund
from tools.send_reply import send_reply

def auto_resolve(category, order, ticket_id):
    if category == "refund":
        ok = check_refund(order["id"], order["amount"])
        if not ok:
            return False, "Refund not eligible."

        send_reply(ticket_id, "Your refund has been processed.")
        return True, "Refund processed."

    if category == "damage":
        send_reply(ticket_id, "We apologize. Replacement is underway.")
        return True, "Replacement initiated."

    return False, "Cannot resolve automatically."
