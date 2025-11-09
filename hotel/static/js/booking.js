// Add to the static/js/booking.js file
document.addEventListener('DOMContentLoaded', function() {
    // Set minimum dates for check-in and check-out
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const checkIn = document.getElementById('checkIn');
    const checkOut = document.getElementById('checkOut');
    
    // Format date to YYYY-MM-DD
    const formatDate = (date) => {
        const d = new Date(date);
        let month = '' + (d.getMonth() + 1);
        let day = '' + d.getDate();
        const year = d.getFullYear();
        
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        
        return [year, month, day].join('-');
    };
    
    // Set minimum dates
    checkIn.min = formatDate(today);
    checkOut.min = formatDate(tomorrow);
    
    // Update check-out minimum date when check-in is selected
    checkIn.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const minCheckout = new Date(selectedDate);
        minCheckout.setDate(selectedDate.getDate() + 1);
        checkOut.min = formatDate(minCheckout);
        
        // If current check-out date is before new minimum, update it
        if (new Date(checkOut.value) <= selectedDate) {
            checkOut.value = formatDate(minCheckout);
        }
    });
    
    // Handle form submission
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Convert dates to timestamps
            const checkinDate = new Date(checkIn.value);
            const checkoutDate = new Date(checkOut.value);
            
            // Calculate number of nights
            const nights = Math.floor((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));
            
            // Add timestamps and nights to form data
            const formData = new FormData(this);
            formData.set('checkin', Math.floor(checkinDate.getTime() / 1000));
            formData.set('checkout', Math.floor(checkoutDate.getTime() / 1000));
            formData.set('nights', nights);
            
            // Build query string
            const params = new URLSearchParams(formData);
            
            // Redirect to booking confirmation page
            window.location.href = this.action + '?' + params.toString();
        });
    }
});