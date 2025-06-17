import httpx
import json
import uuid
from settings import API_TOKEN, BASE_URL
import base64

def get_headers():
    token = base64.b64encode((f'apikey:{API_TOKEN}').encode('ascii')).decode('ascii')
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def list_projects():
    url = f"{BASE_URL}/api/v3/projects"
    try:
        response = httpx.get(url, headers=get_headers(), timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error fetching projects: {e}")
        return []

    return [
        {
            "id": proj["id"],
            "name": proj["_links"]["self"]["title"]
        }
        for proj in response.json().get("_embedded", {}).get("elements", [])
    ]

def list_project_users(project_id: int):
    try:
        project_url = f"{BASE_URL}/api/v3/projects/{project_id}"
        project_res = httpx.get(project_url, headers=get_headers(), timeout=10.0)
        project_res.raise_for_status()
        memberships_href = project_res.json()["_links"]["memberships"]["href"]
        if memberships_href.startswith("/"):
            memberships_href = BASE_URL + memberships_href

        memberships_res = httpx.get(memberships_href, headers=get_headers(), timeout=10.0)
        memberships_res.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Failed to fetch project users: {e}")
        return []

    users = []
    for membership in memberships_res.json().get("_embedded", {}).get("elements", []):
        principal = membership.get("_links", {}).get("principal", {})
        if "href" in principal:
            user_id = principal["href"].rsplit("/", 1)[-1]
            users.append({
                "id": user_id,
                "name": principal.get("title", "Unknown")
            })
    return users

def create_work_package(title, project_id, user_id, description):
    print(f"Running task: {title}")

    data = {
        "subject": f"{title} ({uuid.uuid4().hex[:6]})",
        "description": {
            "format": "markdown",
            "raw": description,
        },
        "_links": {
            "project": { "href": f"/api/v3/projects/{project_id}" },
            "type": { "href": "/api/v3/types/1" },
            "assignee": { "href": f"/api/v3/users/{user_id}" }
        }
    }

    try:
        response = httpx.post(f"{BASE_URL}/api/v3/work_packages", headers=get_headers(), json=data, timeout=10.0)
        response.raise_for_status()
        print(f"Created work package for {title}")
    except httpx.HTTPError as e:
        print(f"Failed to create task '{title}': {e}")
