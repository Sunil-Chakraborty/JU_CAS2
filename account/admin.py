from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Department,Academic,Orientation,ApiCatg_I,Research,PriorPost,PresentPost,TeachingExp,ApiCatg_II



class AccountAdmin(UserAdmin):
	list_display = (
     'email','emp_id','username','date_joined','dt_ob', 
     'last_login','is_applicant','is_admin','is_hod','is_dean',
     'Department', 'Designation', 'faculty',
     'highest_quali','pan_no',
     'gender','quali_year',
     'frm_submitted',
     'tot_experience','is_first_login'     
     )
	search_fields = ('email','username')
	readonly_fields=('id','last_login')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

class AcademicAdmin(admin.ModelAdmin):
	list_display = (
     'email','degree'
     )

class ResearchAdmin(admin.ModelAdmin):
	list_display = (
     'email','degree'
     )

class PriorPostAdmin(admin.ModelAdmin):
	list_display = (
     'email','designation'
     )

class PresentPostAdmin(admin.ModelAdmin):
	list_display = (
     'email','designation'
     )

class TeachingExpAdmin(admin.ModelAdmin):
	list_display = (
     'email','pg_class','ug_class','doc_yrs','postdoc_yrs','specialisation'
     )
	
class OrientationAdmin(admin.ModelAdmin):
	list_display = (
     'email','title'
     )     
admin.site.register(Account, AccountAdmin)
admin.site.register(Academic, AcademicAdmin) 
admin.site.register(Department)
admin.site.register(Orientation,OrientationAdmin)
admin.site.register(ApiCatg_I)
admin.site.register(Research,ResearchAdmin)
admin.site.register(PriorPost,PriorPostAdmin)
admin.site.register(PresentPost,PresentPostAdmin)
admin.site.register(TeachingExp,TeachingExpAdmin)
admin.site.register(ApiCatg_II)