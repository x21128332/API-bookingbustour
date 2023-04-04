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

@app.get("/")
def read_root():
    return {"Hello": "World"}

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

@app.get('/bookings/{booking_id}')
def get_booking(booking_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM Bookings WHERE BookingId=?", booking_id)
        cursor.execute("EXEC [dbo].[search_booking_procedure] @booking_id = ?", booking_id)
        columns = [column[0] for column in cursor.description]
        booking = cursor.fetchone()
        cursor.close()
        conn.close()

        if not booking:
            return {'error': 'Booking not found'}
        
        booking_dict = dict(zip(columns, booking))
        return booking_dict
        #    return {'booking_id': booking.booking_id, 'booking_date': booking.booking_date, 'first_name': booking.first_name}

    except Exception as e:
        print("Error: %s" % e)

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
    
@app.delete('/delete-booking/{booking_id}')
async def delete_booking(booking_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC [dbo].[delete_booking_procedure] @booking_id = ?", booking_id)
        conn.commit()
        cursor.close()
        conn.close()

        cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_id = ?", booking_id)
        result = cursor.fetchone()
        count = result[0]

        if count == 0:
            return {"success": True, "message": f"Booking with ID {booking_id} deleted successfully."}
        else:
            return {"success": False, "message": f"Booking with ID {booking_id} not found."}

        # if cursor.rowcount > 0:
        #     return {"success": True, "message": f"Booking with ID {booking_id} deleted successfully."}
        # else:
        #     return {"success": False, "message": f"Booking with ID {booking_id} not found."}

    except Exception as e:
        print("Error: %s" % e)
        return {'error': str(e)}
