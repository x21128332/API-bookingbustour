/*Managed Identity
  Add both api app service slots as a managed identity*/

CREATE USER [aislingsbustours-bookingapi/slots/staging] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aaislingsbustours-bookingapi/slots/staging];
GRANT SELECT TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON [dbo].[timetable_procedure] TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON [dbo].[get_booking_procedure] TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON SCHEMA::dbo TO [aislingsbustours-bookingapi/slots/staging];

CREATE USER [aislingsbustours-bookingapi] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aislingsbustours-bookingapi];
GRANT SELECT TO a[aislingsbustours-bookingapi];
GRANT EXECUTE ON [dbo].[timetable_procedure] TO [aislingsbustours-bookingapi];
GRANT EXECUTE ON [dbo].[get_booking_procedure] TO [aislingsbustours-bookingapi];
GRANT EXECUTE ON SCHEMA::dbo TO [aislingsbustours-bookingapi];


/*creating store PROCEDURE */
CREATE PROCEDURE timetable_procedure
AS
select [dbo].[tours].origin, [dbo].[tours].destination, [dbo].[timetables].departure_time, [dbo].[timetables].arrival_time
from [dbo].[timetables]
JOIN [dbo].[tours] on [dbo].[timetables].tour_id=[dbo].[tours].tour_id;
GO;

CREATE PROCEDURE get_booking_procedure
AS
SELECT [dbo].[bookings].booking_date, [dbo].[passengers].first_name, [dbo].[passengers].last_name, [dbo].[bookings].seat_number, [dbo].[tours].origin, [dbo].[tours].destination
FROM [dbo].[bookings]
JOIN [dbo].[passengers] ON [dbo].[bookings].passenger_id=[dbo].[passengers].passenger_id
JOIN [dbo].[tours] ON [dbo].[bookings].tour_id=[dbo].[tours].tour_id;
GO;

CREATE PROCEDURE search_booking_procedure
    @booking_id INT
AS
BEGIN
    SELECT [dbo].[bookings].booking_id, [dbo].[bookings].booking_date, [dbo].[passengers].first_name, [dbo].[passengers].last_name, [dbo].[bookings].seat_number, [dbo].[tours].origin, [dbo].[tours].destination
		FROM [dbo].[bookings]
		JOIN [dbo].[passengers] ON [dbo].[bookings].passenger_id=[dbo].[passengers].passenger_id
		JOIN [dbo].[tours] ON [dbo].[bookings].tour_id=[dbo].[tours].tour_id
  	WHERE [dbo].[bookings].booking_id = @booking_id;
END;
GO