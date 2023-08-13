from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve



from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from account.mail_attachment import Mail_File_View,File_Path_View

from personal.views import (
    temp,
    home_proj,
    dashboard,
    

)


from account.views import (    
    register_view,
    login_view,
    logout_view,
    academy_add,
    research_add,
    prests_add,
    curpost_add,
    #teach_add,
    orient_add,
    
    
)

from catg_3.views import (	
    jrnl_add,
    
    pub_other_add,
    
    jrnl_paper_add,
    
    resch_sponsor_add,
    resch_cons_add,
    
    
    prj_add,
    
    resch_guide_add,
    
    fellow_award_add,
    
    
    lecture_paper_add,
    
    
    lecture_elearn_add,
   
    
)

urlpatterns = [	
       
	# path('admin/',include('admin_honeypot.urls',namespace='admin-honeypot')),
    path('juadmin/',admin.site.urls),

    path('mail',Mail_File_View,name='mail'),
    path('mailf',File_Path_View,name='mailf'),

    path('login', login_view, name="login"),
    path('account/', include('account.urls', namespace='account')),
    path('catg_3/', include('catg_3.urls', namespace='catg_3')),
    path('notify/', include('notify.urls', namespace='notify')),

    path('logout/', logout_view, name="logout"),  
    path('', register_view, name="register"),  
    path('academy-add', academy_add, name='academy-add'),
    path('jrnl-add', jrnl_add, name='jrnl-add'),
   
    path('pub-add', pub_other_add, name='pub-add'),
   
    path('jrnl-paper-add', jrnl_paper_add, name='jrnl-paper-add'),
 
    path('resch-sponsor-add', resch_sponsor_add, name='resch-sponsor-add'),
    path('resch-cons-add', resch_cons_add, name='resch-cons-add'),
   
    path('resch-guide-add', resch_guide_add, name='resch-guide-add'),
    
    path('fellow-award-add', fellow_award_add, name='fellow-award-add'),
    
    path('lecture-paper-add', lecture_paper_add, name='lecture-paper-add'),
    
    path('lecture-elearn-add', lecture_elearn_add, name='lecture-elearn-add'),
    
    path('prj-add', prj_add, name='prj-add'),
   
    
    path('research-add', research_add, name='research-add'),
    path('prests-add', prests_add, name='prests-add'),
    path('curpost-add', curpost_add, name='curpost-add'),
   
    path('orient-add', orient_add, name='orient-add'),
   
    path('temp/', temp, name='temp'),    
    path('home-proj/', home_proj, name='home-proj'),
    path('dashboard/', dashboard, name='dashboard'),
    
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),
        
    path('password_change2/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change2.html'), 
        name='password_change2'),
        
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),    
    
    path('password_change_done2', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done2.html'), 
        name='password_change_done2'),    
   
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/reset_password.html"),
         name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/reset_password_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/reset.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/reset_password_complete.html"),
         name="password_reset_complete"),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),    
     
     
]

    
 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    


# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_complete"    

