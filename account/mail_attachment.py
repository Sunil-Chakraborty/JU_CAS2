from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse,HttpResponseRedirect 
from django.conf import settings
from .forms import PathForm
import datetime
from datetime import datetime


def Mail_File_View(request):   

    
    now =  datetime.now()
    
    dd = now.strftime("%d")
    mm = now.strftime("%m")
    yy = now.strftime("%Y")
 
    if len(dd) == 1:
        dd="0"+dd
        
    if len(mm) == 1:
        mm="0"+mm
        
    yy=yy[-2:]

    path_txt="/home/iqac-cas/backup_"+dd+mm+yy+"_1.dump"
   
    print(path_txt)

    email_subject = 'Email with JUCAS Backup file'
    email_body = 'Please find the attachment'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['to.sayantani@gmail.com', 'to.sunilc@gmail.com']
    
    email = EmailMessage(email_subject, email_body, from_email, recipient_list)
   
   
    email.attach_file(path_txt)
    
  
        
    email.send()
    
   
    return render(request, "account/pathfinder.html")
    

def File_Path_View(request):   

    form1 = PathForm()
    
    email_subject = 'Email with attachment'
    email_body = 'Please find the attachment'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['to.sayantani@gmail.com', 'to.sunilc@gmail.com']
    
    email = EmailMessage(email_subject, email_body, from_email, recipient_list)
        
    #email.attach_file('/personal/Sunil_CV.docx')
    
    if request.method == 'POST':
        form1 = PathForm(request.POST,request.FILES)
        if form1.is_valid():        
            # Retrieve the value of the text field from the form data
            p = form1.cleaned_data.get('path_name')
            print(p)
            
            try:
            #if p != "":
                email.attach_file(p)
                email.send()
                msg = f'<div style="width:30%;text-align:center;font-size:20px;font-weight:bold;background-color: lightblue;">The mail is been sent successfully.<br>Check your mail!!</div>'
                return HttpResponse(msg, content_type='text/html')
                
            except:
                msg = f'<h1>Path/file name  is wrong <br>Try again</h1>'
                return HttpResponse(msg, content_type='text/html')
                #return HttpResponse(msg, content_type='text/plain')
        
        
        
        return redirect("/")
        
    context={       
        'form1':form1,        
       }
   
    return render(request, "account/filefinder.html",context)
