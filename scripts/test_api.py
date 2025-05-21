#!/usr/bin/env python
"""
Test script to verify the API functionality.
"""

import asyncio
import httpx
import json
from typing import Dict, Any, Optional

# API base URL
BASE_URL = "http://localhost:48001"

# Admin credentials
USERNAME = "admin"
PASSWORD = "adminpassword"


async def get_token() -> str:
    """Get JWT token for authentication."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/auth/token",
            data={"username": USERNAME, "password": PASSWORD},
        )
        
        if response.status_code != 200:
            print(f"Failed to get token: {response.status_code}")
            print(response.text)
            exit(1)
            
        data = response.json()
        return data["access_token"]


async def make_request(
    method: str,
    endpoint: str,
    token: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Make a request to the API."""
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    async with httpx.AsyncClient() as client:
        if method.lower() == "get":
            response = await client.get(
                f"{BASE_URL}{endpoint}", headers=headers, params=params
            )
        elif method.lower() == "post":
            response = await client.post(
                f"{BASE_URL}{endpoint}", headers=headers, json=data
            )
        else:
            print(f"Unsupported method: {method}")
            exit(1)
            
        return {
            "status_code": response.status_code,
            "data": response.json() if response.status_code < 400 else response.text,
        }


async def test_health_check():
    """Test the health check endpoints."""
    print("Testing health check...")
    
    # Basic health check
    response = await make_request("GET", "/api/v1/health")
    print(f"Basic health check: {response['status_code']}")
    print(json.dumps(response["data"], indent=2))
    
    # Detailed health check
    response = await make_request("GET", "/api/v1/health/details")
    print(f"Detailed health check: {response['status_code']}")
    print(json.dumps(response["data"], indent=2))


async def test_auth():
    """Test the authentication endpoints."""
    print("\nTesting authentication...")
    
    # Get token
    token = await get_token()
    print(f"Got token: {token[:20]}...")
    
    # Get current user
    response = await make_request("GET", "/api/v1/auth/me", token=token)
    print(f"Current user: {response['status_code']}")
    print(json.dumps(response["data"], indent=2))


async def test_users():
    """Test the users endpoints."""
    print("\nTesting users API...")
    
    # Get token
    token = await get_token()
    
    # List users
    response = await make_request("GET", "/api/v1/users", token=token)
    print(f"List users: {response['status_code']}")
    print(json.dumps(response["data"], indent=2))
    
    # Create a new user
    new_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "full_name": "Test User",
    }
    
    response = await make_request("POST", "/api/v1/users", token=token, data=new_user)
    print(f"Create user: {response['status_code']}")
    print(json.dumps(response["data"], indent=2))


async def main():
    """Main function to run all tests."""
    await test_health_check()
    await test_auth()
    await test_users()


if __name__ == "__main__":
    asyncio.run(main())
