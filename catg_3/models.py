from django.db import models
from account.models import Account
from django.core.exceptions import ValidationError
from django.contrib import messages



# Create your models here.

#---------IIIA-Journal Publication--------------------
class  Jrnl_pub(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    yr_pub  				 = models.PositiveIntegerField(verbose_name='Year of Publication',null=True)
    title_pub                = models.CharField(verbose_name='Title of the Paper',max_length=300, null=True, blank=True)                    
    no_auth                  = models.PositiveIntegerField(verbose_name='No.of authors', null=True, blank=True)
    
    ROLE_CHOICES = (
     	(None, 'Select'),       
        ('F_A', 'First author'),
        ('C_A', 'Corresponding author / supervisor / mentor'),
        ('FC_A', 'First and Corresponding author'),
        ('O_A', 'Other co-author'),
    )	
    role_appl   			 = models.CharField(verbose_name='Role of Applicant',max_length=50, choices=ROLE_CHOICES, null=True, blank=True)
    jrnl_name             	 = models.CharField(verbose_name='Journal Name',max_length=200, null=True, blank=True)
    vl_pg                    = models.CharField(verbose_name='Volume (Issue), pg no. from - to',max_length=300, null=True, blank=True)
    JRNL_CHOICES = (
     	(None, 'Select'),       
        ('UGC', 'UGC Care List'),
        ('OTHER', 'Other reputed journal as notified by UGC'),        
    )	
    jrnl_type             	 = models.CharField(verbose_name='Journal Type',max_length=50, choices=JRNL_CHOICES,null=True, blank=True)
    imp_fac             	 = models.DecimalField(verbose_name='Impact Factor (put 0 if NA)',max_digits=6,decimal_places=3,null=True, blank=True)
    jrnl_url             	 = models.CharField(verbose_name='Link of Journal page showing impact factor',max_length=500, null=True, blank=True)
    jrnl_link 				 = models.CharField(verbose_name='Document Link',max_length=700,null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)
    jrnl_oth                 = models.PositiveIntegerField(verbose_name="Other's number",null=True, blank=True)
      
    
    def __str__(self):
        return str(self.email)
    class Meta:
          ordering = ('-yr_pub',)
       
#--------IIIB(i)-Publications other than journal articles ---------
class Pub_other(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    yr_pub                   = models.PositiveIntegerField(verbose_name='Year of Publication',null=True, blank=True)
    
    PUB_CHOICES = (
     	(None, 'Select'),       
        ('TEXT_BK', 'Text Book'),
        ('REF_BK', 'Reference Book'),
        ('BK_CHAP', 'Book Chapter/ Conf. Proceedings'),        
    )

    pub_type                 = models.CharField(verbose_name='Type of Publication',max_length=50, choices=PUB_CHOICES, null=True, blank=True)
    chap_title               = models.CharField(verbose_name='Title of the Chapter',max_length=300, null=True, blank=True)
    bk_title                 = models.CharField(verbose_name='Title of the Book',max_length=300, null=True, blank=True)
    no_auth                  = models.PositiveIntegerField(verbose_name='No.of Authors', null=True, blank=True)
    name_pub                 = models.CharField(verbose_name='Name of the Publisher',max_length=300, null=True, blank=True)
    
    STATUS_CHOICES = (
     	(None, 'Select'),       
        ('INTL', 'International'),
        ('NATL', 'National'),
        ('LOCL', 'Local'),        
    )

    sts_pub                  = models.CharField(verbose_name='Status of Publisher',max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    isbn_no                  = models.CharField(verbose_name='ISBN/ISSN No.',max_length=100, null=True, blank=True)
    pub_url                  = models.CharField(verbose_name='Link of the Publication/Book/Book chapter',max_length=500, null=True, blank=True)
    pub_pdf                  = models.FileField(verbose_name='Upload Paper(PDF)',upload_to='pub_other/pdfs/', null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)



def __str__(self):
        return str(self.email)

class Meta:
          ordering = ('yr_pub',)
        
        
#--------IIIB(ii)-Referring of Journal Papers from UGC list  ---------

class JrnlPaper_UGC(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    jrnl_name                = models.CharField(verbose_name='Journal Name',max_length=300, null=True, blank=True)
    paper_title              = models.CharField(verbose_name='Title of the paper',max_length=300, null=True, blank=True)
    yr_review                = models.PositiveIntegerField(verbose_name='Year of review submission',null=True, blank=True)
    ltr_url                  = models.CharField(verbose_name='Review Invitation Letter Link',max_length=500, null=True, blank=True)
    sub_ltr_url              = models.CharField(verbose_name='Review submission document link',max_length=500, null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email)
class Meta:
          ordering = ('yr_review',)        
           
        
    
#------------------IIIC(i)-Research Projects---IIIC.(i) Sponsored Project-----------------------
class Resch_proj(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    proj_tag                 = models.CharField(verbose_name='Proj tile',max_length=5, null=True, blank=True)
    FACULTY_CHOICES = (
     	(None, 'Select'),       
        ('ARTS', 'Arts'),
        ('SCNC', 'Science'),
        ('ENGG', 'Engineering & Technology'),        
    )
    
    faculty_app              = models.CharField(verbose_name='Area of the Applicant',max_length=50, choices=FACULTY_CHOICES, null=True, blank=True)
    proj_title               = models.CharField(verbose_name='Title of the Project',max_length=300, null=True, blank=True)
    fund_agnc                = models.CharField(verbose_name='Funding Agency',max_length=300, null=True, blank=True)
    no_yrs                   = models.PositiveIntegerField(verbose_name='Duration (no.of years)',null=True, blank=True)
    prj_amt                  = models.DecimalField(verbose_name='Grant Sanctioned (in Lakhs)',max_digits=6,decimal_places=2,null=True,blank=True)
    prj_url                  = models.CharField(verbose_name='Link of the Grant Letter',max_length=500, null=True, blank=True)
    prj_pdf                  = models.FileField(verbose_name='Upload Grant Letter(PDF)',upload_to='resch_proj/pdfs/', null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email)


    
#------------------IIIC(i)-Research Projects---IIIC (ii)  Consultancy Project-----------------------
class Resch_cons(models.Model):
    error_name = {'blank':'You must select an option!!!!! !','invalid':'Wrong format.!!!!!'}
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    proj_tag                 = models.CharField(verbose_name='Proj tile',max_length=5, null=True, blank=True)
    FACULTY_CHOICES = (
     	(None, 'Select'),       
        ('ARTS', 'Arts'),
        ('SCNC', 'Science'),
        ('ENGG', 'Engineering & Technology'),        
    )
   
    faculty_app              = models.CharField(verbose_name='Area of the Applicant',max_length=50,
                               error_messages=error_name,choices=FACULTY_CHOICES, null=True)
    proj_title               = models.CharField(verbose_name='Title of the Project',max_length=300, null=True, blank=True)
    fund_agnc                = models.CharField(verbose_name='Funding Agency',max_length=300, null=True, blank=True)
    no_yrs                   = models.PositiveIntegerField(verbose_name='Duration (no.of years)',null=True, blank=True)
    prj_amt                  = models.DecimalField(verbose_name='Amount Mobilized (Rs.in Lacs)',max_digits=6,decimal_places=2,null=True,blank=True)
    prj_url                  = models.CharField(verbose_name='Link of the Grant Letter',max_length=500, null=True, blank=True)
    prj_pdf                  = models.FileField(verbose_name='Upload Grant Letter(PDF)',upload_to='resch_proj/pdfs/', null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email)


  
#--------------IIIC(iii)-Projects Outcome/Output-----------------    
class Prj_outcm(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    FACULTY_CHOICES = (
     	(None, 'Select'),       
        ('ARTS', 'Arts'),
        ('SCNC', 'Science'),
        ('ENGG', 'Engineering & Technology'),        
    )
    faculty_app              = models.CharField(verbose_name='Area of the Applicant',max_length=50, choices=FACULTY_CHOICES, null=True, blank=True)
    PRJ_CHOICES = (
     	(None, 'Select'),       
        ('MPD', 'Major Policy Document'),
        ('PTNT', 'Patent'),
        ('TETR', 'Technology Transfer'),  
        ('PRDT', 'Product'), 
        ('PRCS', 'Process'),     
    )
    prj_type                 = models.CharField(verbose_name='Type of Project',max_length=50, choices=PRJ_CHOICES, null=True, blank=True)
    proj_title               = models.CharField(verbose_name='Title of the Outcome/Output',max_length=300, null=True, blank=True)
    LEVEL_CHOICES = (
     	(None, 'Select'),       
        ('INTR', 'International'),
        ('NATL', 'National'),
        ('LCL', 'Local'),  
        ('CNGV', 'National (Central Govt.)'), 
        ('STGV', 'State Govt.'),     
    )
    prj_lvl                  = models.CharField(verbose_name='Level',max_length=50, choices=LEVEL_CHOICES, null=True, blank=True)
    ref_no                   = models.CharField(verbose_name='Document No./Patent No/Other reference no',max_length=100,null=True, blank=True)
    PTNT_CHOICES = (
     	(None, 'Select'),       
        ('FILE', 'Filed'),
        ('PUBG', 'Published'),
        ('GRNT', 'Granted'),    
    )
    ptnt_sts                 = models.CharField(verbose_name='Patent Status',max_length=50, choices=PTNT_CHOICES, null=True, blank=True)
    prj_url                  = models.CharField(verbose_name='Link of Document',max_length=500, null=True, blank=True)
    prj_pdf                  = models.FileField(verbose_name='Upload Grant Letter(PDF)',upload_to='resch_proj/pdfs/', null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)


def __str__(self):
        return str(self.email)  
 

class Resch_guide(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)
    student_name             = models.CharField(verbose_name='Student Name',max_length=100, null=True, blank=True)
    DEGR_CHOICES = (
     	(None, 'Select'),       
        ('MPHIL', 'Mphil'),
        ('ME', 'ME'),
        ('MTECH', 'Mtech'),
        ('MPHARM', 'MPHARM'),
        ('PHD', 'PhD'),    
    )
    degree                   = models.CharField(verbose_name='Degree',max_length=20, choices=DEGR_CHOICES, null=True, blank=True)
    title_thesis             = models.CharField(verbose_name='Title of the Thesis',max_length=300, null=True, blank=True)
    STS_CHOICES = (
     	(None, 'Select'),
        ('PHDR', 'Ph.D Registered'),        
        ('DEGR', 'Degree awarded'),
        ('THES', 'Thesis submitted'),             
    )    
    status                   = models.CharField(verbose_name='Status',max_length=50, choices=STS_CHOICES, null=True, blank=True)
    prj_url                  = models.CharField(verbose_name='Upload document',max_length=500, null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email) 
 

class Fellow_Award(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)           
    FELLOW_CHOICES = (
     	(None, 'Select'),       
        ('FELLOW', 'Fellowship'),
        ('AWARD', 'Award for academic bodies/ Association'),            
    )
    fellow_type              = models.CharField(verbose_name='Fellow Type',max_length=50, choices=FELLOW_CHOICES, null=True, blank=True)
    name_fellow              = models.CharField(verbose_name='Name of the Fellowship/Award',max_length=300, null=True, blank=True)
    name_body                = models.CharField(verbose_name='Name of the Fellowship/Award',max_length=300, null=True, blank=True)
    LEVEL_CHOICES = (
     	(None, 'Select'),       
        ('INTR', 'International'),
        ('NATL', 'National'),
        ('LCL',  'State'),  
        ('UNIV', 'University'),            
    )
    prj_lvl                  = models.CharField(verbose_name='Level',max_length=50, choices=LEVEL_CHOICES, null=True, blank=True)
    prj_url                  = models.CharField(verbose_name='Upload document',max_length=500, null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email) 
        

class Lecture_Paper(models.Model):
    email 					 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)           
    INVITE_CHOICES = (
     	(None, 'Select'),       
        ('LECT', 'Invited Lecture'),
        ('PAPER', 'Paper presented'),            
    )
    invitation_type           = models.CharField(verbose_name='Invitation Type',max_length=50, choices=INVITE_CHOICES, null=True, blank=True)
    title_lecture             = models.CharField(verbose_name='Title of the Lecture / Paper',max_length=300, null=True, blank=True)
    seminer                   = models.CharField(verbose_name='Name of the Conference/Seminar/ Workshop',max_length=300, null=True, blank=True)
    organizer                 = models.CharField(verbose_name='Organized by',max_length=200, null=True, blank=True)
    venue                     = models.CharField(verbose_name='Venue',max_length=300, null=True, blank=True)
    duration                  = models.CharField(verbose_name='Duration',max_length=200, null=True, blank=True)
    LEVEL_CHOICES = (
     	(None, 'Select'),       
        ('INTR', 'International'),
        ('NATL', 'National'),
        ('LCL',  'State'),  
        ('UNIV', 'University'),            
    )
    prj_lvl                  = models.CharField(verbose_name='Level',max_length=50, choices=LEVEL_CHOICES, null=True, blank=True)
    prj_url                  = models.CharField(verbose_name='Upload document',max_length=500, null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email) 
        

class E_Learning(models.Model):
    email 				 	 = models.ForeignKey(Account,null=True, on_delete = models.CASCADE)           
    model_name               = models.CharField(verbose_name='Name of the model',max_length=200, null=True, blank=True)
    course_name              = models.CharField(verbose_name='Name of the courses',max_length=200, null=True, blank=True)
    program_name             = models.CharField(verbose_name='NAme of the programs',max_length=200, null=True, blank=True)
    prj_url                  = models.CharField(verbose_name='Upload document',max_length=500, null=True, blank=True)
    self_api_score           = models.DecimalField(verbose_name='Self Appraisal Score',max_digits=5,decimal_places=2,null=True,blank=True)
    veri_api_score           = models.DecimalField(verbose_name='Verified API Score',max_digits=5,decimal_places=2,null=True,blank=True)

def __str__(self):
        return str(self.email) 
        
