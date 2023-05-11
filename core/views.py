from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import BMICalculatorForm, TestimonialForm, SubscriptionForm, \
    MembershipForm, ContactForm, BookingForm, OneDayBookingForm
from django.shortcuts import render
from django.utils import timezone
from .models import BMI, Testimonial, Contact
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Membership, Booking, Gallery



def index(request):
    galleries = Gallery.objects.all()
    bmi_form = BMICalculatorForm()
    subscription_form = SubscriptionForm()

    if request.method == 'POST':
        if 'bmi_submit' in request.POST:
            bmi_form = BMICalculatorForm(request.POST)
            if bmi_form.is_valid():
                name = bmi_form.cleaned_data['name']
                age = bmi_form.cleaned_data['age']
                height = bmi_form.cleaned_data['height']
                bmi_instance = BMI.objects.create(name=name, age=age,height = height)
                bmi_instance = bmi_instance.calculate_bmi()
                bmi_instance.save()
                return render(request, 'core/index.html', {'galleries': galleries, 'bmi_form': BMICalculatorForm(),
                                                           'subscription_form': SubscriptionForm(), 'bmi_result': bmi_instance})

        if 'subscription_submit' in request.POST:
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email_instance = subscription_form.save()
                return render(request, 'core/index.html', {'galleries': galleries, 'bmi_form': BMICalculatorForm(),
                                                           'subscription_form': SubscriptionForm()})

    return render(request, 'core/index.html', {'galleries': galleries, 'bmi_form': bmi_form,
                                               'subscription_form': subscription_form})




def membership_view(request):
    form = MembershipForm(request=request)
    if request.method == 'POST':
        form = MembershipForm(request.POST, request=request)  # Pass the POST data
        if form.is_valid():
            form.save()
            messages.info(request, "Thank you for becoming a member. Your membership will be approved soon.")
            return redirect('prifile_dashboard')
        else:
            messages.warning(request, "Sorry, something went wrong.")
            print(form.errors)  # Print form errors for debugging
    return render(request, 'core/membership.html', {'form': form})



def send_expiry_reminder_emails(request):
    # Get all users whose membership is about to expire
    users_to_remind = User.objects.filter(
        membership_end_date=timezone.now().date() + timezone.timedelta(days=2)
    )
    for user in users_to_remind:
        user.send_membership_expiry_email()
    return render(request, 'expiry_reminder_sent.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission
            messages.info(request,"Thanks for Contacting us we will get back you soon")
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'core/contact.html', context)



def booking(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False, user=request.user)
            booking.user = request.user

            # Check if the user has an active and paid membership
            booking = request.user.booking.first()
            if booking is None:
                messages.warning(request, "You don't have a membership. Please sign up for one.")
                return redirect('membership')

            membership = booking.membership

            if not membership.is_active:
                messages.warning(request, "You don't have an active membership, but you can book one day.")
                return redirect('one_day_booking')

            if not membership.has_paid:
                messages.warning(request, "Your membership hasn't been paid for.")
                return redirect('membership')

            # Rest of the validation logic...

            booking.save()
            messages.success(request, "Your session has been booked.")
            return redirect('booking')

    else:
        form = BookingForm()

    context = {'form': form}
    return render(request, 'core/booking.html', context)







def one_day_booking(request):
    if request.method == 'POST':
        form = OneDayBookingForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission
            messages.info(request,"Thanks for Contacting us we will get back you soon")
    else:
        form = OneDayBookingForm()

    context = {'form': form}
    return render(request, 'core/booking.html', context)



def bookin(request):
    user = request.user
    membership = Membership.objects.filter(user=user, is_active=True).last()
    booked_hours = Booking.get_booked_hours()
    if not membership:
        messages.warning(request, 'You do not have an active membership. Please purchase a membership to book a session.')
        return redirect('membership')
    elif not membership.has_paid:
        messages.warning(request, 'Your membership has not been paid for. Please pay for your membership to book a session.')
        return redirect('membership')
    elif Booking.is_sunday_booked():
        messages.warning(request, 'Sorry, bookings cannot be made on Sundays.')
        return redirect('booking')
    elif Booking.is_day_sold_out():
        messages.warning(request, 'Sorry, all spots for this day have been booked.')
        return redirect('booking')
    else:
        if request.method == 'POST':
            form = OneDayBookingForm(request.POST)
            if form.is_valid():
                session_date = form.cleaned_data['session_date']
                session_start_time = form.cleaned_data['session_start_time']
                session_end_time = form.cleaned_data['session_end_time']
                session_type = form.cleaned_data['session_type']
                booking = Booking.objects.create(user=user, membership=membership, session_date=session_date, session_start_time=session_start_time, session_end_time=session_end_time, session_type=session_type)
                booking.save()
                messages.success(request, 'Your session has been booked.')
                return redirect('booking')
        else:
            form = BookingForm()
        
        form.fields['session_date'].widget.attrs.update({'class': 'form-control form-control-lg bg-dark text-white', 'placeholder': 'Select a date'})
        form.fields['session_start_time'].widget.attrs.update({'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'Select a start time'})
        form.fields['session_end_time'].widget.attrs.update({'class': 'form-control form-control-lg bg-dark text-white timepicker', 'placeholder': 'Select an end time'})

        context = {'form': form, 'booked_hours': booked_hours}
        return render(request, 'core/booking.html', context)


def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


