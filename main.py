import pyodbc
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
app = FastAPI(title="Aisling Bus Tours API")

def get_db_connection():
    server = 'sqlaislingsbustour.database.windows.net'
    database = 'sqlaislingsbustour'
    #using managed identity so no need for user + pass
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:sqlaislingsbustour.database.windows.net,1433;Database=sqlaislingsbustour;Authentication=ActiveDirectoryMsi; Encrypt=yes'
    return pyodbc.connect(connection_string)

class Booking(BaseModel):
    email_address: str
    tour_id: int

class Passenger(BaseModel):
    first_name: str
    last_name: str
    email_address: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

# view all timetables
@app.get("/timetables")
def view_timetables():
    conn = get_db_connection()  
    cursor = conn.cursor()
    cursor.execute("EXEC dbo.timetable_procedure;")    
    rows = cursor.fetchall()
    timetables = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    cursor.close()
    conn.close()
    return {"timetables": timetables}

# view all passengers
@app.get("/passengers")
def view_passengers():
    conn = get_db_connection()  
    cursor = conn.cursor()
    cursor.execute("EXEC dbo.get_passengers_procedure;")    
    rows = cursor.fetchall()
    passengers = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    cursor.close()
    conn.close()
    return {"passengers": passengers}

# create a passenger
@app.post('/create-passenger')
async def create_passenger(passenger: Passenger):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(" EXEC [dbo].[create_passenger_procedure] @first_name = ?, @last_name = ?, @email_address = ?", passenger.first_name, passenger.last_name, passenger.email_address) 
        conn.commit() # commit the changes
        cursor.close()
        conn.close()
        return{"success": True, "message": "Passenger created successfully"}
       
    except Exception as e:
        print("Error: %s" % e)
        return {'error': str(e)}

#view all bookings
@app.get("/bookings")
def view_bookings():
    conn = get_db_connection()  
    cursor = conn.cursor()
    cursor.execute("EXEC dbo.get_booking_procedure;")    
    book_rows = cursor.fetchall()
    bookings = [dict(zip([column[0] for column in cursor.description], row)) for row in book_rows]
    cursor.close()
    conn.close() 
    return {"bookings": bookings}

# view a specific booking
# @app.get('/bookings/{booking_id}')
# def get_booking(booking_id: int):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         #cursor.execute("SELECT * FROM Bookings WHERE BookingId=?", booking_id)
#         cursor.execute("EXEC [dbo].[search_booking_procedure] @booking_id = ?", booking_id)
#         columns = [column[0] for column in cursor.description]
#         booking = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         if not booking:
#             return {'error': 'Booking not found'}
        
#         booking_dict = dict(zip(columns, booking))
#         return booking_dict

#     except Exception as e:
#         print("Error: %s" % e)

# view all passengers bookings
@app.get('/bookings/{email_address}')
def get_booking(email_address: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC [dbo].[get_passenger_booking_procedure] @email_address = ?", email_address)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        passengerBookings = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        cursor.close()
        conn.close()

        if not passengerBookings:
            return {'error': 'passenger has no bookings'}
        
        return {"passengers": passengerBookings}

    except Exception as e:
        print("Error: %s" % e)

# create a new booking
@app.post('/create-booking')
async def create_booking(booking: Booking):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DECLARE @booking_id INT; EXEC [dbo].[create_booking_procedure] @email_address = ?, @tour_id = ?, @booking_id = @booking_id OUTPUT;"
               , booking.email_address, booking.tour_id)
        booking_id = cursor.fetchval() # retrieve the value of the booking_id       
        conn.commit() # commit the changes
        cursor.close()
        conn.close()

        if booking_id:
            return{"success": True, "booking_id": booking_id}
        else:
            return {'error': 'Booking not created'}
       
    except Exception as e:
        print("Error: %s" % e)
        return {'error': str(e)}

# delete a specific booking 
@app.delete('/delete-booking/{booking_id}')
async def delete_booking(booking_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC [dbo].[delete_booking_procedure] @booking_id = ?", booking_id)
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_id = ?", booking_id)
        result = cursor.fetchone()
        count = result[0]

        cursor.close()
        conn.close()

        if count == 0:
            return {"success": True, "message": f"Booking with ID {booking_id} deleted successfully."}
        else:
            return {"success": False, "message": f"Booking with ID {booking_id} not found."}

    except Exception as e:
        print("Error: %s" % e)
        return {'error': str(e)}

# update a specific booking   
@app.put('/update-booking/{booking_id}')
async def update_booking(booking_id: int, booking: Booking):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC [dbo].[update_booking_procedure] @booking_id = ?, @email_address = ?, @tour_id = ?"
               , booking_id, booking.email_address, booking.tour_id)
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount < 0:
            return {"success": True, "message": f"Booking with ID {booking_id} updated successfully."}
        else:
            return {"success": False, "message": f"Booking with ID {booking_id} not found."}

    except Exception as e:
        print("Error: %s" % e)
        return {'error': str(e)}