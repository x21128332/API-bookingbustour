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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # adding the sql stored procedure script and parameter values
        stored_proc = "[dbo].[search_booking_procedure] @booking_id = ?"
        params = (booking_id)
        # Execute stored procedur with the params
        cursor.execute(stored_proc, params)
    
        # Iterate the cursor
        row = cursor.fetchone()
        while row:
            print(str(row[0]) + " : " + str(row[1] or '') )
            row = cursor.fetchone()
        cursor.close()
        del cursor
        conn.close()

    except Exception as e:
        print("Error: %s" % e)

    # #cursor.execute("SELECT * FROM Bookings WHERE BookingId=?", booking_id)
    # cursor.execute("EXEC [dbo].[search_booking_procedure] @booking_id = ?", booking_id)
    # booking = cursor.fetchone()
    # cursor.close()

    # if not booking:
    #     return {'error': 'Booking not found'}
    
    # return {'booking_id': booking.booking_id}
