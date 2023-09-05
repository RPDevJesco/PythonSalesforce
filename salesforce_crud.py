from salesforce_client import SalesforceClient
class SalesforceCRUD:
    def __init__(self, token, instance_url):
        self._token = token
        self._instance_url = instance_url
        self._client = SalesforceClient()

    async def get_async(self, query):
        return await self._client.async_get_request(self._token, self._instance_url, query)

    async def create_async(self, object_name, data):
        return await self._client.async_insert_request(self._token, self._instance_url, object_name, data)

    async def update_async(self, object_name, id, data):
        return await self._client.async_update_request(self._token, self._instance_url, object_name, id, data)

    async def upsert_async(self, object_name, data, record_id=None):
        return await self._client.async_upsert_request(self._token, self._instance_url, object_name, data, record_id)

    async def delete_async(self, object_name, id):
        return await self._client.async_delete_request(self._token, self._instance_url, object_name, id)