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

## Service bus

## Functions
