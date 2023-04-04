function deleteBooking() {
    let bookingId = document.getElementById('booking-id').value;
    let csrf_token = document.getElementsByName('csrf_token')[0].value;

    fetch('/delete_booking', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({booking_id: bookingId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Booking with ID ' + bookingId + ' has been deleted');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
