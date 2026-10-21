"""
Brew Haven — Orders Lambda (showcase code only)
================================================
AWS Lambda function (Python) that receives a coffee order and appends it
as a new item to a DynamoDB table.

This is illustrative source code only — it is NOT deployed or run here.
Table creation, IAM roles, API Gateway, and deployment are handled separately.

Expected environment variable:
    ORDERS_TABLE   DynamoDB table name (default: "BrewHavenOrders")

Assumed DynamoDB table key schema:
    Partition key : order_id (String)

Expected incoming order payload (JSON), e.g. from API Gateway proxy:
    {
        "customer": "Aarav Sharma",
        "items": [
            {"name": "Caramel Latte", "qty": 2, "price": 250},
            {"name": "Fresh Croissant", "qty": 1, "price": 150}
        ],
        "payment": "UPI"
    }
"""

import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

# Initialized once per container (reused across warm invocations)
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("ORDERS_TABLE", "BrewHavenOrders")
table = dynamodb.Table(TABLE_NAME)


def _response(status_code, body):
    """Build an API Gateway (proxy) style HTTP response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # adjust to your site origin in production
        },
        "body": json.dumps(body),
    }


def _parse_body(event):
    """Accept either a raw dict event or an API Gateway proxy event."""
    if isinstance(event, dict) and "body" in event and event["body"] is not None:
        body = event["body"]
        return json.loads(body) if isinstance(body, str) else body
    return event  # direct invocation with the payload as the event


def handler(event, context):
    # 1. Parse the incoming order
    try:
        order = _parse_body(event)
    except (ValueError, TypeError):
        return _response(400, {"message": "Invalid JSON body."})

    customer = (order.get("customer") or "Guest").strip()
    items = order.get("items") or []
    payment = order.get("payment") or "Unknown"

    # 2. Validate
    if not items:
        return _response(400, {"message": "Order must contain at least one item."})
    if payment not in ("UPI", "Cash on Delivery"):
        return _response(400, {"message": "Unsupported payment method."})

    # 3. Compute totals (Decimal — DynamoDB does not accept float)
    total_qty = 0
    total_price = Decimal("0")
    normalized_items = []
    for it in items:
        name = str(it.get("name", "")).strip()
        qty = int(it.get("qty", 0))
        price = Decimal(str(it.get("price", 0)))
        if not name or qty <= 0:
            return _response(400, {"message": f"Invalid item: {it}"})
        total_qty += qty
        total_price += price * qty
        normalized_items.append({"name": name, "qty": qty, "price": price})

    # 4. Build the DynamoDB item
    item = {
        "order_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "customer": customer,
        "items": normalized_items,
        "total_qty": total_qty,
        "total_inr": total_price,
        "payment": payment,
        "status": "RECEIVED",
    }

    # 5. Append (put) the order into the table
    try:
        table.put_item(Item=item)
    except ClientError as err:
        print("DynamoDB PutItem failed:", err.response["Error"]["Message"])
        return _response(500, {"message": "Could not save the order. Please try again."})

    # 6. Confirm back to the caller
    return _response(201, {
        "message": "Order received.",
        "order_id": item["order_id"],
        "total_qty": total_qty,
        "total_inr": float(total_price),
        "payment": payment,
    })
