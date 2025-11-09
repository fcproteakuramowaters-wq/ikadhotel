from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from smtplib import SMTPException
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def confirm_booking(request):
    if request.method == 'POST':
        # Debug: Print all POST data
        print("Received POST data:", request.POST)
        
        # Collect form data with default values
        first_name = request.POST.get('firstName', 'Not provided')
        last_name = request.POST.get('lastName', 'Not provided')
        email = request.POST.get('email', 'Not provided')
        phone = request.POST.get('phone', 'Not provided')
        address = request.POST.get('address', 'Not provided')
        city = request.POST.get('city', 'Not provided')
        state = request.POST.get('state', 'Not provided')
        country = request.POST.get('country', 'Not provided')
        zip_code = request.POST.get('zipCode', 'Not provided')
        special_requests = request.POST.get('specialRequests', 'None')
        room_rate = request.POST.get('roomRate', 'Not provided')
        num_nights = request.POST.get('numNights', 'Not provided')
        total_amount = request.POST.get('totalAmount', 'Not provided')
        
        # Debug: Print collected data
        print("Collected form data:", {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'room_rate': room_rate,
            'num_nights': num_nights,
            'total_amount': total_amount
        })

        # Prepare email content with improved formatting
        subject = f'New Booking from {first_name} {last_name}'
        message = f"""
IKAD Hotel - New Booking Confirmation
====================================

Guest Information
----------------
Full Name: {first_name} {last_name}
Email Address: {email}
Phone Number: {phone}

Mailing Address
--------------
Street Address: {address}
City: {city}
State/Province: {state}
Country: {country}
Postal Code: {zip_code}

Booking Details
-------------
Room Rate per Night: {room_rate}
Number of Nights: {num_nights}
Total Amount: {total_amount}

Special Requests/Notes
--------------------
{special_requests}

This booking was received on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        
        # Debug: Print email content
        print("\nEmail Content:")
        print("Subject:", subject)
        print("Message:", message)

        # Send email
        try:
            # Create email message
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['fatukasikayode2013@gmail.com'],
                reply_to=[email] if email else None
            )
            
            # Debug information
            logger.info(f"Attempting to send email to fatukasikayode2013@gmail.com")
            logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}")
            logger.info(f"Subject: {subject}")
            
            # Send the email
            email.send(fail_silently=False)
            
            logger.info("Email sent successfully")
            
            # Determine which hotel page to redirect to based on the room type
            room_type = request.POST.get('room_type', '').lower()
            # Use the actual URL patterns defined in urls.py
            redirect_url = '/hotels/victoria-island/' if 'studio' in room_type or 'elite' in room_type or 'premier' in room_type or 'luxury' in room_type or 'master' in room_type else '/hotels/cooli-hotel/'
            
            # Redirect to appropriate hotel page with success message
            response = redirect(redirect_url)
            response.set_cookie('booking_message', 'Your booking has been confirmed successfully! Check your email for details.', max_age=30)
            return response
            
        except SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Email server error. Please try again later.'
            }, status=500)
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}'
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from datetime import datetime

def home(request):
    return render(request, 'hotel/home.html')

def ikad_victoria_island(request):
    context = {}
    if 'booking_message' in request.COOKIES:
        context['booking_message'] = request.COOKIES['booking_message']
    return render(request, 'ikadvi/victoria_island.html', context)

def cooli_hotel(request):
    context = {}
    if 'booking_message' in request.COOKIES:
        context['booking_message'] = request.COOKIES['booking_message']
    return render(request, 'ikadbw/cooli.html', context)

def contact(request):
    return render(request, 'hotel/contact.html')

def booking_confirmation(request, hotel_type):
    if request.method == 'POST':
        # Handle form submission
        try:
            # Process the booking data
            booking_data = {
                'first_name': request.POST.get('firstName'),
                'last_name': request.POST.get('lastName'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'address': request.POST.get('address'),
                'city': request.POST.get('city'),
                'state': request.POST.get('state'),
                'country': request.POST.get('country'),
                'zip_code': request.POST.get('zipCode'),
                'special_requests': request.POST.get('specialRequests'),
                'checkin': request.POST.get('checkin'),
                'checkout': request.POST.get('checkout'),
                'room_type': request.POST.get('room_type'),
                'guests': request.POST.get('guests'),
                'total_amount': request.POST.get('total_amount')
            }
            
            # Here you would typically save the booking to your database
            # For now, we'll just simulate success
            
            # Redirect to a success page or send a success response
            return JsonResponse({'status': 'success', 'message': 'Booking confirmed successfully'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    else:
        # Handle GET request - show the booking form
        context = {
            'checkin': request.GET.get('checkin', int(time.time())),  # Default to current time if not provided
            'checkout': request.GET.get('checkout', int(time.time() + 86400)),  # Default to tomorrow if not provided
            'room_type': request.GET.get('room_type', 'Standard Room'),
            'guests': request.GET.get('guests', 2),
            'hotel_type': hotel_type,  # 'vi' for Victoria Island or 'bw' for Cooli Hotel
            'price_per_night': request.GET.get('price', 50000),  # Default price if not specified
            'num_nights': request.GET.get('nights', 1)
        }
        
        template_name = 'ikadvi/booking_confirmation.html' if hotel_type == 'vi' else 'ikadbw/booking_confirmation.html'
        return render(request, template_name, context)

@csrf_exempt
def process_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Here you would process the booking data
            # For now, we'll just return success
            return JsonResponse({
                'status': 'success',
                'booking_id': f"BK{int(time.time())}"  # Generate a simple booking ID
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
