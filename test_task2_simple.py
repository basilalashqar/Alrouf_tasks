#!/usr/bin/env python3
"""
Simple test script for Task 2 - Quotation Service
"""

import requests

# Test quotation generation
quotation_data = {
    "client": {
        "name": "Gulf Engineering",
        "contact": "omar@client.com",
        "lang": "en"
    },
    "currency": "SAR",
    "items": [
        {
            "sku": "ALR-SL-90W",
            "qty": 120,
            "unit_cost": 240.0,
            "margin_pct": 22
        },
        {
            "sku": "ALR-OBL-12V",
            "qty": 40,
            "unit_cost": 95.5,
            "margin_pct": 18
        }
    ],
    "delivery_terms": "DAP Dammam, 4 weeks",
    "notes": "Client requested Tarsheed compliance"
}

response = requests.post("http://localhost:8000/quote", json=quotation_data)
result = response.json()

print(f"Quotation ID: {result['quotation_id']}")
print(f"Client: {result['client']['name']}")
print(f"Subtotal: {result['subtotal']} SAR")
print(f"Tax: {result['tax_amount']} SAR")
print(f"Total: {result['total']} SAR")
print(f"Email Draft: {result['email_draft']}")
