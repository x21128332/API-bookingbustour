# API - Aisling's Bus tours, using FASTAPI and Azure App Service

This follows on from the README at [Scalable Cloud Programming](https://github.com/x21128332/ScalableCloudProgramming).

## App Service
* Create a new App Service using the App Service plan that you created previously.
* Follow the same steps to create a staging slot.
* In General settings step there is an additional requirement. You need to add a startup command `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

## Managed Identity
1. In the Azure App Service, go to the Identity and turn on System Assigned Managed Identity
2. In the Azure Active Directory go to Enterprise Applications and search for your App Service (you may need to remove some of the preset filters), click on it and copy the exact name of the application listed.

## SQL
1. Using the sqlqueries file run the store procedures in your SQL DB that you created previously.
2. Run the Create USER queries found in the sqlqueries.sql file and replace the names with your application names you copied earlier.
3. Run the queries to give that user the correct access
4. Run the queries to granted the user permissions to SELECT, INSERT and EXECUTE.
5. Run each create store procedure query
6. Update main.py to connect to the database

## Key vault - create
Create a key vault in Azure.

## Service bus
1. Create the service bus in Azure.
Grab your Shared Access Policy key and add your  Primary Connection String and primary key into your key vault.
2. Create a Topic bookings, a subscription called edit and rules called: edit-booking-tool with a property name:
action and value: edit.

## APIM
Create APIM in Azure, map your API there and add all the endpoints.
Apply the policies listed in APIM-policies file. The 1st policy goes on the root of the API, the 2nd policy goes on the PUT endpoint only. These both go into inboud processing policies.
Edit the 2nd policy to include your service bus connection string details and key names from your vault.

## Key vault - add identity
In the Azure Key Vault, go to the Access policies and a new policy for APIM. Give it both "GET" and "LIST" permissions.



This continues with the README at [Azure-Function](https://github.com/x21128332/Azure-Function/tree/master/ServiceBusTopicTrigger1).