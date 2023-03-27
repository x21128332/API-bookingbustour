import pyodbc
from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter()
app = FastAPI(title="Sample FastAPI Application")

def get_db_connection():
    server = 'sqlaislingsbustour.database.windows.net'
    database = 'sqlaislingsbustour'
    #using managed identity so no need for user + pass
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:sqlaislingsbustour.database.windows.net,1433;Database=sqlaislingsbustour;Authentication=ActiveDirectoryMsi; Encrypt=yes'
    return pyodbc.connect(connection_string)

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
    conn.close() 
    return {"timetables": timetables}

@app.get("/bookings")
def view_bookings():
    book_conn = get_db_connection()  
    book_cursor = book_conn.cursor()
    book_cursor.execute("EXEC dbo.get_booking_procedure;")    
    book_rows = book_cursor.fetchall()
    bookings = [dict(zip([column[0] for column in book_cursor.description], row)) for row in book_rows]
    book_conn.close() 
    return {"bookings": bookings}

@app.get('/bookings/{booking_id}')
def get_booking(booking_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    #cursor.execute("SELECT * FROM Bookings WHERE BookingId=?", booking_id)
    cursor.execute("EXEC [dbo].[search_booking_procedure] @booking_id = ?", booking_id)
    booking = cursor.fetchone()
    cursor.close()

    if not booking:
        return {'error': 'Booking not found'}
    
    return {'booking_id': booking[0], 'booking_id': booking[1], 'booking_date': booking[2], 'first_name': booking[3], 'last_name': booking[4], 'seat_number': booking[5], 'origin': booking[6], 'destination': booking[7]}
