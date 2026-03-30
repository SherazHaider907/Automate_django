from django.shortcuts import render,redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subcriber
from .tasks import send_email_task

# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            # send an Email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            # to_email = settings.DEFAULT_TO_EMAIL
            email_list = request.POST.get('email_list')

            # excess the selected email list
            email_list = email_form.email_list

            # Extract email addressess from the subcriber model
            subcribers = Subcriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subcribers]
        
            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                attachment = None

            # Handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)
            
            
            # display a success message
            messages.success(request,'Email sent Successfully!')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form,
        }
    return render (request,'emails/send_email.html',context)


def track_click():
    return

def track_open():
    return