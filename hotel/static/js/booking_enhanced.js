document.addEventListener('DOMContentLoaded', function() {
    // Initialize date inputs
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const checkIn = document.getElementById('checkIn');
    const checkOut = document.getElementById('checkOut');
    const roomTypeSelect = document.getElementById('room_type');
    const roomPreview = document.getElementById('roomPreview');
    const previewRoomType = document.getElementById('previewRoomType');
    const previewPrice = document.getElementById('previewPrice');
    
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
    
    // Format currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-NG', {
            style: 'currency',
            currency: 'NGN'
        }).format(amount);
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
    
    // Show room preview when room type is selected
    roomTypeSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const price = selectedOption.dataset.price;
        const roomType = selectedOption.text;
        
        previewRoomType.textContent = roomType;
        previewPrice.textContent = `${formatCurrency(price)} per night`;
        roomPreview.classList.remove('d-none');
    });
    
    // Add animation to booking form on scroll
    const bookingFormContainer = document.querySelector('.booking-form');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            bookingFormContainer.classList.add('booking-form-float');
        } else {
            bookingFormContainer.classList.remove('booking-form-float');
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
            
            // Add loading state to button
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitBtn.disabled = true;
            
            // Redirect to booking confirmation page
            setTimeout(() => {
                window.location.href = this.action + '?' + params.toString();
            }, 1000);
        });
    }

    // Add floating labels effect
    document.querySelectorAll('.form-control, .form-select').forEach(element => {
        element.addEventListener('focus', () => {
            element.closest('.input-group').classList.add('focused');
        });
        
        element.addEventListener('blur', () => {
            element.closest('.input-group').classList.remove('focused');
        });
    });
});