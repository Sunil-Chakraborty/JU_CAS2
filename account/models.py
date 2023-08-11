# from inspect import modulesbyfile
from http.client import PRECONDITION_REQUIRED
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator

import os
import uuid


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


# def get_profile_image_filepath(self, filename):
# 	return 'profile_images/' + str(self.pk) + '/profile_image.png'


# def get_default_profile_image():
# 	return "codingwithmitch/logo_1080_1080.png"

def get_image_path(instance, filename):
    return os.path.join('general', "user_%s" % str(instance.id), filename)
    
    
class Account(AbstractBaseUser,PermissionsMixin):
	email                                = models.EmailField(verbose_name="email", max_length=60, unique=True)
	emp_id                               = models.CharField(verbose_name="Emp_id", unique=True, max_length=6) 
	username                             = models.CharField(max_length=100)
	parent                               = models.CharField(max_length=100, null=True, blank=True)	
	CAST_CHOICES = (
 		 (None, 'Select'),
         ('cast-1', 'SC'),
         ('cast-2', 'ST'),
         ('cast-3', 'OBC-A'),
         ('cast-4', 'OBC-B'),
         ('cast-5', 'GEN'),
	)
	catg                            = models.CharField(verbose_name='Category', max_length=6,
	                                  choices=CAST_CHOICES, null=True, blank=True)
	Department                      = models.ForeignKey(
	                                    "Department", on_delete=models.CASCADE, null=True, blank=True)
	current_dsg                     = models.CharField(
	                                verbose_name='Present Dsgn.', max_length=30, null=True, blank=True)
	AGP_CHOICES = (
 		 (None, 'Select'),
         (1, '6000/10'),
         (2, '7000/11'),
         (3, '8000/12'),
         (4, '9000/13A'),
         (5, '10000/14'),
	)
	agp = models.IntegerField(verbose_name='AGP fig.',
	                          choices=AGP_CHOICES, null=True, blank=True)
	dt_last_promo = models.DateField(
	    verbose_name='Date of last promotion', null=True, blank=True)
	dt_eligibility = models.DateField(
	    verbose_name='Date of promo elig', null=True, blank=True)
	addr_corres = models.TextField(
	    verbose_name='Address for corres', max_length=300, null=True, blank=True)
	addr_perm = models.TextField(
	    verbose_name='Address for permanent', max_length=300, null=True, blank=True)
	mobile = models.CharField(default="Individual",
	                          max_length=10, null=True, blank=True)
	date_joined = models.DateField(verbose_name='Date of joining', null=True, blank=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_carry = models.BooleanField(default=False)
	is_hod = models.BooleanField(verbose_name='Are you HOD',default=False)
	is_dean = models.BooleanField(verbose_name='Are you Dean',default=False)
	is_applicant = models.BooleanField(default=True)
    
	FACULTY_CHOICES = (
 		 (None, 'Select Faculty'),
         ('fac-1', 'ARTS'),
         ('fac-2', 'SCIENCE'),
         ('fac-3', 'ENGINEERING & TECHNOLOGY'),
         ('fac-4', 'ISLM'),
         
	)
 
 
	faculty = models.CharField(max_length=100,verbose_name='Faculty :',
	                          choices=FACULTY_CHOICES, null=True, blank=True)
	facult  = models.CharField(max_length=100,null=True, blank=True)
	hide_email				= models.BooleanField(default=True)
	
	DSG_CHOICES = (
 		 (None, 'Select Designation'),
         ('dsg-1', 'Assistant Professor'),
         ('dsg-2', 'Associate Professor'),
	)
	Designation             = models.CharField(max_length=30, choices=DSG_CHOICES, null=True, blank=True)
	QUALI_CHOICES = (
        (None, 'Select Qualification'),
        ('q1', 'Ph.D'),
        ('q2', 'M.phil'),
        ('q3', 'M.E'),
        ('q4', 'M.Tech'),
        ('q5', 'M.Arch'),
        ('q6', 'M.Pharm'),
        ('q7', 'M.Sc.'),
        ('q8', 'M.A'),
        ('q9', 'Others'),
    )
	highest_quali			= models.CharField(max_length=200, choices=QUALI_CHOICES, null=True, blank=True)
	pan_no					= models.CharField(max_length=10, null=True, blank=True)
	GENDER_CHOICES = (
     	(None, 'Select Faculty'),       
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
	gender					= models.CharField(verbose_name='Gender(M/F)',max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
	quali_year				= models.CharField(verbose_name='Qualifying Year',max_length=4, null=True, blank=True)
	dt_ob             		= models.DateField(verbose_name='date of birth', null=True, blank=True)
	tot_experience			= models.IntegerField(verbose_name='Total Experience in year', default=0)
	POST_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)'),
        ('Stage 5', 'Professor (Stage 5)')
    )
	post					= models.CharField(verbose_name='Post applied for',max_length=30,choices=POST_CHOICES,null=True, blank=True)
	FROM_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 1', 'Assistant Prof. (Stage 1)'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)')
    )
	from_dsg                = models.CharField(verbose_name='From stage/desgn.',max_length=30,choices=FROM_CHOICES,null=True, blank=True)
	TO_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)'),
        ('Stage 5', 'Professor (Stage 5)')
    )
	to_dsg                  = models.CharField(verbose_name='To stage/desgn.',max_length=30,choices=TO_CHOICES,null=True, blank=True)
	frm_general_info        = models.BooleanField(default=False)
	general_info_date       = models.DateTimeField(auto_now=True)
	frm_submitted           = models.BooleanField(default=False)
	submitted_date          = models.DateTimeField(auto_now=True)
	frm_approved            = models.BooleanField(default=False)
	approved_date           = models.DateTimeField(auto_now=True)
	frm_resubmission        = models.BooleanField(default=False) 
	resubmission_date       = models.DateTimeField(auto_now=True)
	frm_rejected            = models.BooleanField(default=False) 
	rejected_date           = models.BooleanField(default=False)
	ass_yr                  = models.IntegerField(verbose_name='Assessment Year',null=True, blank=True)   
	pdf 				    = models.ImageField(verbose_name='Attachment(image)',upload_to=get_image_path, null=True, blank=True)
	doc_link 				= models.CharField(verbose_name='Document Link',max_length=700,null=True, blank=True)
	is_pwd                  = models.BooleanField(default=False)
	pwd_link 				= models.CharField(verbose_name='Document Link',max_length=700,null=True, blank=True)
	fwd_link 				= models.ImageField(verbose_name='Attachment(image)',upload_to=get_image_path,null=True, blank=True)
	promo_link 				= models.CharField(verbose_name='Document Link',max_length=700,null=True, blank=True)
	is_submit               = models.BooleanField(default=False)
	is_first_login          = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username
        
    #django-cleanup, it automatically invokes delete method on 
    #FileField/ImageField
    
    #pip install django-cleanup
    
    #settings.py

    #INSTALLED_APPS = (
    #     ...
    #    'django_cleanup.apps.CleanupConfig', # should go after your apps
           
        

	def delete(self, *args, **kwargs):
            self.pdf.delete()
            super().delete(*args, **kwargs)
            

                
    
       
    
