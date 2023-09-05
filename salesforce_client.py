import httpx
from constants import Constants

class SalesforceClient:
    def __init__(self):
        self.token = None
        self.instance_url = None

    async def authorize_async(self):
        response = await self.async_auth_request()
        self.token = response['access_token']
        self.instance_url = response['instance_url']

    async def async_auth_request(self):
        data = {
            'grant_type': 'password',
            'client_id': Constants.CONSUMER_KEY,
            'client_secret': Constants.CONSUMER_SECRET,
            'username': Constants.USERNAME,
            'password': Constants.PASSWORD + Constants.TOKEN
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(Constants.TOKEN_REQUEST_ENDPOINTURL, data=data)
            response.raise_for_status()
            return response.json()

    async def async_get_request(self, token, url, query):
        headers = {
            'Authorization': f'Bearer {token}'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url + Constants.TOKEN_REQUEST_QUERYURL + query, headers=headers)
            return response.text

    async def async_insert_request(self, token, instance_url, object_name, data):
        url = f"{instance_url}{Constants.TOKEN_REQUEST_POSTURL}{object_name}/"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.text

    async def async_update_request(self, token, instance_url, object_name, record_id, data):
        url = f"{instance_url}{Constants.TOKEN_REQUEST_POSTURL}{object_name}/{record_id}"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, headers=headers, json=data)  # Typically, updates are done with PATCH
            response.raise_for_status()
            return response.text

    async def async_upsert_request(self, token, instance_url, object_name, data, record_id=None):
        if record_id is None:
            return await self.async_insert_request(token, instance_url, object_name, data)
        else:
            return await self.async_update_request(token, instance_url, object_name, record_id, data)

    async def async_delete_request(self, token, instance_url, object_name, record_id):
        url = f"{instance_url}{Constants.TOKEN_REQUEST_POSTURL}{object_name}/{record_id}"
        headers = {
            'Authorization': f'Bearer {token}'
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            response.raise_for_status()
            return response.text

    async def async_undelete_request(self, token, instance_url, record_ids):
        url = f"{instance_url}{Constants.TOKEN_REQUEST_POSTURL}undelete"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {
            'ids': record_ids
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.text