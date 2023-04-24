from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import BMICalculatorForm, TestimonialForm, SubscriptionForm, MembershipForm, ContactForm
from django.shortcuts import render
from django.utils import timezone
from .models import BMI, Testimonial, Contact
from django.contrib import messages


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

