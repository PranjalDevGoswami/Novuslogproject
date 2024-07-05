import requests
import numpy as np
from .models import Order, Voucher, VoucherDetails
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
import json

# Function to send an email with voucher codes
def send_voucher_email(email, voucher_codes):
    subject = "Your Vouchers from Novus Insights"
    message = f"Here are your voucher codes:\n\n" + "\n".join(voucher_codes)
    from_email = "noreply.erp@unimrkt.com"
    
    # Directly use email as a list of strings for recipients
    send_mail(
        subject,
        message,
        from_email,
        [email],  # Recipient email as a list
    )

# Function to handle the voucher order process
def send_voucher_order(selected_voucher, voucher_value, voucher_quantity, notify_receiver_email, notify_admin_email):
    random_number = np.random.randint(1000, 10000)
    print(random_number)

    url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api/"
    payload = {
        "query": "plumProAPI.mutation.placeOrder",
        "tag": "plumProAPI",
        "variables": { 
            "data": {
                "productId": int(selected_voucher),
                "quantity": int(voucher_quantity),
                "denomination": int(voucher_value),
                "poNumber": f"PO{random_number}",
                "notifyReceiverEmail": notify_receiver_email,
                "notifyAdminEmail": notify_admin_email
            }
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTk4MTczMjk0NzgsImV4cGlyZXNBdCI6MTcyMTExMzMyOTQ3OCwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbEZQVFZCSlJYQlBOemw1YkdJek5VeEpXVEpVV2s5QldsTmtZa0o1UjAxSE1IUktXR1IwVldKbGFGVWlMQ0o1SWpvaVozRmZRMUF6Ulc5V1NIQkhNVWQ0VUVnNGVXbHBPSHBoZG10VFp6SktSamx1UW5GUk5VNXNlblpaWnlKOWZRLi56SXNJR2NrMXhqdmlENWp1aElNTG5nLmlyM3V4RVVHakhON3dSMnZFdFFIQUwxNFMyNXpVS09DV2NWQkFaamhlZW83T0VOMDF6YjNnTHc2YTM5SlE2TGRwQi1PMmljRHk0WXBIb0VmWE1iUnVZeW5rcTdkcTFEdVAwM2pFcW1TSEJvMkloQno5aWxkb0xvMnRhT1lPcFBDRzFFQlFETU40d2V5Q0cydG1uLUJqTHFjVFFDQzA1YzhMYmdkaDhTQUhld0VNUEE1M0lDcU5ZQ1I4ME9YTkJBUGMtV2g0cFI3enN3Z1NpNmRrd0tUZlBSa2hPYVQ2ckEwNTRweHVqYjEwcjVwd2hMSkhJM0dLRE16aHlWV0tJMFVIT2MzYXFMWXExcWszbjZsUDN1QWlNTk1yc0dyejhmaHF3Z1VSbWFpZDZ5X3o2MmtNOFhVX0FVaFI4Q2ZTR2NFc2VvYnJxSGVGVUFfSm12Q1k0UDJKRmJmN2xTQ2Zuc2lLZmFNWWxveVJzbkM1TGphV1BKaWg1UzBpU29rNGFLcmxQR0FFdFRTbzRqeXdRaksydHdJQUg2cmVuQ1liR2RyWEVZbDJVd0dZbUpwd2w0c3FmSWx4dXJzUDBJczFZNllqY3Q1TlE1TGg4TkVBbDBxdmFBS1FWeVdKVTg5X3BySU1DLU96eUZqbU9sZy1pcFAwcVhsUmZhdVltaFNCM0NaTmtXNU80bGJZWEFyaGVHaHFHM2lEVnpPaVFOTU5NejRMSURoOEFlRDNrVDdMX3ZLWXNWdXpveGptT0xrMk1oWlpQSVp6dTVNUW5IdlNqNkhWNFMtQTJzc25aZ0YzRmQyN1hCQWJhcE1mQl9NazNGcld6aXN1RlhxUkpVcU4yR3g2YkVNc3BDUUlXdWhlMGlQVndjdFprUVdrbWM4UjlKUmRfd3QzMXhxMVd2QlIwRjNldmljeVhjaXZtQlJNZVRWaTJoOFRBLWFtNERjS042dEVwaFlyNnotY0FXYkFUUFNEQWNoa0xYTUtHSTZETjVSZGdZenZKVjZLYlloVmxvVmlTODJmYWc0bHQtZ1F5RlMyWXBxalRaejlyTUItOXMtQVNNY2p6eFc4V1lTdTRKamJBekpzckJoRkxOaW5wUFhlMlJWNzJVdmpkNHJlRkFNLXQ3UzNyQmVXc21LSm1fTEd3MlhBanZnTURHdW5GbXZZbkNMNFV5RXJ0RzJpLXpyRkVxYXFCZmN1REVNMnRsRDFaREZ3Zy5SLU5sYVNxUk95XzhadHBVYVMyaFhnIn0="
    }

    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Ensure the request was successful

    data = response.json()

    if 'data' not in data or 'placeOrder' not in data['data'] or 'data' not in data['data']['placeOrder']:
        raise ValueError("Unexpected API response structure")

    order_data = data['data']['placeOrder']['data']

    # Create and save the Order instance
    order = Order.objects.create(
        order_id=int(order_data['orderId']),
        order_total=str(order_data['orderTotal']),
        order_discount=str(order_data.get('orderDiscount', '')),
        discount_percent=str(order_data.get('discountPercent', '')),
        currency_code=order_data['currencyCode'],
        currency_value=str(order_data['currencyValue']),
        amount_charged=str(order_data['amountCharged']),
        order_status=order_data['orderStatus'],
        delivery_status=order_data['deliveryStatus'],
        tag=order_data.get('tag', ''),
        quantity=int(order_data['quantity'])
    )

    # Create and save each Voucher instance
    for voucher in order_data['vouchers']:
        Voucher.objects.create(
            order=order,
            product_id=int(voucher['productId']),
            voucher_code=voucher['voucherCode'],
            pin=voucher.get('pin', ''),
            validity=voucher['validity'],
            amount=str(voucher['amount']),
            currency=voucher['currency'],
            country=voucher['country'],
            voucher_type=voucher['type'],
            currency_value=str(voucher['currencyValue'])
        )

    # Create and save each VoucherDetails instance
    for detail in order_data['voucherDetails']:
        VoucherDetails.objects.create(
            order=order,
            product_id=int(detail['productId']),
            product_name=detail['productName'],
            currency_code=detail['currencyCode'],
            product_status=detail['productStatus'],
            denomination=str(detail['denomination'])
        )

    # Send email with voucher codes
    voucher_codes = [v['voucherCode'] for v in order_data['vouchers']]
    send_voucher_email('ankit.sharma@novusinsights.com', voucher_codes)
    
    