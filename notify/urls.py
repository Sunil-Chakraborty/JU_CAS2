from django.urls import path

from notify.views import (
	send_message,
    inbox,
    create_message,
    edit_message,
    view_message,
    delete_message,
 )
 
app_name = 'notify'


urlpatterns = [
	path('send/<int:receiver_id>/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),
    path('view/<int:message_id>/', view_message, name='view-message'),
    path('create/', create_message, name='create_message'),
    path('edit/<int:message_id>/', edit_message, name='edit-message'),
    path('delete/<int:message_id>/', delete_message, name='delete-message'),
]