def has_perm(self, perm, obj=None):
		    return True
  
def has_module_perms(self, app_label):
		    return True
 
def save(self, force_insert=False,force_update=False, using=None, update_fields=None):
            if self.parent is not None:
             self.parent = self.parent.upper()
             super(Account, self).save( force_insert,force_update, using, update_fields)
 
    
      

class Department(models.Model):
    name = models.CharField(max_length=60, unique=True)
    faculty = models.CharField(max_length=100,  null=True, blank=True)
    
 
    def __str__(self):
        return self.name



# def get_file_path(self):
#     return os.path.join('academy/pdfs/'+ str(self.pk) + "/")


class Academic(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    degree  				 = models.CharField(verbose_name='Degree/Certificate Name',max_length=200, null=True, blank=True)
    name_board_university	 = models.CharField(verbose_name='Name of the Board/University',max_length=200, null=True, blank=True)                    
    year_passing             = models.IntegerField(verbose_name='Pass out(Yr.)', null=True, blank=True)
    marks_obtained 			 = models.DecimalField(verbose_name='Marks (%)',max_digits=5, decimal_places=2,null=True,blank=True)
    div_class_grade      	 = models.CharField(verbose_name='Divn/Class/Grade',max_length=200, null=True, blank=True)
    subject                  = models.CharField(verbose_name='Subject(s)',max_length=500, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='academy/pdfs/', null=True, blank=True)
    doc_link 				 = models.CharField(verbose_name='Document Link',max_length=700,null=True, blank=True)

    
    def __str__(self):
        return str(self.email)
       
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name_board_university is not None:
            self.name_board_university = self.name_board_university.upper()
        if self.degree is not None:
            self.degree = self.degree.upper()
        super(Academic, self).save(force_insert, force_update, using, update_fields)
    
    
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)
    
     
class Research(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    degree				     = models.CharField(verbose_name='Degree',max_length=200, null=True, blank=True)
    thesis 				     = models.CharField(verbose_name='Title of Dissertation/Thesis',max_length=500, null=True, blank=True)
    dt_award             	 = models.DateField(verbose_name='Date of Award', null=True, blank=True)
    institute	 		     = models.CharField(verbose_name='Institute/ University',max_length=200, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='research/pdfs/', null=True, blank=True)
    url_link                 = models.CharField(verbose_name='Document(Certificate) link',max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.email)
    
      
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        if self.thesis is not None:
            self.thesis = self.thesis.upper()
        if self.degree is not None:
            self.degree = self.degree.upper()
        if self.institute is not None:    
            self.institute = self.institute.upper()
        super(Research, self).save(force_insert, force_update, using, update_fields)
   
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)
     
