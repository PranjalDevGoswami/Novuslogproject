import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

XOXO_CLIENT_ID = "fbc574677ab033b7f38861e6fd956384"
XOXO_SECRET_ID = "4n1m973k3lrqhaoc0k4bq7vfbtos09k4eocm"

@api_view(['GET'])
def get_vouchers(request):
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
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTczOTkyMTgwMzIsImV4cGlyZXNBdCI6MTcxODY5NTIxODAzMiwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbWxsWkVSR1VuUkhhekJTUm05V09XaFNiRVZ5WDJ4TmNIRjVRV3B6VFMwNFlWUmhkVXR5ZEhjM09ITWlMQ0o1SWpvaU1VRmFhVlY2ZFhoNVVETkVWbFJRYURKNFgwbGZNRGd4Ylc5YU9Fc3pZVjkzTVV4Tk5VdDFXRFJ0VFNKOWZRLi41NktITElKZjJXSmI1UHl4el9vZ05nLkh0R0laMjlLMXpBZW94cUktSHJhQzV3aloyRDFHMktqNDBqYXlmTXZZamtwRFpTMm1ROFZ0ek55MkpENFQzakM2TXN3bENiYll5cktkdzYzMGJMeWczb3hMUUY3T0FCUnJfMF8waTBGeHZMeUNfbHJ3QzVyZHV0Q0NPcTcwX3BTUkpMUHpXMUdLR2FfRUZxN0FmVng0ak1WdFVnd1dVbU9WNzU5SXdNUTBfdGZJdTREd0VocFFqSVdUMzB3Y2hGRWc5cHk3ajIyZDdQQmJtVXl2RHJLUUVuMGZHNXFHNWJtQ2l0TXJxX1ctdkhiU1hZT1QyaVZ3eDZUSHhldGt0ZEhaTkJNVk1QWXNjYUFkWC10eDFSRFljS3U1TFluZXpnNlZyMk1EX3pkaXhTVks0cUZQVjYwZno5cktJS1BtSlRmQnRTNGtmQW9uMXdDNEIteUFrdG92Sm0xcWlFYmtkd3NxZjUzS2daUHBVRFlneTg4bWtldEl2NkxneExvZkRQbURaMXc4cTA2QWVGZW83YkI2S2pBOXFuUGFDZVdXdFppSGhPckpfYTczLV9maEY1aVR1RFN4Z3p2WjVzVE5fMlhwMzdGdjZSOU9vUUVyc1M4MUdtVERXX0FMeG9oeXNZS0NzYURiRERLZE1vbGo0WlRFbjhKMjJkNXlzU0lRbEc0UGk4ZXFkVmhIX3ZYc0MzMGc3eTg5bVBrUHdEWktZblZoRkFUckpzd0t4dWZfeVo5Ym5zMHE0WEJUVDUyRGRqUzhzTUViZXptaTRwOW15VVZEaWxaOHNuOXJfOXdtZEQwVDhpQTdBZGFtMGs5aWRsTlFSM1puNjd4c3BPLXpZVHR2UVlqTy0zWVRMOVpzQ2N0czhrSHJvdmkxN3g5UUpRb1AxYlpscTNySEZqXzRScVF2SEREbURJcllsX2cyLVgyY2JwTGNBOVlMQXNtTklaeUFnSXBiZUw2MHpWLWpZUmdLd3AxZ2Q1aWhGYjFqcmZvSERyaGhCMUpUdFAzaElvbmJvUnZTMWJVQW1lNThBNXNwb0FCTHhPU1VOQnpubVhmNWFDQmczd3laWHBTSmN1bnRSME8zRG9TYlVIYXpnRDZDSFg1aUd5Wi16SnFzM1NLNzROWnFlTDc0ajVQMUhIV2tHNkVLcEhQc09kYW1RQVBtdGoxUVVnSEoyWHpsZC0yWXlPc3VMSGxHUTQ2WWRBbzlyajIyUS5FaXdCdnZvTENkUXZFTlEtY212Q01BIn0="
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
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTczOTkyMTgwMzIsImV4cGlyZXNBdCI6MTcxODY5NTIxODAzMiwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbWxsWkVSR1VuUkhhekJTUm05V09XaFNiRVZ5WDJ4TmNIRjVRV3B6VFMwNFlWUmhkVXR5ZEhjM09ITWlMQ0o1SWpvaU1VRmFhVlY2ZFhoNVVETkVWbFJRYURKNFgwbGZNRGd4Ylc5YU9Fc3pZVjkzTVV4Tk5VdDFXRFJ0VFNKOWZRLi41NktITElKZjJXSmI1UHl4el9vZ05nLkh0R0laMjlLMXpBZW94cUktSHJhQzV3aloyRDFHMktqNDBqYXlmTXZZamtwRFpTMm1ROFZ0ek55MkpENFQzakM2TXN3bENiYll5cktkdzYzMGJMeWczb3hMUUY3T0FCUnJfMF8waTBGeHZMeUNfbHJ3QzVyZHV0Q0NPcTcwX3BTUkpMUHpXMUdLR2FfRUZxN0FmVng0ak1WdFVnd1dVbU9WNzU5SXdNUTBfdGZJdTREd0VocFFqSVdUMzB3Y2hGRWc5cHk3ajIyZDdQQmJtVXl2RHJLUUVuMGZHNXFHNWJtQ2l0TXJxX1ctdkhiU1hZT1QyaVZ3eDZUSHhldGt0ZEhaTkJNVk1QWXNjYUFkWC10eDFSRFljS3U1TFluZXpnNlZyMk1EX3pkaXhTVks0cUZQVjYwZno5cktJS1BtSlRmQnRTNGtmQW9uMXdDNEIteUFrdG92Sm0xcWlFYmtkd3NxZjUzS2daUHBVRFlneTg4bWtldEl2NkxneExvZkRQbURaMXc4cTA2QWVGZW83YkI2S2pBOXFuUGFDZVdXdFppSGhPckpfYTczLV9maEY1aVR1RFN4Z3p2WjVzVE5fMlhwMzdGdjZSOU9vUUVyc1M4MUdtVERXX0FMeG9oeXNZS0NzYURiRERLZE1vbGo0WlRFbjhKMjJkNXlzU0lRbEc0UGk4ZXFkVmhIX3ZYc0MzMGc3eTg5bVBrUHdEWktZblZoRkFUckpzd0t4dWZfeVo5Ym5zMHE0WEJUVDUyRGRqUzhzTUViZXptaTRwOW15VVZEaWxaOHNuOXJfOXdtZEQwVDhpQTdBZGFtMGs5aWRsTlFSM1puNjd4c3BPLXpZVHR2UVlqTy0zWVRMOVpzQ2N0czhrSHJvdmkxN3g5UUpRb1AxYlpscTNySEZqXzRScVF2SEREbURJcllsX2cyLVgyY2JwTGNBOVlMQXNtTklaeUFnSXBiZUw2MHpWLWpZUmdLd3AxZ2Q1aWhGYjFqcmZvSERyaGhCMUpUdFAzaElvbmJvUnZTMWJVQW1lNThBNXNwb0FCTHhPU1VOQnpubVhmNWFDQmczd3laWHBTSmN1bnRSME8zRG9TYlVIYXpnRDZDSFg1aUd5Wi16SnFzM1NLNzROWnFlTDc0ajVQMUhIV2tHNkVLcEhQc09kYW1RQVBtdGoxUVVnSEoyWHpsZC0yWXlPc3VMSGxHUTQ2WWRBbzlyajIyUS5FaXdCdnZvTENkUXZFTlEtY212Q01BIn0="
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
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTczOTkyMTgwMzIsImV4cGlyZXNBdCI6MTcxODY5NTIxODAzMiwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbWxsWkVSR1VuUkhhekJTUm05V09XaFNiRVZ5WDJ4TmNIRjVRV3B6VFMwNFlWUmhkVXR5ZEhjM09ITWlMQ0o1SWpvaU1VRmFhVlY2ZFhoNVVETkVWbFJRYURKNFgwbGZNRGd4Ylc5YU9Fc3pZVjkzTVV4Tk5VdDFXRFJ0VFNKOWZRLi41NktITElKZjJXSmI1UHl4el9vZ05nLkh0R0laMjlLMXpBZW94cUktSHJhQzV3aloyRDFHMktqNDBqYXlmTXZZamtwRFpTMm1ROFZ0ek55MkpENFQzakM2TXN3bENiYll5cktkdzYzMGJMeWczb3hMUUY3T0FCUnJfMF8waTBGeHZMeUNfbHJ3QzVyZHV0Q0NPcTcwX3BTUkpMUHpXMUdLR2FfRUZxN0FmVng0ak1WdFVnd1dVbU9WNzU5SXdNUTBfdGZJdTREd0VocFFqSVdUMzB3Y2hGRWc5cHk3ajIyZDdQQmJtVXl2RHJLUUVuMGZHNXFHNWJtQ2l0TXJxX1ctdkhiU1hZT1QyaVZ3eDZUSHhldGt0ZEhaTkJNVk1QWXNjYUFkWC10eDFSRFljS3U1TFluZXpnNlZyMk1EX3pkaXhTVks0cUZQVjYwZno5cktJS1BtSlRmQnRTNGtmQW9uMXdDNEIteUFrdG92Sm0xcWlFYmtkd3NxZjUzS2daUHBVRFlneTg4bWtldEl2NkxneExvZkRQbURaMXc4cTA2QWVGZW83YkI2S2pBOXFuUGFDZVdXdFppSGhPckpfYTczLV9maEY1aVR1RFN4Z3p2WjVzVE5fMlhwMzdGdjZSOU9vUUVyc1M4MUdtVERXX0FMeG9oeXNZS0NzYURiRERLZE1vbGo0WlRFbjhKMjJkNXlzU0lRbEc0UGk4ZXFkVmhIX3ZYc0MzMGc3eTg5bVBrUHdEWktZblZoRkFUckpzd0t4dWZfeVo5Ym5zMHE0WEJUVDUyRGRqUzhzTUViZXptaTRwOW15VVZEaWxaOHNuOXJfOXdtZEQwVDhpQTdBZGFtMGs5aWRsTlFSM1puNjd4c3BPLXpZVHR2UVlqTy0zWVRMOVpzQ2N0czhrSHJvdmkxN3g5UUpRb1AxYlpscTNySEZqXzRScVF2SEREbURJcllsX2cyLVgyY2JwTGNBOVlMQXNtTklaeUFnSXBiZUw2MHpWLWpZUmdLd3AxZ2Q1aWhGYjFqcmZvSERyaGhCMUpUdFAzaElvbmJvUnZTMWJVQW1lNThBNXNwb0FCTHhPU1VOQnpubVhmNWFDQmczd3laWHBTSmN1bnRSME8zRG9TYlVIYXpnRDZDSFg1aUd5Wi16SnFzM1NLNzROWnFlTDc0ajVQMUhIV2tHNkVLcEhQc09kYW1RQVBtdGoxUVVnSEoyWHpsZC0yWXlPc3VMSGxHUTQ2WWRBbzlyajIyUS5FaXdCdnZvTENkUXZFTlEtY212Q01BIn0="
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    