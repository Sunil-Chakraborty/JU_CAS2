from django.contrib import admin
from catg_3.models import Jrnl_pub, Pub_other, Resch_proj,Resch_cons,Prj_outcm,JrnlPaper_UGC,Resch_guide,Lecture_Paper,Fellow_Award,E_Learning


# Register your models here.

class Jrnl_pubAdmin(admin.ModelAdmin):
	list_display = (
     'email','yr_pub','title_pub','no_auth','role_appl','jrnl_name','vl_pg','jrnl_type','imp_fac','jrnl_url','jrnl_link'
     )
 
 
admin.site.register(Jrnl_pub,Jrnl_pubAdmin)

#--------------------------------

class Pub_otherAdmin(admin.ModelAdmin):
	list_display = (
     'email','yr_pub','pub_type','chap_title','bk_title','no_auth','name_pub','sts_pub','isbn_no','pub_url','pub_pdf'
     )
 
class JrnlPaper_UGCAdmin(admin.ModelAdmin):
	list_display = (
     'email','jrnl_name','paper_title'
     )

class Resch_guideAdmin(admin.ModelAdmin):
	list_display = (
     'email','student_name'
     )

class Lecture_PaperAdmin(admin.ModelAdmin):
	list_display = (
     'email','title_lecture'
     )

class Resch_projAdmin(admin.ModelAdmin):
	list_display = (
     'email','proj_title'
     )

class Resch_consAdmin(admin.ModelAdmin):
	list_display = (
     'email','proj_title'
     )

class Prj_outcmAdmin(admin.ModelAdmin):
	list_display = (
     'email','proj_title'
     )          	

class Fellow_AwardAdmin(admin.ModelAdmin):
	list_display = (
     'email','name_fellow'
     ) 
	
class E_LearningAdmin(admin.ModelAdmin):
	list_display = (
     'email','model_name'
     )      



admin.site.register(Pub_other,Pub_otherAdmin)
admin.site.register(JrnlPaper_UGC,JrnlPaper_UGCAdmin)
admin.site.register(Resch_guide,Resch_guideAdmin)
admin.site.register(Lecture_Paper,Lecture_PaperAdmin)
admin.site.register(Resch_proj,Resch_projAdmin)
admin.site.register(Resch_cons,Resch_consAdmin)
admin.site.register(Prj_outcm,Prj_outcmAdmin)
admin.site.register(Fellow_Award,Fellow_AwardAdmin)
admin.site.register(E_Learning,E_LearningAdmin)

 