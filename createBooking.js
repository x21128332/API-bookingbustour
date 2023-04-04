function createBooking() {
    let email = document.getElementById('email').value;
    let tour_id = document.getElementById('tour_id').value;
    let csrf_token = document.getElementsByName('csrf_token')[0].value;

    fetch('/create_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({email_address: email, tour_id: tour_id})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Booking created. Booking ID: ' + data.booking_id);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
