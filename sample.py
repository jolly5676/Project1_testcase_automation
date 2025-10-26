"""
This module handles basic payment and refund processing
for an online transaction system.

It includes functions for validating payments,
processing refunds, and generating transaction summaries.
"""

import datetime
import uuid


def validate_payment(card_number: str, expiry_date: str, cvv: str, amount: float) -> bool:
    """
    Validate payment details before processing.

    Steps:
    1. Check if the card number length is valid (16 digits).
    2. Ensure the card is not expired.
    3. Validate CVV length (3 digits).
    4. Confirm the transaction amount is greater than zero.
    """
    if len(card_number) != 16:
        raise ValueError("Invalid card number length")

    today = datetime.date.today()
    expiry = datetime.datetime.strptime(expiry_date, "%m/%y").date()
    if expiry < today:
        raise ValueError("Card has expired")

    if len(cvv) != 3:
        raise ValueError("Invalid CVV")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    return True


def process_payment(user_id: str, card_number: str, amount: float) -> dict:
    """
    Process a payment transaction for a given user.

    This function simulates a payment gateway API call.
    It assumes payment validation is already done.
    """
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    # Log simulated payment
    print(f"Processing payment for user {user_id} - Amount: {amount}")

    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "status": "SUCCESS",
        "timestamp": timestamp
    }


def issue_refund(transaction_id: str, user_id: str, amount: float) -> dict:
    """
    Issue a refund for a given transaction.

    The function records the refund operation and
    returns confirmation with timestamps.
    """
    if amount <= 0:
        raise ValueError("Refund amount must be positive")

    refund_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    print(f"Issuing refund for transaction {transaction_id} - Amount: {amount}")

    return {
        "refund_id": refund_id,
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "status": "REFUNDED",
        "timestamp": timestamp
    }
