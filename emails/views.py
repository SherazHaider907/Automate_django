from django.shortcuts import render,redirect,get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subcriber,Email
from .tasks import send_email_task
from django.db.models import Sum
from emails.models import Sent

# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            # send an Email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            # to_email = settings.DEFAULT_TO_EMAIL
            email_list = request.POST.get('email_list')

            # excess the selected email list
            email_list = email.email_list

            # Extract email addressess from the subcriber model
            subcribers = Subcriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subcribers]
        
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id
            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment,email_id)
            
            
            # display a success message
            messages.success(request,'Email sent Successfully!')
            return redirect('send_email')
    else:
        email = EmailForm()
        context = {
            'email_form' : email,
        }
    return render (request,'emails/send_email.html',context)


def track_click():
    return

def track_open():
    return

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent'))

    context = { 
        'emails':emails
    }
    return render(request , 'emails/track_dashboard.html',context)

def track_stats(request,pk):
    email = get_object_or_404(Email,pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email':email,
        'total_sent':sent.total_sent
    }
    return render(request,'emails/track_stats.html',context)