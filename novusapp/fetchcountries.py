import requests
from .models import Country

def handle():
    url = "https://stagingaccount.xoxoday.com/chef/v1/oauth/api"
    payload = {
        "query": "plumProAPI.mutation.getFilters",
        "tag": "plumProAPI",
        "variables": { "data": { "filterGroupCode": "Country" } }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJ0b2tlbkNvbnRlbnQiOnsiaXNzdWVkRm9yIjoidGVzdCIsInNjb3BlIjoiIiwiaXNzdWVkQXQiOjE3MjExMjI0MzYwNzMsImV4cGlyZXNBdCI6MTcyMjQxODQzNjA3MywidG9rZW5fdHlwZSI6IlVTRVIifSwiYV90IjoiZXlKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVJVTkVTQzFGVXlJc0ltdHBaQ0k2SW1WdVl5SXNJbVZ3YXlJNmV5SnJkSGtpT2lKRlF5SXNJbU55ZGlJNklsQXRNalUySWl3aWVDSTZJazFCY2pKNE1uWXpOMDV5VmtkME1rMUNVa3BNY2taU2RFb3RWMHBGYkVGaWMwUnhUVU5QV1VnNWIyc2lMQ0o1SWpvaVNWVktibkZRU0ZCWVoxcGtVVTlETW01bGRIQjRiMjVyTWpGdE1sTjFSa3BJYkRsamVrbDJRVVZ0VFNKOWZRLi5pUjBQX3E4MVg5dTJCN3dqSzZlZC1BLjY3QXdKYTVBVlFFT2pMcnNoa1JjX0ZuTjlvck5rZ19VTTRfM1RjeWpFTjNzLTlyQlVhOHVNaVM2RzVDV0drV1R6VXV5dG5WeFRzdGRzSzNuQTdOOC1iY0JfQkxjYnd0ZnNMUE5nTU1tM3QzazFxTXhEM2RwRkZ1b1lmNlNIY0EzcngwNDlkTi1NM1RwZXU2Q1JjUU5nN05IMmplZUxqT2dZM1FydklTRV92ZHpHMGpiNDUxaFBWVU1CN09SQ1VNeHB2VENWUWxBRHBTQ1pjZGlNWnU3Tl9SbVk0Z1ZSTU1wR20yRVJXRmRaNmFweld4UWxxYUZ5S3A0X3pmVHF2blY5Y3JPaEJqRGFFUDQ0QWtlaWZHTHB6aEhlZEdLaUt5UXA3SFJTT3JUYWxtN1pyQ3JJWFBGQllnN2VsNV83MmhCR2Y0eHJOUXFfelZobE5uZGNzWE9rMTdvZWNUOG1qeHNSN0lUdWhVbXFYajNSMThmS2JmN1g2bWRVTlJnNHFVWU16VjFhZ3plMms3WGdWN2JuNzI2cU1PNE1nRk5yNDZRWk42dnh5QWhBZVpqYUc3dEtYT0JjX1FUQlRMY0duUHVDS2VEbEpxaFJoOG9CbGhwdXlpd1hSYVV2c0VhUG9TaXBpdEM5aFphWHRqM1IwSV9tWi1jREluUWktSlpzU0JzYUFMQjhoY3BwcGg5QU5kT0Z2VWs0N1NkN3YwSHJ6bTd2ZTJNc1hMUzFEWnVtOVljNVZVblV2dm5neThuLTh2S1p4SmhJTlVCbHo3c3M0TEU2YTNCNkt4bl94dUg5LXpzZmdPRWZTTXlVQU8yc3BBNExMaHNJM3UxbEZKdXFCUGtWQ0VtZW1EV2MyR2pOZHVyajgzaXJQeVVwcUtSN1hRRWJCUVNlUFgtUW5ERnAxTWg4TW05UXBZYks3bnJKbDNHa2ZMeXpHLUdhQTBCbmQ0Vk44QUZock5NRURSZ0tjMkJZZkFkU0NINmZoSDBDUS1NX1RIUlVETXROVks4RzVPUmcyWWpxQWVtaklodjVhTmJfR2ZmdTdvbmdudk4tclZsbHIwRzJtNzdTUnNrUVdTOFZ1YnlvaTNDdUN5aTF3N2tyc2szMmgySXVNSFBvSTJjdWRYSEdQR2d2OE00dHZQeFgwOE84VWkzUHlFLnpPUF9QSXR0MkFyX0YzV3NWbG04d0EifQ=="
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    filters_data = response.json().get('data', {}).get('getFilters', {}).get('data', [])
    for group in filters_data:
        if group['filterGroupCode'] == 'country':
            for item in group['filters']:
                print('*****DATAAAAA',item['filterValue'])
                Country.objects.get_or_create(
                    filter_value=item['filterValue'],
                    iso_code=item['isoCode'],
                    filter_value_code=item['filterValueCode']
                )

    print('Successfully fetched and saved country data')