class PriorPost(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    designation				 = models.CharField(verbose_name='Designation',max_length=400, null=True, blank=True)
    employer 				 = models.CharField(verbose_name='Name of Employer',max_length=400, null=True, blank=True)
    dt_join             	 = models.DateField(verbose_name='Date of Joining', null=True, blank=True)
    dt_leav             	 = models.DateField(verbose_name='Date of Leaving', null=True, blank=True)
    gross_salary             = models.CharField(verbose_name='Gross Salary (per annum)', max_length=20,null=True, blank=True)
    
    reason_leaving 		     = models.CharField(verbose_name='Reason for Leaving',max_length=400, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='sts_before/pdfs/', null=True, blank=True)
    url_link                 = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.email)
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)
     
class PresentPost(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    DSG_CHOICES = (
     	(None, 'Select'),
        ('Stage 1', 'Assistant Professor - Stage 1'),
        ('Stage 2', 'Assistant Professor - Stage 2'),
        ('Stage 3', 'Assistant Professor - Stage 3'),
        ('Stage 4', 'Assistant Professor - Stage 4'),
        ('Stage 5', 'Professor - Stage 5'),
    )
    designation              = models.CharField(verbose_name='Designation', max_length=30, choices=DSG_CHOICES, null=True, blank=True)
    department               = models.ForeignKey("Department", on_delete=models.CASCADE, null=True, blank=True)   
    period_from            	 = models.DateField(verbose_name='Period: from ', null=True, blank=True)
    period_to            	 = models.DateField(verbose_name='Period: to ', null=True, blank=True)
    pay_scale             	 = models.CharField(verbose_name='Pay Scale', max_length=20,null=True, blank=True)
    
    AGP_CHOICES= (
 		 (None, 'Select'),
         ('1st', '6000/10'),
         ('2nd', '7000/11'),
         ('3rd', '8000/12'),
         ('4th', '9000/13A'),
         ('5th', '10000/14'),         
	)
    agp						 = models.CharField(verbose_name='AGP/Level',max_length=30,choices=AGP_CHOICES, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='sts_after/pdfs/', null=True, blank=True)
    url_link                 = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
     
    def __str__(self):
        return str(self.email)
   
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)


class TeachingExp(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    pg_class				 = models.IntegerField(verbose_name='PG Classes',null=True,blank=True)
    ug_class				 = models.IntegerField(verbose_name='UG Classes',null=True,blank=True)
    doc_yrs				     = models.IntegerField(verbose_name='Doctoral Research',null=True,blank=True)
    postdoc_yrs				 = models.IntegerField(verbose_name='Post-doctoral Research',null=True,blank=True)
    specialisation			 = models.CharField(verbose_name='Specialisation under the Subject/Discipline',max_length=400, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='sts_after/pdfs/', null=True, blank=True)
    url_link                 = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
     
    def __str__(self):
        return str(self.email)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.specialisation is not None:
            self.specialisation = self.specialisation.upper()       
        super(TeachingExp, self).save(force_insert, force_update, using, update_fields)
    
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)

