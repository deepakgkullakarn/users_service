import requests
from fastapi import HTTPException

OPA_URL = "http://localhost:8181/v1/data/authz/allow"

def authorize(user: dict, path: str, method: str):
    payload = {"input": {"user": user, "path": path, "method": method}}
    try:
        response = requests.post(OPA_URL, json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="OPA service error")
        allowed = response.json().get("result", False)
        if not allowed:
            raise HTTPException(status_code=403, detail="Access denied by OPA")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="OPA not reachable")
