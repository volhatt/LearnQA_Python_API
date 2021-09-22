import time
import requests
from jsonschema import validate


"""
1. create task
2. request with token when expected status "Job is NOT ready"
3. wait time from previous response
4. call with token when task is completed, check "status" and "result"
"""
end_point = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1 call NO parameter (to create new task )
# expected response json
task_keys = ["second", "token"]
params_task_keys = ["error", "status", "result"]
params = {}

# create task
res1 = requests.get(end_point)
res1_json = res1.json()

# save time and token for another call
wait, token = res1_json.get('seconds'), res1_json.get('token')
print(f"#1\nTask created and will be completed in {wait} second\n")

# create params for future call
params["token"] = token

# 2 call with token before task completed
res2 = requests.get(end_point, params=params)
#res2 = requests.get(end_point, params={"token":"None"})
expected_status = "Job is NOT ready"
actual_status = res2.json().get("status")
print("\n#2\nCall with valid token before task completed")
if expected_status == actual_status:
    print(f"Actual status: {actual_status}")
elif res2.json().get("error"):
    print(f"Something went wrong. Error message: {res2.json().get('error')}")
else:
    print(f"Unexpected status: {actual_status}")

# 3 wait when task is completed
time.sleep(wait)
print(f"\n#3\nWaiting time {wait}")

# 4 call and confirm status that task is completed
print("\n#4\nCall with valid params and expecting task completed")
res3 = requests.get(end_point, params=params)
expected_status = "Job is ready"

try:
    assert expected_status == res3.json().get("status") and res3.json().get("result")
    print(f"Task is completed successfully.\n"
          f"Status is {res3.json().get('status')};\nResult is {res3.json().get('result')}")
except AssertionError:
    if res3.json().get("error"):
        print(f"Something went wrong. Error message: {res3.json().get('error')}")
    elif expected_status != res3.json().get("status"):
        print(f"Something went wrong. Unexpected status: {res3.json().get('status')}")
    elif not res3.json().get("result"):
        print(f"Something went wrong. Result is not available: {res3.json()}")
    else:
        print(f"Something went wrong.")
        print(res3.json())
