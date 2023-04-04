/*Managed Identity
  Add both api app service slots as a managed identity*/

CREATE USER [aislingsbustours-bookingapi/slots/staging] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aaislingsbustours-bookingapi/slots/staging];
GRANT SELECT TO [aislingsbustours-bookingapi/slots/staging];
GRANT INSERT TO [aislingsbustours-bookingapi/slots/staging];
GRANT DELETE TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON [dbo].[timetable_procedure] TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON [dbo].[get_booking_procedure] TO [aislingsbustours-bookingapi/slots/staging];
GRANT EXECUTE ON SCHEMA::dbo TO [aislingsbustours-bookingapi/slots/staging];

CREATE USER [aislingsbustours-bookingapi] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [aislingsbustours-bookingapi];
GRANT SELECT TO [aislingsbustours-bookingapi];
GRANT INSERT TO [aislingsbustours-bookingapi];
GRANT DELETE TO [aislingsbustours-bookingapi];
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

CREATE PROCEDURE get_passengers_procedure
AS
SELECT * FROM [dbo].[passengers]
GO;

CREATE PROCEDURE get_booking_procedure
AS
SELECT [dbo].[bookings].booking_date, [dbo].[passengers].first_name, [dbo].[passengers].last_name, [dbo].[bookings].seat_number, [dbo].[tours].origin, [dbo].[tours].destination
FROM [dbo].[bookings]
JOIN [dbo].[passengers] ON [dbo].[bookings].email_address=[dbo].[passengers].email_address
JOIN [dbo].[tours] ON [dbo].[bookings].tour_id=[dbo].[tours].tour_id;
GO;

CREATE PROCEDURE search_booking_procedure
    @booking_id INT
AS
BEGIN
    SELECT [dbo].[bookings].booking_id, [dbo].[bookings].booking_date, [dbo].[passengers].first_name, [dbo].[passengers].last_name, [dbo].[tours].origin, [dbo].[tours].destination
		FROM [dbo].[bookings]
		JOIN [dbo].[passengers] ON [dbo].[bookings].email_address=[dbo].[passengers].email_address
		JOIN [dbo].[tours] ON [dbo].[bookings].tour_id=[dbo].[tours].tour_id
  	WHERE [dbo].[bookings].booking_id = @booking_id
END;
GO

CREATE PROCEDURE [dbo].[create_booking_procedure]
    @email_address VARCHAR(100),
	@tour_id INT,
    @booking_id INT OUTPUT
AS
BEGIN
    INSERT INTO [dbo].[bookings] (email_address, booking_date, tour_id)
	OUTPUT inserted.booking_id
    VALUES (@email_address, GETDATE(), @tour_id)
END;

CREATE PROCEDURE [dbo].[delete_booking_procedure]
    @booking_id INT
AS
BEGIN
    DELETE FROM [dbo].[bookings] WHERE booking_id = @booking_id
END;

CREATE PROCEDURE [dbo].[create_passenger_procedure]
    @first_name VARCHAR(50),
    @last_name VARCHAR(50),
    @email_address VARCHAR(100)
	
AS
BEGIN
    INSERT INTO [dbo].[passengers]
    VALUES (@first_name, @last_name, @email_address)
END;
