from django.shortcuts import render, get_object_or_404, redirect,reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from notify.forms import MessageForm
#from django.contrib.auth.views import LoginView
from account.models import Account
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.utils.html import strip_tags


@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('notify:inbox')  # Replace 'inbox' with the name of your view displaying received messages
    else:
        receiver = User.objects.get(id=receiver_id)
        return render(request, 'notify/send_message.html', {'receiver': receiver})


def inbox(request,*args, **kwargs):
    #user_id = kwargs.get("user_id")
    user = request.user
    id_no = user.id
    #user_id = request.session['user_id']
    account = Account.objects.get(pk=user.id)
    
    print("l-34 ",user.id)
    received_messages = Message.objects.filter(receiver=user.id,read=False)
    sending_message = Message.objects.filter(sender=user.id) 
    
    if received_messages or sending_message or user.id == 1 : 
        return render(request, 'notify/inbox.html', {'messages': received_messages,'sending_message': sending_message,'account':account,'id_no':id_no})
    else:
        return redirect('account:home', user_id=id_no)
        
      
def create_message(request):
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        receiver = request.POST.get('receiver')
        
        account = Account.objects.get(pk=receiver)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.receiver_name = account.username
            user.email = account.email
            
            user.save()
            return redirect('notify:inbox')
        
        
    form = MessageForm()     
    return render(request, 'notify/create_message.html', {'form': form})

def edit_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    content_text=message.content
    #user_id = request.session['user_id']
    user = request.user
    id_no = user.id
    account = Account.objects.get(pk=user.id)
    hide_sender = False
    hide_receiver = False
    
    if not account.is_superuser: 
        hide_sender = True  # Set this to True or False based on your condition
        hide_receiver = True  # Set this to True or False based on your condition
        
        
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        receiver = request.POST.get('receiver')        
        account = Account.objects.get(pk=receiver)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            user.receiver_name = account.username
           
            if hide_sender and hide_receiver:
                user.read = True
                
                print('l-145',user.content)
            else:
                user.timestamp = user.modified_date
                user.read = False
            user.email = account.email
            user.save()
            
            return redirect('notify:inbox')
    else:
        form = MessageForm(instance=message)
    return render(request, 'notify/edit_message.html', {'form': form, 'message': message,'hide_sender': hide_sender, 'hide_receiver': hide_receiver,'content_text':content_text,'id_no':id_no})


def view_message(request,message_id):     
    
    message = get_object_or_404(Message, pk=message_id)
    
    if not message.read:        
        message.read = True       
        message.save()
       
    return redirect('dashboard')
    

def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message_subject = message.content  # Save the subject for displaying in the message

    message.delete()

    # Redirect to inbox after deletion
    return redirect('notify:inbox')
