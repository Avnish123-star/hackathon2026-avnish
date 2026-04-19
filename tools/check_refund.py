def check_refund(order_id, amount):
    # irreversible action (refund triggered)
    return amount < 500
