/*Managed Identity
  Add both api app service slots as a managed identity*/

CREATE USER [aislingsbustours-bookingapi/slots/staging] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aaislingsbustours-bookingapi/slots/staging];
GRANT SELECT TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON [dbo].[timetable_procedure] TO [aislingsbustours-bookingapi/slots/staging];


CREATE USER [aislingsbustours-bookingapi] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aislingsbustours-bookingapi];
GRANT SELECT TO a[aislingsbustours-bookingapi];
GRANT EXECUTE ON [dbo].[timetable_procedure] TO [aislingsbustours-bookingapi];

