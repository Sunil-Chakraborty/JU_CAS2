from django.urls import path
from . import views


from account.views import (
	account_view,
    edit_account_view,
    cas_view,
    academy_view,
    professional_view,
    teaching_view,    
    orient_view,
    cas_edit,
    cas_edit1,
    academy_edit1,    
    research_edit1,    
    prests_edit1,
    academy_delete,
    research_delete,
    prests_delete,
    curpost_edit1,
    curpost_delete,
    #teach_edit,
    #teach_edit1,
    #teach_delete,    
    orient_edit1,
    orient_delete,         
    self_view,
    api1_view,
    api2_view,
    ViewPDF,
    AboutView,
    NoticeView,
    InstructionView,
   
    
)

app_name = 'account'

urlpatterns = [

    path('about/', views.AboutView.as_view(), name='about'),
    path('notice/', views.NoticeView.as_view(), name='notice'),
    path('instruction/', views.InstructionView.as_view(), name='instruction'),
    
	path('<user_id>/', account_view, name="view"),
 	path('<user_id>/edit/', edit_account_view, name="edit"),
  	path('<user_id>/cas/', cas_view, name="cas"),
    path('<user_id>/pdf_view/', ViewPDF.as_view(), name="pdf_view"),
    
    path('<user_id>/home/', self_view, name="home"),
    path('<user_id>/academy/', academy_view, name="academy"),
    path('<user_id>/professional/', professional_view, name="professional"),
    path('<user_id>/teaching/', teaching_view, name="teaching"),    
    path('<user_id>/orient/', orient_view, name="orient"),
    
    path('cas-edit/<str:pk>/', cas_edit, name="cas-edit"),
    path('cas-edit1/<str:pk>/', cas_edit1, name="cas-edit1"),
    
    path('academy-edit1/<str:pk>/', academy_edit1, name="academy-edit1"),
    path('academy-delete/<str:pk>/', academy_delete, name="academy-delete"),
   
    path('research-edit1/<str:pk>/', research_edit1, name="research-edit1"),
    path('research-delete/<str:pk>/', research_delete, name="research-delete"),

    path('prests-edit1/<str:pk>/', prests_edit1, name="prests-edit1"),
    path('prests-delete/<str:pk>/', prests_delete, name="prests-delete"),

    path('curpost-edit1/<str:pk>/', curpost_edit1, name="curpost-edit1"),
    path('curpost-delete/<str:pk>/', curpost_delete, name="curpost-delete"),

    path('orient-edit1/<str:pk>/', orient_edit1, name="orient-edit1"),
    path('orient-delete/<str:pk>/', orient_delete, name="orient-delete"),


    path('<user_id>/api-1/', api1_view, name="api-1"),
    path('<user_id>/api-2/', api2_view, name="api-2"),
       
    # path('<user_id>/pdf_view/', ViewPDF.as_view(), name="pdf_view"),

]
