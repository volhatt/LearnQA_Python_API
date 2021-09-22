"""
requests to https://playground.learnqa.ru/ajax/api/compare_query_type with
4 HTTP methods - POST, GET, PUT, DELETE
create payload method with request method

"""
import requests


# 1 http request any type, no method parameter, print response text
res1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"#1 Response text is {res1.text}")
print(f"#1 Response is {res1}")
# Response: "Wrong method provided"

# 2 http request HEAD, print result text
res2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"#2 Response text is {res2.text}")
print(f"#2 Response is {res2}")
# Response: None

# 3 correct http request
payload = {"method": "POST"}
res3 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type",
                     data=payload)
print(f"#3 Response text is {res3.text}")
print(f"#3 Response is {res3}")
# Response: {"success":"!"}

# 4 check all combination method / request type
print("== == == #4 == == == ")
end_pont = "https://playground.learnqa.ru/ajax/api/compare_query_type"
requests_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'TRACE', 'PATCH']
payloads = [
    {"method": "GET"},
    {"method": "POST"},
    {"method": "PUT"},
    {"method": "DELETE"},
    {"method": "HEAD"},
    {"method": "TRACE"},
    {"method": "PATCH"},
]
# store invalid response
errors = []
for method in requests_methods:
    for payload in payloads:
        if method == "GET":
            res = requests.get(end_pont, params=payload)
        elif method == "POST":
            res = requests.post(end_pont, data=payload)
        elif method == "PUT":
            res = requests.put(end_pont, data=payload)
        elif method == "DELETE":
            res = requests.delete(end_pont, data=payload)
        print(f"* * * *\nMethod {method}\npayload {payload}\nResponse is {res.text}")
        if method == payload["method"]:
            expected_response = '{"success":"!"}'
        else:
            expected_response = "Wrong method provided"
        # collect errors
        if expected_response != res.text:
            errors.append({method: payload.get("method")})

# print(errors)
print("Server response is not correct when:")
for error in errors:
    for k, v in error.items():
        print(f"method in payload {v} with request {k}")

