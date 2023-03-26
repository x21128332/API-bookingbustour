import pyodbc
from fastapi import FastAPI, APIRouter, HTTPException

router = APIRouter()
app = FastAPI()

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

def test_view_bookings():
    book_conn = get_db_connection()  
    book_cursor = book_conn.cursor()
    book_cursor.execute("EXEC dbo.get_booking_procedure;")    
    book_rows = book_cursor.fetchall()
    bookings = [dict(zip([column[0] for column in book_cursor.description], row)) for row in book_rows]
    book_conn.close() 
    return {"bookings": bookings}

@router.get("/{booking_id}")
async def get_booking(booking_id: str = None):
    if booking_id is None:
        raise HTTPException(status_code=400, detail="booking_id parameter is required")
    # Lookup booking by booking_id in database
    booking = test_view_bookings(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

