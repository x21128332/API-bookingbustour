import pyodbc
from fastapi import FastAPI

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
    conn.close() 
    return {"timetables": "timetables"}


# @app.post("/bookings")
# async def create_booking(booking: BookingSchema, db: pyodbc.Connection = Depends(get_db)):
#     cursor = db.cursor()
#     insert_query = f"INSERT INTO bookings (tour_id, passenger_name, email, phone_number, number_of_passengers, pickup_address, pickup_date, pickup_time) VALUES ('{booking.tour_id}', '{booking.passenger_name}', '{booking.email}', '{booking.phone_number}', {booking.number_of_passengers}, '{booking.pickup_address}', '{booking.pickup_date}', '{booking.pickup_time}')"
#     cursor.execute(insert_query)
#     db.commit()
#     return {"message": "Booking created"}
