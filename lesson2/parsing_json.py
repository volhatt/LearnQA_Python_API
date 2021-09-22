import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04' \
        ' 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04' \
        ' 16:41:01"}]}'

obj = json.loads(json_text)

# target text of second message
target_message = obj['messages'][1]['message']
target_message = obj.get('messages')[1]['message']

print(target_message)



