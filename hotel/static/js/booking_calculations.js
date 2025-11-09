function formatCurrency(amount) {
    return new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function updateTotalAmount() {
    const pricePerNight = parseInt(document.getElementById('room-rate').textContent.replace(/[^0-9]/g, ''));
    const nights = parseInt(document.getElementById('num-nights').textContent);
    const rooms = parseInt(document.getElementById('num-rooms').value);
    
    // Calculate subtotal per night (price per night × number of rooms)
    const subtotalPerNight = pricePerNight * rooms;
    document.getElementById('subtotal-per-night').textContent = formatCurrency(subtotalPerNight);
    
    // Calculate total amount (subtotal per night × number of nights)
    const totalAmount = subtotalPerNight * nights;
    document.getElementById('total-amount').textContent = formatCurrency(totalAmount);

    // Update hidden input for form submission
    document.getElementById('total_amount').value = totalAmount;
}

function incrementRooms() {
    const input = document.getElementById('num-rooms');
    const currentValue = parseInt(input.value);
    if (currentValue < parseInt(input.max)) {
        input.value = currentValue + 1;
        updateTotalAmount();
    }
}

function decrementRooms() {
    const input = document.getElementById('num-rooms');
    const currentValue = parseInt(input.value);
    if (currentValue > parseInt(input.min)) {
        input.value = currentValue - 1;
        updateTotalAmount();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Format dates
    const checkin = new Date(parseInt(document.getElementById('checkin_timestamp').value) * 1000);
    const checkout = new Date(parseInt(document.getElementById('checkout_timestamp').value) * 1000);
    
    document.getElementById('check-in-date').textContent = checkin.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    document.getElementById('check-out-date').textContent = checkout.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });

    // Calculate number of nights
    const nights = Math.floor((checkout - checkin) / (1000 * 60 * 60 * 24));
    document.getElementById('num-nights').textContent = nights;

    // Initialize phone input
    const phoneInput = document.getElementById('phone');
    if (window.intlTelInput) {
        window.intlTelInput(phoneInput, {
            preferredCountries: ['ng'],
            utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js"
        });
    }

    // Add event listener for manual input changes
    const numRoomsInput = document.getElementById('num-rooms');
    numRoomsInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        const min = parseInt(this.min);
        const max = parseInt(this.max);
        
        if (value < min) this.value = min;
        if (value > max) this.value = max;
        if (!isNaN(value)) {
            updateTotalAmount();
        }
    });

    // Initial price calculation
    updateTotalAmount();
});