import requests

url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api/"

payload = {
    "query": "plumProAPI.mutation.getVouchers",
    "tag": "plumProAPI",
    "variables": { "data": {
            "limit": 10,
            "page": 1,
            "exchangeRate": 1,
            "sort": {
                "field": "name",
                "order": "ASC"
            }
        } }
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MTcwNjM4MjkzMDQsImV4cGlyZXNBdCI6MTcxODM1OTgyOTMwNCwidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJbXA2TjNrNGJVbDRTWFZ1U2tKcWRHNVdZemN4TWxkWWRHRnRUblYyVWtsVlgyaDNlRlpLUjJjMWExa2lMQ0o1SWpvaVlrTlVhWHBhYUZORVZFeEpZV1JKUkRGT01HaFZSRTlFWW01amJURnRlVXh1WTJKcFFXVTJNRkp2V1NKOWZRLi5NY0VEdEc2cmFVMUZDQl9tdGtQVmlBLk1DaHVVQmNjeHZ4cHF0cFl3cFFsdDBLcGticHYzSUNCOWNod0luVGZMQWdDZXhrd2l6dzJ3NmlwMjA5YTdqUGlGWTBTM3V5UENueXdFQXZMbDR6eFlOTzVSVVA0VjdmZnBWQ3lqdFo4dWFFWE5WNzNuUnh1bkxxTEc3UjZyMFNHQVpNOHBDd2pKRUl4QkZCdjlmc04tSnhEN05nNUFrT2dRMDU4VTR6VURhOEhEeVpOX0NKYzVpcDJob2F2dzk5blk3UHpkUkZfUmlSeGFjQjJuNDVyRUo3MGpFNEpLcU84ZzJMa1MyMVgyUEh4d2tmM3FhV2ZPOTlEWWZyV3B1bll0NmxQRm11VENYOGlVTFhFQmVhZTJlZl9OMHVvSUVwN0hrS1dldWk5Y3pDal9kSTQ4cGVCaFNfSm9QaXZqdEdZbmRHYUZhU0U4T0w1T2kyem85LS0yV0FrV0oxMWhnOUNaNHJPMXMwWWd6NlBKcFR4amMwZXpabWxFdnJxVmtUVXRMU1l4TWduY05nWXhYUXpPT1JwdUxtSTdfQ2I4SFZGVWstUFU1UEY3eDFXTkc4dmE5MWJ5R0JkWElDNGhJVk1Day1xeTVlN3lBUHcxVXB2QlJKNFBhWVZ2WWNrdXdjYzJvUVZfeTQ2dWk3SUk1YmlmQ0MyWWZXTTBSM3F1QnliaHg2RnpVajJaRktpSi1CRTFwT2luWlFnSzFqcFZab1VJMER2bG5iNHpPTGZOSUhTSFZXR01ZcWpjeWJIak9QZlFJRXRzMWcySlVxNklWamtsZi14WGI2Tll4ZVo2Nl9iajF0TjFlUHlWblRLa0tUX094UTQ5amVNS0U0dzlhblVOR1VHcnRuMUhxN0EtTFNsVTUwaXZCX2lyZnN1VlVYcVFGcEtGdzlLczdIdU5OMng0UlBySEFySGtrZzVrZ0lCUUV3QmhNYzNsbVVRMGhpLXk0OHdaeEY3Sjlrek16dUQ2M19LNG5qTFZjZzNuREd6dEE4Njhwdl9Ia3hPX2YxTW9zS0V6VS1ocXlOTk1IbmJJd3dSaHpsOXVhT0ZvR2k5bi1mRkpjMXpncVU0WGxtV1lXNFBvUDlVamFhd2RUbGhud081ZEtzOGJtSVBmUDZOQXdMYVpORkpzRldCdnB6eVJuOGtXcmtfdFR0aEVhUXZqS3EyU2dzVS11a3dMdmxPWVEzMzZiQ01DRlU0c1o3S3h3Y0N5Zy4xeWVJSDkyUEtqX2t0VHZPNllMNVhBIn0="
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)