class Orientation(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    title    				 = models.CharField(verbose_name='Title of the Course', max_length=300, null=True, blank=True)
    place    				 = models.CharField(verbose_name='Place', max_length=200, null=True, blank=True)
    duration  				 = models.CharField(verbose_name='Duration (No. of Weeks)', max_length=100, null=True, blank=True)
    period                   = models.CharField(verbose_name='From Date- To Date', max_length=200, null=True, blank=True)
    pdf 					 = models.FileField(verbose_name='Attachment(PDF)',upload_to='orient/pdfs/', null=True, blank=True)
    url_link                 = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
     
    def __str__(self):
        return str(self.email)
    
    def save(self, force_insert=False,force_update=False, using=None, update_fields=None):
        if self.title is not None:
            self.title = self.title.upper()
        if self.place is not None:
            self.place = self.place.upper()
        if self.duration is not None:
            self.duration = self.duration.upper()
        if self.period is not None:
            self.period = self.period.upper()
        super(Orientation, self).save(force_insert,force_update, using, update_fields)
     
    def delete(self, *args, **kwargs):
        self.pdf.delete()        
        super().delete(*args, **kwargs)

class ApiCatg_I(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    direct_teaching          = models.PositiveIntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_dt              = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_dt              = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,default=0)
    pdf_dt                   = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg1/pdfs/', null=True, blank=True) 
    veri_api_dt              = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_dt                   = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    exam_duties              = models.IntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_ed              = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_ed              = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,null=True,blank=True)
    pdf_ed                   = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg1/pdfs/', null=True, blank=True) 
    veri_api_ed              = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_ed                   = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    innovating_teaching      = models.IntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_it              = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_it              = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,null=True,blank=True)
    pdf_it                   = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg1/pdfs/', null=True, blank=True) 
    veri_api_it              = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_it                   = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.email)

class ApiCatg_II(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    field_based_activities   = models.PositiveIntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_fba             = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_fba             = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,null=True,blank=True)
    pdf_fba                  = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg2/pdfs/', null=True, blank=True) 
    veri_api_fba             = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_fba                  = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    corp_life_management     = models.IntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_clm             = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_clm             = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,null=True,blank=True)
    pdf_clm                  = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg2/pdfs/', null=True, blank=True) 
    veri_api_clm             = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_clm                  = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    prof_dev_activity        = models.IntegerField(verbose_name='Hours spent per academic year',null=True,blank=True)
    actl_api_pda             = models.DecimalField(verbose_name='Actual Appraisal Score',max_digits=6,decimal_places=2,null=True,blank=True)
    self_api_pda             = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=4,decimal_places=2,null=True,blank=True)
    pdf_pda                  = models.FileField(verbose_name='Attachment(PDF)',upload_to='api_catg2/pdfs/', null=True, blank=True) 
    veri_api_pda             = models.DecimalField(verbose_name='Verified API Score',max_digits=4,decimal_places=2,null=True,blank=True)
    url_pda                  = models.CharField(verbose_name='Put your document link',max_length=500, null=True, blank=True)
    
    def __str__(self):
        return str(self.email)

class CasFormSts(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete=models.CASCADE)
    general_sts              = models.BooleanField(default=False)
    academy_sts              = models.BooleanField(default=False)
    research_paper_sts       = models.BooleanField(default=False)
    priorpost_sts            = models.BooleanField(default=False)
    present_post_sts         = models.BooleanField(default=False)
    teaching_sts             = models.BooleanField(default=False)
    orientation_sts          = models.BooleanField(default=False)
    api_catg1_sts            = models.BooleanField(default=False)
    api_catg2_sts            = models.BooleanField(default=False)
    jrnl_pub_sts             = models.BooleanField(default=False)
    pub_other_sts            = models.BooleanField(default=False)
    jrnlpaper_sts            = models.BooleanField(default=False)
    resch_proj_sts           = models.BooleanField(default=False)
    resch_cons_sts           = models.BooleanField(default=False)
    prj_outcm_sts            = models.BooleanField(default=False)
    resch_guide_sts          = models.BooleanField(default=False)
    fellow_award_sts         = models.BooleanField(default=False)
    lecture_paper_sts        = models.BooleanField(default=False)
    e_learning_sts           = models.BooleanField(default=False)
    final_sts                = models.BooleanField(default=False)
    general_no               = models.IntegerField(default=0)
    academy_no               = models.IntegerField(default=0)
    research_paper_no        = models.IntegerField(default=0)
    priorpost_no             = models.IntegerField(default=0)
    present_post_no          = models.IntegerField(default=0)
    teaching_no              = models.IntegerField(default=0)
    orientation_no           = models.IntegerField(default=0)
    api_catg1_no             = models.IntegerField(default=0)
    api_catg2_no             = models.IntegerField(default=0)
    jrnl_pub_no              = models.IntegerField(default=0)
    pub_other_no             = models.IntegerField(default=0)
    jrnlpaper_no             = models.IntegerField(default=0)
    resch_proj_no            = models.IntegerField(default=0)
    resch_cons_no            = models.IntegerField(default=0)
    prj_outcm_no             = models.IntegerField(default=0)
    resch_guide_no           = models.IntegerField(default=0)
    fellow_award_no          = models.IntegerField(default=0)
    lecture_paper_no         = models.IntegerField(default=0)
    e_learning_no            = models.IntegerField(default=0)
    final_no                 = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.email)
