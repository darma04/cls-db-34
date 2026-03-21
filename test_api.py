import urllib.request
import json
import uuid

url = "http://127.0.0.1:8080/api/v1/license/verify/"
payload = {
    "license_key": "DUMMY-KEY-NOT-FOUND",  # We will test a bad key first
    "domain": "test.com",
    "ip_address": "127.0.0.1",
    "hardware_id": str(uuid.getnode()),
    "device_name": "Test Script"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print(f"SUCCESS: {result}")
except urllib.error.HTTPError as e:
    result = e.read().decode('utf-8')
    print(f"ERROR {e.code}: {result}")
except Exception as e:
    print(f"EXCEPTION: {e}")
