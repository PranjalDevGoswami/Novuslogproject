import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

XOXO_CLIENT_ID = "fbc574677ab033b7f38861e6fd956384"
XOXO_SECRET_ID = "4n1m973k3lrqhaoc0k4bq7vfbtos09k4eocm"

@api_view(['GET'])
def get_vouchers(request,filter_value):
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
                },
                "filters": [
                {
                    "key": "country",
                    "value": filter_value
                }
            ]
            }
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MjExMjI0MzYwNzMsImV4cGlyZXNBdCI6MTcyMjQxODQzNjA3MywidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJazFCY2pKNE1uWXpOMDV5VmtkME1rMUNVa3BNY2taU2RFb3RWMHBGYkVGaWMwUnhUVU5QV1VnNWIyc2lMQ0o1SWpvaVNWVktibkZRU0ZCWVoxcGtVVTlETW01bGRIQjRiMjVyTWpGdE1sTjFSa3BJYkRsamVrbDJRVVZ0VFNKOWZRLi5pUjBQX3E4MVg5dTJCN3dqSzZlZC1BLjY3QXdKYTVBVlFFT2pMcnNoa1JjX0ZuTjlvck5rZ19VTTRfM1RjeWpFTjNzLTlyQlVhOHVNaVM2RzVDV0drV1R6VXV5dG5WeFRzdGRzSzNuQTdOOC1iY0JfQkxjYnd0ZnNMUE5nTU1tM3QzazFxTXhEM2RwRkZ1b1lmNlNIY0EzcngwNDlkTi1NM1RwZXU2Q1JjUU5nN05IMmplZUxqT2dZM1FydklTRV92ZHpHMGpiNDUxaFBWVU1CN09SQ1VNeHB2VENWUWxBRHBTQ1pjZGlNWnU3Tl9SbVk0Z1ZSTU1wR20yRVJXRmRaNmFweld4UWxxYUZ5S3A0X3pmVHF2blY5Y3JPaEJqRGFFUDQ0QWtlaWZHTHB6aEhlZEdLaUt5UXA3SFJTT3JUYWxtN1pyQ3JJWFBGQllnN2VsNV83MmhCR2Y0eHJOUXFfelZobE5uZGNzWE9rMTdvZWNUOG1qeHNSN0lUdWhVbXFYajNSMThmS2JmN1g2bWRVTlJnNHFVWU16VjFhZ3plMms3WGdWN2JuNzI2cU1PNE1nRk5yNDZRWk42dnh5QWhBZVpqYUc3dEtYT0JjX1FUQlRMY0duUHVDS2VEbEpxaFJoOG9CbGhwdXlpd1hSYVV2c0VhUG9TaXBpdEM5aFphWHRqM1IwSV9tWi1jREluUWktSlpzU0JzYUFMQjhoY3BwcGg5QU5kT0Z2VWs0N1NkN3YwSHJ6bTd2ZTJNc1hMUzFEWnVtOVljNVZVblV2dm5neThuLTh2S1p4SmhJTlVCbHo3c3M0TEU2YTNCNkt4bl94dUg5LXpzZmdPRWZTTXlVQU8yc3BBNExMaHNJM3UxbEZKdXFCUGtWQ0VtZW1EV2MyR2pOZHVyajgzaXJQeVVwcUtSN1hRRWJCUVNlUFgtUW5ERnAxTWg4TW05UXBZYks3bnJKbDNHa2ZMeXpHLUdhQTBCbmQ0Vk44QUZock5NRURSZ0tjMkJZZkFkU0NINmZoSDBDUS1NX1RIUlVETXROVks4RzVPUmcyWWpxQWVtaklodjVhTmJfR2ZmdTdvbmdudk4tclZsbHIwRzJtNzdTUnNrUVdTOFZ1YnlvaTNDdUN5aTF3N2tyc2szMmgySXVNSFBvSTJjdWRYSEdQR2d2OE00dHZQeFgwOE84VWkzUHlFLnpPUF9QSXR0MkFyX0YzV3NWbG04d0EifQ=="
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def get_Order(request):
    url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api/"
    payload = {
        "query": "plumProAPI.mutation.getOrderDetails",
        "tag": "plumProAPI",
        "variables": { "data": {
                "poNumber": "PO123",
                "orderId": 123,
                "sendMailToReceiver": 0
            } }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTk4MTczMjk0NzgsImV4cGlyZXNBdCI6MTcyMTExMzMyOTQ3OCwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbEZQVFZCSlJYQlBOemw1YkdJek5VeEpXVEpVV2s5QldsTmtZa0o1UjAxSE1IUktXR1IwVldKbGFGVWlMQ0o1SWpvaVozRmZRMUF6Ulc5V1NIQkhNVWQ0VUVnNGVXbHBPSHBoZG10VFp6SktSamx1UW5GUk5VNXNlblpaWnlKOWZRLi56SXNJR2NrMXhqdmlENWp1aElNTG5nLmlyM3V4RVVHakhON3dSMnZFdFFIQUwxNFMyNXpVS09DV2NWQkFaamhlZW83T0VOMDF6YjNnTHc2YTM5SlE2TGRwQi1PMmljRHk0WXBIb0VmWE1iUnVZeW5rcTdkcTFEdVAwM2pFcW1TSEJvMkloQno5aWxkb0xvMnRhT1lPcFBDRzFFQlFETU40d2V5Q0cydG1uLUJqTHFjVFFDQzA1YzhMYmdkaDhTQUhld0VNUEE1M0lDcU5ZQ1I4ME9YTkJBUGMtV2g0cFI3enN3Z1NpNmRrd0tUZlBSa2hPYVQ2ckEwNTRweHVqYjEwcjVwd2hMSkhJM0dLRE16aHlWV0tJMFVIT2MzYXFMWXExcWszbjZsUDN1QWlNTk1yc0dyejhmaHF3Z1VSbWFpZDZ5X3o2MmtNOFhVX0FVaFI4Q2ZTR2NFc2VvYnJxSGVGVUFfSm12Q1k0UDJKRmJmN2xTQ2Zuc2lLZmFNWWxveVJzbkM1TGphV1BKaWg1UzBpU29rNGFLcmxQR0FFdFRTbzRqeXdRaksydHdJQUg2cmVuQ1liR2RyWEVZbDJVd0dZbUpwd2w0c3FmSWx4dXJzUDBJczFZNllqY3Q1TlE1TGg4TkVBbDBxdmFBS1FWeVdKVTg5X3BySU1DLU96eUZqbU9sZy1pcFAwcVhsUmZhdVltaFNCM0NaTmtXNU80bGJZWEFyaGVHaHFHM2lEVnpPaVFOTU5NejRMSURoOEFlRDNrVDdMX3ZLWXNWdXpveGptT0xrMk1oWlpQSVp6dTVNUW5IdlNqNkhWNFMtQTJzc25aZ0YzRmQyN1hCQWJhcE1mQl9NazNGcld6aXN1RlhxUkpVcU4yR3g2YkVNc3BDUUlXdWhlMGlQVndjdFprUVdrbWM4UjlKUmRfd3QzMXhxMVd2QlIwRjNldmljeVhjaXZtQlJNZVRWaTJoOFRBLWFtNERjS042dEVwaFlyNnotY0FXYkFUUFNEQWNoa0xYTUtHSTZETjVSZGdZenZKVjZLYlloVmxvVmlTODJmYWc0bHQtZ1F5RlMyWXBxalRaejlyTUItOXMtQVNNY2p6eFc4V1lTdTRKamJBekpzckJoRkxOaW5wUFhlMlJWNzJVdmpkNHJlRkFNLXQ3UzNyQmVXc21LSm1fTEd3MlhBanZnTURHdW5GbXZZbkNMNFV5RXJ0RzJpLXpyRkVxYXFCZmN1REVNMnRsRDFaREZ3Zy5SLU5sYVNxUk95XzhadHBVYVMyaFhnIn0="
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
    
    
    

@api_view(['POST'])
def place_order(request):
    url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api/"
    payload = {
        "query": "plumProAPI.mutation.placeOrder",
        "tag": "plumProAPI",
        "variables": {
            "data": {
                "productId": request.data.get('productId', 51699),
                "quantity": request.data.get('quantity', 1),
                "denomination": request.data.get('denomination', 20),
                "poNumber": request.data.get('poNumber', "PO12662"),
                "notifyAdminEmail": request.data.get('notifyAdminEmail', 0),
                "email": request.data.get('email', "tomarpramod0532@gmail.com"),
                "contact": request.data.get('contact', "+91-7835864271"),
                "tag": request.data.get('tag', "b2cf")
            }
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MjExMjI0MzYwNzMsImV4cGlyZXNBdCI6MTcyMjQxODQzNjA3MywidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJazFCY2pKNE1uWXpOMDV5VmtkME1rMUNVa3BNY2taU2RFb3RWMHBGYkVGaWMwUnhUVU5QV1VnNWIyc2lMQ0o1SWpvaVNWVktibkZRU0ZCWVoxcGtVVTlETW01bGRIQjRiMjVyTWpGdE1sTjFSa3BJYkRsamVrbDJRVVZ0VFNKOWZRLi5pUjBQX3E4MVg5dTJCN3dqSzZlZC1BLjY3QXdKYTVBVlFFT2pMcnNoa1JjX0ZuTjlvck5rZ19VTTRfM1RjeWpFTjNzLTlyQlVhOHVNaVM2RzVDV0drV1R6VXV5dG5WeFRzdGRzSzNuQTdOOC1iY0JfQkxjYnd0ZnNMUE5nTU1tM3QzazFxTXhEM2RwRkZ1b1lmNlNIY0EzcngwNDlkTi1NM1RwZXU2Q1JjUU5nN05IMmplZUxqT2dZM1FydklTRV92ZHpHMGpiNDUxaFBWVU1CN09SQ1VNeHB2VENWUWxBRHBTQ1pjZGlNWnU3Tl9SbVk0Z1ZSTU1wR20yRVJXRmRaNmFweld4UWxxYUZ5S3A0X3pmVHF2blY5Y3JPaEJqRGFFUDQ0QWtlaWZHTHB6aEhlZEdLaUt5UXA3SFJTT3JUYWxtN1pyQ3JJWFBGQllnN2VsNV83MmhCR2Y0eHJOUXFfelZobE5uZGNzWE9rMTdvZWNUOG1qeHNSN0lUdWhVbXFYajNSMThmS2JmN1g2bWRVTlJnNHFVWU16VjFhZ3plMms3WGdWN2JuNzI2cU1PNE1nRk5yNDZRWk42dnh5QWhBZVpqYUc3dEtYT0JjX1FUQlRMY0duUHVDS2VEbEpxaFJoOG9CbGhwdXlpd1hSYVV2c0VhUG9TaXBpdEM5aFphWHRqM1IwSV9tWi1jREluUWktSlpzU0JzYUFMQjhoY3BwcGg5QU5kT0Z2VWs0N1NkN3YwSHJ6bTd2ZTJNc1hMUzFEWnVtOVljNVZVblV2dm5neThuLTh2S1p4SmhJTlVCbHo3c3M0TEU2YTNCNkt4bl94dUg5LXpzZmdPRWZTTXlVQU8yc3BBNExMaHNJM3UxbEZKdXFCUGtWQ0VtZW1EV2MyR2pOZHVyajgzaXJQeVVwcUtSN1hRRWJCUVNlUFgtUW5ERnAxTWg4TW05UXBZYks3bnJKbDNHa2ZMeXpHLUdhQTBCbmQ0Vk44QUZock5NRURSZ0tjMkJZZkFkU0NINmZoSDBDUS1NX1RIUlVETXROVks4RzVPUmcyWWpxQWVtaklodjVhTmJfR2ZmdTdvbmdudk4tclZsbHIwRzJtNzdTUnNrUVdTOFZ1YnlvaTNDdUN5aTF3N2tyc2szMmgySXVNSFBvSTJjdWRYSEdQR2d2OE00dHZQeFgwOE84VWkzUHlFLnpPUF9QSXR0MkFyX0YzV3NWbG04d0EifQ=="
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    





