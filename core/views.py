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
from .models import Membership, Booking



def index(request):
    bmi_form = BMICalculatorForm()
    testimonial_form = TestimonialForm()
    subscription_form = SubscriptionForm()

    if request.method == 'POST':
        if 'bmi_form' in request.POST:
            bmi_form = BMICalculatorForm(request.POST)
            if bmi_form.is_valid():
                name = bmi_form.cleaned_data['name']
                age = bmi_form.cleaned_data['age']
                height = bmi_form.cleaned_data['height']
                bmi_instance = BMI.objects.create_user(name=name, age=age,height = height)
                bmi_instance = bmi_instance.calculate_bmi()
                bmi_instance.save()
                return render(request, 'core/index.html', {'bmi_form': BMICalculatorForm(), 'testimonial_form': TestimonialForm(), 'subscription_form': SubscriptionForm(), 'bmi_result': bmi_instance})
            print(bmi_form.age.errors)

        # if 'testimonial_form' in request.POST:
        #     testimonial_form = TestimonialForm(request.POST)
        #     if testimonial_form.is_valid():
        #         testimonial_instance = testimonial_form.save(commit=False)
        #         testimonial_instance.user = request.user
        #         testimonial_instance.save()
        #         return render(request, 'core/index.html', {'bmi_form': BMICalculatorForm(), 'testimonial_form': TestimonialForm(), 'subscription_form': SubscriptionForm()})

        if 'subscription_form' in request.POST:
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email_instance = subscription_form.save()
                return render(request, 'core/index.html', {'bmi_form': BMICalculatorForm(), 'testimonial_form': TestimonialForm(), 'subscription_form': SubscriptionForm()})

    return render(request, 'core/index.html', {'bmi_form': bmi_form, 'testimonial_form': testimonial_form, 'subscription_form': subscription_form})


def membership_view(request):
    form = MembershipForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('membership_success')
    return render(request, 'membership_form.html', {'form': form})


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
            booking = form.save(commit=False)
            booking.user = request.user
            session_date = booking.session_date
            session_start_time = booking.session_start_time

            # Check if the user has an active and paid membership
            if not booking.user.membership.is_active:
                messages.warning(request, "You don't have an active membership, but you can book one day.")
                return redirect('one_day_booking')

            if not booking.user.membership.has_paid:
                messages.warning(request, "Your membership hasn't been paid for.")
                return redirect('membership')

            # Check if it's not Sunday
            if session_date.weekday() == 6:
                messages.warning(request, "The gym is closed on Sundays.")
                return redirect('booking')

            # Get the booked hours for the session date
            bookings = Booking.objects.filter(session_date=session_date)
            booked_hours = bookings.values_list('session_start_time', 'session_end_time')

            # Check if the day is sold out
            if bookings.count() >= 6:
                messages.warning(request, "This day is already sold out.")
                return redirect('booking')

            # Check if the session time is available
            for booked_hour in booked_hours:
                if (session_start_time >= booked_hour[0] and session_start_time < booked_hour[1]) or \
                   (booking.session_end_time > booked_hour[0] and booking.session_end_time <= booked_hour[1]):
                    messages.warning(request, "This time slot is already booked.")
                    return redirect('booking')

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


