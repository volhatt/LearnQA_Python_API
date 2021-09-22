import requests

"""
1. Request GET to https://playground.learnqa.ru/api/long_redirect
2. Find how many redirects are in response
3. Print finale URL
"""

res = requests.get("https://playground.learnqa.ru/api/long_redirect")

redirects = len(res.history)

print(f"There are {redirects} redirects {res.history}")
print(f"Finale URL is {res.url}")