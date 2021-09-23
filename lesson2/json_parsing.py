import json  # no need to import if requests

string_as_json_format = '{"answer": "Hello, User"}'
# parsing json
obj = json.loads(string_as_json_format)
print(obj['answer'])

key = "answer"
if key in obj:
    print(obj[key])
else:
    print(f"There is no {key} in JSON file")
