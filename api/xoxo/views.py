from django.shortcuts import render
from django.shortcuts import render
from .api import get_vouchers
import requests
from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView



def get_vou(request):
    url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api/"
    payload = {
        "query": "plumProAPI.mutation.getVouchers",
        "tag": "plumProAPI",
        "variables": {
            "data": {
                "limit": 10,
                "page": 1,
                "exchangeRate": 1,
                "sort": {
                    "field": "name",
                    "order": "ASC"
                }
            }
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTcxMjU1MzcxNTIsImV4cGlyZXNBdCI6MTcxODQyMTUzNzE1MiwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbGxtYmpkcE1GZHVTazlxVFdocVVHSlVTRkpvTUV0UU4yTXdkRkJaZW0xd1VUWlFjMGhCVmxnMmRqZ2lMQ0o1SWpvaU5ubzBZbGRVTnpSbFppMVVNRE42WmtwUWVEVnBhVWgzVVdGNk5YYzVNSE5aYVhwaVEyOWhlRlpTTUNKOWZRLi5sWVZYQklkbHUyNlFMOE9yNTMtT2lRLkdDN0N4S0lTVVRMdjZkMExFWUtRV3JUaEFtX0tCWXk5Y0VlZGl6S0tLaDdwOUhnbmlwWkhjNTZkZzBCRl9LT2VNWVhzYUQxS3NCTHE1cFFkSGdVMk5ia3lTUko4QWcyTmFRa3ZOUUU0X05QenhFY016SHV4OG9uNWt5WkVnNV9TNDQ4TDdHNUVsajUzY0pRSnE0SVY5NmhFdWdXdjNOWlB0bXVnbTJMOXBSbUJHLUR2X29RQjVoUkp4YlVNaThSVW83RWRsOHl3bWRPTk90WWhibEVUY1paaEM5Zzk2aUJULXhZc0p4alZ6N1pNS25rY0JJV3V5S1pZLUtYZ3F5VzZVY3hza3hhOGY3NE96R2pJWTc2Z0ltVVNpZEpjZ2VrT05ySDBzNU1SX2p3aUJFX0lSdHhpQ1hMc045dlJ6YW54TzdIaTZfMTBnMWxfMGZSdnd3LUY4aHJnbXh3aVFSeEQ3UWMyN2JETlM0NTVvbjVwZTU4dXVpUTJELS1sZkUxbktCYUxTaGozQUt4VGs3RDdtcEZTR1Z5UDV4MGNQY3RfSXo5UmRkZnRnNmppaGJvcHpQU2ZUVUdZZjM4S3I1Z3RUZjkxV21qVHRlN3hXZkgyb1JmbkhJc0FSS2VTYTdBcUYwb05VcWh3dTk0QTJKc3ZldmhVLVYxS3RDdnU2TzVMWmo0SWp1bDhIbG5zamExY2hBRG9CZ2l5SlBlWjJiRFFpOVdLS0NXSE1heGtxSk9GZTdhQm1oVkdsZVI2SWpVRlN4bXFXSHgtV0dvVnRrTVBDbzV0bndjdTlPVzhfX3JDenZPWVMyeWRjbDQ4VkVBYU8xUGdlMTh1ZnZMRnRzRjNjQl9YS3lvRnRXejdtS2xnOVRwU2VPNVZOQ1ZyVW5nel9MWmxTNm5UMVhMbFZKWllnUEc5R3BQdDdEc0hOMHppbTI5alBDT3ltUjZ3UFVSNm9CTTR1NktVaXRwMlo4VjBGSzlqODBMdl9jS1U1MlgtdlZZMXo3TFVRQ1czdHdQbHhWVUl5U2pNa0F1czloS1RRbTQwbDJoN3N1NF9TaGhmQmNEUDNwUWVzbWJjVFJPUGZmdnFreFc0M0dPMGlvOF9DYVhWaGt5Wl90LUZEZEJLb0ZnNThIeUNOSnNsWU5oN2RHaXozYU1VdWFfakJXeEU0XzZheFI5WWl3aDFLNkw3SmM4UWUwQk9RWGp4RzJ2bElDWGNHQS52bkNVSXVXVU9rbU1TbzZCZWtUOXdRIn0="
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response)


from django.shortcuts import render


def voucher_view(request):
    try:
        vouchers = get_vou()
        return render(request, 'novusapp/xoxo/vouchers.html', {'vouchers': vouchers})
    except Exception as e:
        return render(request, 'novusapp/xoxo/vouchers.html', {'error': str(e)})
def voucher_view(request):
    try:
        vouchers = get_vou()
        return render(request, 'vouchers/voucher.html', {'vouchers': vouchers})
    except Exception as e:
        return render(request, 'vouchers/voucher.html', {'error': str(e)})
