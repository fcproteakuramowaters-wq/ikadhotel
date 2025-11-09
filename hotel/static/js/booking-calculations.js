document.addEventListener('DOMContentLoaded', function() {
    // Constants
    const CURRENCY_SYMBOL = '₦';
    const MIN_ROOMS = 1;
    const MAX_ROOMS = 5;

    // Get DOM elements
    const roomQuantityElement = document.getElementById('room-quantity');
    const roomRateElement = document.getElementById('room-rate');
    const numNightsElement = document.getElementById('num-nights');
    const subtotalElement = document.getElementById('subtotal');
    const totalAmountElement = document.getElementById('total-amount');

    // Format currency function
    function formatCurrency(amount) {
        return CURRENCY_SYMBOL + amount.toLocaleString('en-NG');
    }

    // Calculate totals function
    function calculateTotals() {
        const roomRate = parseInt(roomRateElement.textContent.replace(/[^0-9]/g, ''));
        const numNights = parseInt(numNightsElement.textContent);
        const numRooms = parseInt(roomQuantityElement.textContent);

        const subtotalPerNight = roomRate * numRooms;
        const totalAmount = subtotalPerNight * numNights;

        subtotalElement.textContent = formatCurrency(subtotalPerNight);
        totalAmountElement.textContent = formatCurrency(totalAmount);
    }

    // Adjust rooms function
    window.adjustRooms = function(change) {
        const currentRooms = parseInt(roomQuantityElement.textContent);
        const newRooms = Math.max(MIN_ROOMS, Math.min(MAX_ROOMS, currentRooms + change));
        
        if (newRooms !== currentRooms) {
            roomQuantityElement.textContent = newRooms;
            calculateTotals();
        }
    };

    // Initial calculation
    calculateTotals();
});