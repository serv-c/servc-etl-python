import json
import os
import time

import requests

API_URL = os.getenv("API_URL", "https://api.servc.io")
API_TOKEN = os.getenv("API_TOKEN", "")
DAG_FILE = os.getenv("DAG_JSON", "dag.json")

if not os.path.exists(DAG_FILE):
    print(f"Error: DAG file '{DAG_FILE}' does not exist.")
    exit(1)
if not API_TOKEN:
    print("Error: api_token variable is not set.")
    exit(1)

dag = {}
with open(DAG_FILE, "r") as f:
    dag = json.load(f)

hdrs = {"Apitoken": API_TOKEN}
request = requests.post(
    url=API_URL,
    json={
        "type": "input",
        "route": "orchestrator",
        "argumentId": "plain",
        "force": True,
        "instanceId": None,
        "inputs": {
            "method": "add_dag",
            "inputs": {
                "dag": json.dumps(dag),
            },
        },
    },
    headers=hdrs,
)
job_id = request.text

# poll for result
response = None
while True:
    time.sleep(2)
    status = requests.get(url=f"{API_URL}/id/{job_id}", headers=hdrs)
    res = status.json() if status.text else {}
    if res and (res["progress"] == 100 or res["isError"]):
        response = res["responseBody"]

        if res["isError"]:
            print("Error:", response)
            exit(1)
        break
print(response)
