from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import BMICalculatorForm, TestimonialForm, SubscriptionForm, MembershipForm

def index(request):
    bmi_form = BMICalculatorForm()
    testimonial_form = TestimonialForm()
    subscription_form = SubscriptionForm()

    if request.method == 'POST':
        if 'bmi_form' in request.POST:
            bmi_form = BMICalculatorForm(request.POST)
            if bmi_form.is_valid():
                bmi_instance = bmi_form.save(commit=False)
                bmi_instance.bmi_result = bmi_instance.calculate_bmi()
                bmi_instance.save()
                return render(request, 'core/index.html', {'bmi_form': BMICalculatorForm(), 'testimonial_form': TestimonialForm(), 'subscription_form': SubscriptionForm(), 'bmi_result': bmi_instance.bmi_result})

        if 'testimonial_form' in request.POST:
            testimonial_form = TestimonialForm(request.POST)
            if testimonial_form.is_valid():
                testimonial_instance = testimonial_form.save(commit=False)
                testimonial_instance.user = request.user
                testimonial_instance.save()
                return render(request, 'core/index.html', {'bmi_form': BMICalculatorForm(), 'testimonial_form': TestimonialForm(), 'subscription_form': SubscriptionForm()})

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