import requests
from jsonschema import validate


#response = requests.get("https://playground.learnqa.ru/api/get_text")
#print(response.text)

print("Hello from Olga Kameneva")

# request hello
print(f"== request hello == ")
"""
payload = {"name": "User"} - works only with GET ???

res = requests.get("http://playground.learnqa.ru/api/hello", params=payload)
parsed_response_text = response.json()
print(parsed_response_text["answer"])
"""

print(f"== request with not json answer  == ")
# but if we not sure if response json
# if not json - returns error then:
"""
from json.decoder import JSONDecodeError
res = requests.get("http://playground.learnqa.ru/api/get_text")

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")
"""
# === requests types
print("==== type check ====")
res = requests.post("https://playground.learnqa.ru/api/check_type")
print(res.text)
#print(res.history)
#print(res.history[0].request.method)
#print(res.url)

# errors playing
print("==== Error check ====")
res = requests.post("http://playground.learnqa.ru/api/get_500")
print(res.status_code)
print(res.text)

print("==== Redirect check ====")
res = requests.post("http://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_res = res.history[0]
second_res = res
print(first_res.url)
print(second_res.url)

# using headers
print("==== headers as data  ====")
headers = {"some_headers": "123"}
res = requests.get("http://playground.learnqa.ru/api/show_all_headers", headers=headers)
print(res.text)
print(res.headers)

print("==== get and pass authorization cookie  ====")
payload = {"login":"secret_login", "password":"secret_pass"}
res1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
cookie_value = res1.cookies.get('auth_cookie')
cookies = {}
if cookie_value is not None:
    cookies.update({"auth_cookie": cookie_value})
res2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(res.status_code)
print(res.cookies)
print(res.headers)  # appears 'Set-Cookie' with request to save authorization cookie
print(f"Response 2  {res2.text}")