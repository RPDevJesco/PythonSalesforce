import asyncio
from salesforce_client import SalesforceClient
from salesforce_crud import SalesforceCRUD

async def main():
    # Using Python's requests, the TLS 1.2 protocol should be used by default for HTTPS requests.
    client = SalesforceClient()

    await client.authorize_async()

    crud_operations = SalesforceCRUD(client.token, client.instance_url)

    account = await crud_operations.get_async("SELECT Id, Name FROM Account LIMIT 1")
    account_data = {
        "Name": "Python Test",
        "Industry": "Software",
        "AccountNumber": "CC977211-E"
    }
    # record_id is an optional parameter for upsert. Without the id, it will do an insert operation; with it, it will update.
    await crud_operations.upsert_async("Account", account_data)

    # Uncomment below line to delete the record with given Id
    # crud_operations.delete("Account", "001Dn00000erJ1LIAU")

    print(account) # Uncomment if you want to print the retrieved account

if __name__ == '__main__':
    asyncio.run(main())
