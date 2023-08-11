from django import forms
from django.forms import Field,widgets,ValidationError
from django.core.validators import URLValidator
#from django.utils.translation import ugettext_lazy




from . models import Jrnl_pub, Pub_other,Resch_proj,Resch_cons,Prj_outcm,Resch_guide,Fellow_Award,Lecture_Paper,E_Learning,JrnlPaper_UGC
  
class Jrnl_pubForm(forms.ModelForm):
    
    class Meta:
        model = Jrnl_pub
        fields = "__all__"
         
    
        widgets = {            
            'yr_pub'        : widgets.NumberInput(attrs={
                                'class':'form-number form-control',
                                'style': 'font-size:18px;font-weight:bold;width:7ch',
                                'oninput': 'limit_yr_pub()'
                                }),                        
            'title_pub'     : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 5em;font-size:18px;font-weight:bold;',
                                               'rows': 3,'cols': 30}),
            'no_auth'       : widgets.NumberInput(attrs={'class':'form-number form-control','style': 'font-size:18px;font-weight:bold;','oninput': 'check_other()'}),                        
            'role_appl'     : widgets.Select(attrs={                              
                              'class':'form-control',
                              'style': 'width:600px;height:3em;font-size:18px;font-weight:bold;',
                              'oninput': 'check_role()'
                               }),
            'jrnl_name'     : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;font-size:18px;font-weight:bold;'}),
            'vl_pg'         : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;font-size:18px;font-weight:bold;'}),
            'jrnl_type'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;font-size:18px;font-weight:bold;text-transform:uppercase'}),
            'imp_fac'       : widgets.NumberInput(attrs={'class':'form-number form-control','style': 'font-size:18px;font-weight:bold;','oninput': 'check_impact()'}),                        
            'jrnl_url'      : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;font-size:18px;font-weight:bold;'}),
            'jrnl_link'     : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;font-size:18px;font-weight:bold;'}),
            'jrnl_oth'      : widgets.NumberInput(attrs={'class':'form-number form-control','style': 'font-size:18px;font-weight:bold;'}),
            
            }
        
    def clean(self):
            cleaned_data = super(Jrnl_pubForm, self).clean()
            no_auth = cleaned_data.get('no_auth')
            print(no_auth)
            jrnl_oth = cleaned_data.get('jrnl_oth')
            role_appl = cleaned_data.get('role_appl')
            imp_fac = cleaned_data.get('imp_fac')
            jrnl_url = cleaned_data.get('jrnl_url')
            jrnl_link = cleaned_data.get('jrnl_link')

            if imp_fac > 0 :
                if not jrnl_url:
                    raise ValidationError(u'Please provide necessary document link against impact factor!')
            #return cleaned_data
            
            if no_auth == 1 :
                if role_appl != "FC_A":
                    raise ValidationError(u'Please ensure no of authors against your Role!')
                    # self.add_error('role_appl', 'Role of applicant does not match with no of authors!')
                    # You can use ValidationError as well
                    # self.add_error('role_appl', form.ValidationError('Role of applicant does not match with no of authors!'))                     
                    # raise ValidationError(u'Role of applicant does not match with no of authors!')
            elif no_auth > 2 :
                if role_appl == "O_A":
                    if not cleaned_data['jrnl_oth']:
                        print(no_auth)
                        raise ValidationError(u'Please provide the no of other co-authors!')
            #return cleaned_data             
                
            
            
            
            if role_appl == "O_A":
                
                #  if jrnl_oth == 0:
                #     raise ValidationError(u'Other no must be > 0')
                 
                 if jrnl_oth >= no_auth:
                    raise ValidationError(u'Other must be < No of authors')
            
            
            if cleaned_data['imp_fac']:
                if not cleaned_data['jrnl_url']:
                    raise forms.ValidationError(u'Please provide document link!')

            


                
    def __init__(self, *args, **kwargs):
        super(Jrnl_pubForm,self).__init__(*args, **kwargs)
        self.fields['yr_pub'].widget.attrs['min'] = 2000
        self.fields['yr_pub'].widget.attrs['max'] = 2023
        self.fields['yr_pub'].required = True
        self.fields['no_auth'].widget.attrs['min'] = 1
        self.fields['no_auth'].widget.attrs['max'] = 50 
        self.fields['imp_fac'].widget.attrs['min'] = 0
        self.fields['imp_fac'].widget.attrs['max'] = 99
        self.fields['jrnl_oth'].widget.attrs['min'] = 0
        self.fields['jrnl_oth'].widget.attrs['max'] = 9
        
        self.fields['title_pub'].required = True
        self.fields['no_auth'].required = True
        self.fields['role_appl'].required = True
        self.fields['jrnl_name'].required = True
        self.fields['vl_pg'].required = True
        self.fields['jrnl_type'].required = True
        self.fields['imp_fac'].required = True
        self.fields['jrnl_link'].required = True
        self.fields['email'].required = False
        
        #if self.instance.imp_fac:
        #   self.fields['jrnl_url'].required = True
        
        #self.fields['jrnl_url'].required = True
        
        #self.fields['jrnl_oth'].required = True
       



class Pub_otherForm(forms.ModelForm):
    
    class Meta:
        model = Pub_other
        fields = "__all__"

        widgets = {            
                    'yr_pub'         : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'limit_input()'}),                        
                    'pub_type'       : widgets.Select(attrs={
                                                        'class':'form-control',
                                                        'style': 'width:600px;height:3em;text-transform:uppercase',
                                                        'oninput': 'check_other()'}),
                    'chap_title'     : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                                                    'rows': 3,'cols': 40}),
                    'bk_title'       : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                                                    'rows': 3,'cols': 40}),
                    'no_auth'        : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'limit_auth()'}), 
                    'name_pub'       : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
                    'sts_pub'        : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
                    'isbn_no'        : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
                    'pub_url'        : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),    
                    
                    
                    
                    }
        
    def clean(self):
            cleaned_data = super(Pub_otherForm, self).clean()
            no_auth = cleaned_data.get('no_auth')
            pub_type = cleaned_data.get('pub_type')
            
            chp_title = cleaned_data.get('chap_title')
            sts_pub = cleaned_data.get('sts_pub')
            
            if pub_type == 'BK_CHAP':
               if not chp_title:                  
                  raise ValidationError(u'Please Fill the Title of the Chapter')
            return cleaned_data
            
                       
    def __init__(self, *args, **kwargs):
        super(Pub_otherForm,self).__init__(*args, **kwargs)
        
        self.fields['yr_pub'].widget.attrs['min'] = 1990
        self.fields['yr_pub'].widget.attrs['max'] = 2023 # check current year
        self.fields['yr_pub'].required = True
        self.fields['no_auth'].widget.attrs['min'] = 1
        self.fields['no_auth'].widget.attrs['max'] = 10
        self.fields['pub_type'].required = True
        #self.fields['chap_title'].required = True
        self.fields['bk_title'].required = True
        self.fields['no_auth'].required = True
        self.fields['name_pub'].required = True        
        self.fields['sts_pub'].required = True
        self.fields['isbn_no'].required = True
        self.fields['pub_url'].required = True
        self.fields['email'].required = False
        
class JrnlPaper_UGCForm(forms.ModelForm):
    
    class Meta:
        model = JrnlPaper_UGC
        fields = "__all__"

        widgets = {            
                    'yr_review'         : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'limit_input()'}),                        
                    'jrnl_name'         : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                                                        'rows': 3,'cols': 40}),
                    'paper_title'       : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;'}),
                    'ltr_url'           : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),    
                    'sub_ltr_url'       : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),    
                  }
        
    def clean(self):
            cleaned_data = super(JrnlPaper_UGCForm, self).clean()
            yr_review = cleaned_data.get('yr_review')
            jrnl_name = cleaned_data.get('jrnl_name')
            paper_title = cleaned_data.get('paper_title')
            ltr_url = cleaned_data.get('ltr_url')
            sub_ltr_url = cleaned_data.get('sub_ltr_url')
                
                       
    def __init__(self, *args, **kwargs):
        super(JrnlPaper_UGCForm,self).__init__(*args, **kwargs)
        
        self.fields['yr_review'].widget.attrs['min'] = 1990
        self.fields['yr_review'].widget.attrs['max'] = 2023 # check current year
        self.fields['yr_review'].required = True
        self.fields['jrnl_name'].required = True
        self.fields['paper_title'].required = True
        self.fields['ltr_url'].required = True
        self.fields['sub_ltr_url'].required = True
        self.fields['email'].required = False




        
class Resch_projForm(forms.ModelForm):
     
    class Meta:
        model = Resch_proj
        fields = "__all__"
        
        error_messages = {
            'name': {
                'prj_amt': "Check the value",
            },
        }
     
        widgets = {
            'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
            'proj_title'   : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                              'rows': 3,'cols': 40}),  
            'fund_agnc'    : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                              'rows': 3,'cols': 40}),                       
            'no_yrs'       : widgets.NumberInput(attrs={'class':'form-number form-control','oninput': 'limit_yrs()'}),
            'prj_amt'      : widgets.NumberInput(attrs={
                                'class':'form-number form-control',
                                'oninput': 'limit_input()'                                
                                }),
            'prj_url'      : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),           
        }
        
        
    def clean(self):
            cleaned_data = super(Resch_projForm, self).clean()
            prj_tg = cleaned_data.get('proj_tag')
            prj_amt = cleaned_data.get('prj_amt')
            faculty_app = cleaned_data.get('faculty_app')
            
            # validating the proj_tag
            
            if prj_tg == 'cons':
                if faculty_app == 'ARTS':
                    if prj_amt < 2 :
                       raise ValidationError(u'Check the amount!')
                else:
                    if prj_amt < 10 :
                       raise ValidationError(u'Check the amount!')
                
                 
                       
                
    def __init__(self, *args, **kwargs):
            super(Resch_projForm,self).__init__(*args, **kwargs)            
            self.fields['prj_amt'].widget.attrs['max'] = 999.99
            self.fields['no_yrs'].widget.attrs['max'] = 99            
            self.fields['faculty_app'].required = True
            self.fields['proj_title'].required = True
            self.fields['fund_agnc'].required = True
            self.fields['no_yrs'].required = True
            self.fields['no_yrs'].widget.attrs['min'] = 1
            self.fields['no_yrs'].widget.attrs['max'] = 20
            self.fields['prj_amt'].required = True
            self.fields['prj_url'].required = True
            self.fields['email'].required = False
          

class Resch_consForm(forms.ModelForm):
  
    class Meta:
        model = Resch_cons
        fields = "__all__" 
        #fields = ('email','proj_tag','faculty_app','proj_title','fund_agnc','no_yrs','prj_amt','prj_url','prj_pdf','self_api_score','veri_api_score')  
        
        widgets = {
            'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
            'proj_title'   : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                              'rows': 3,'cols': 40}),
            'fund_agnc'    : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;',
                              'rows': 3,'cols': 40}),                       
            'no_yrs'       : widgets.NumberInput(attrs={'class':'form-number form-control'}),
            'prj_amt'      : widgets.NumberInput(attrs={
                                'class':'form-number form-control',                               
                                'oninput': 'limit_input()'
                                                              
                                }),
                               
                         
            'prj_url'      : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),           
        }
        
        
    def clean(self):
            cleaned_data = super(Resch_consForm, self).clean()           
            prj_tg = cleaned_data.get('proj_tag')
            prj_amt = cleaned_data.get('prj_amt')
            faculty_app = cleaned_data.get('faculty_app')
            
            
                
            # validating the proj_tag
            
            # if prj_amt :
            #     if prj_tg == 'cons':
            #         if faculty_app == 'ARTS':
            #             if prj_amt < 2 :
            #                 raise ValidationError(u'Check the min amount for "Arts"!')
            #         else:
            #             if prj_amt < 10 :
            #                 raise ValidationError(u'Check the min amount other than Arts!')
            # else:
            #     raise ValidationError('Amount Mobilized must be in lakhs  !')

            if not prj_amt :
                raise ValidationError('Amount Mobilized must be in lakhs  !')

                
           
    def __init__(self, *args, **kwargs):
            super(Resch_consForm,self).__init__(*args, **kwargs)
            self.fields['proj_title'].required = True
            self.fields['fund_agnc'].required = True
            self.fields['no_yrs'].required = True
            self.fields['prj_url'].required = True
            self.fields['prj_amt'].validators = [max_range]
            self.fields['email'].required = False
            
 
def max_range(value):
    if value <= 0 or value > 999.99:
       raise ValidationError(u'Rs. in Lacs only!!!!!')    
       
       
 
class Prj_outcmForm(forms.ModelForm):
     
    class Meta:
        model = Prj_outcm
        fields = "__all__"
                    
        widgets = {
             'faculty_app'  : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_type'     : widgets.Select(attrs={
                                'class':'form-control',
                                'style': 'width:600px;height:3em;text-transform:uppercase',
                                'oninput': 'check_other()'
                                }),
             'proj_title'   : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}), 
             'prj_lvl'      : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'ref_no'       : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'ptnt_sts'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_url'      : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        
        
        }
        
    def clean(self):
            cleaned_data = super(Prj_outcmForm, self).clean()
            prj_type = cleaned_data.get('prj_type')
            ptnt_sts = cleaned_data.get('ptnt_sts')
            prj_lvl = cleaned_data.get('prj_lvl')
            
            if prj_type == 'PTNT':
                if not cleaned_data['ptnt_sts']:
                    raise forms.ValidationError(u'Please select Patent Status!')           
                    
            if prj_lvl == "None":
                raise forms.ValidationError(u'Please select Level!')
            
            
            
    def __init__(self, *args, **kwargs):
            super(Prj_outcmForm,self).__init__(*args, **kwargs)
            self.fields['faculty_app'].required = True
            self.fields['prj_type'].required = True
            self.fields['proj_title'].required = True
            self.fields['prj_lvl'].required = True
            self.fields['ref_no'].required = True
            #self.fields['ptnt_sts'].required = True
            self.fields['prj_url'].required = True
            self.fields['email'].required = False
            
class Resch_guideForm(forms.ModelForm):
     
    class Meta:
        model = Resch_guide
        fields = "__all__"
                    
        widgets = {
             'student_name' : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}), 
             'degree'       : widgets.Select(attrs={
                                'class':'form-control',
                                'style': 'width:600px;height:3em;text-transform:uppercase',
                                'oninput': 'check_option()'
                                }),             
             'title_thesis' : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}), 
             'status'       : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),
             'prj_url'      : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        
        }

    def clean(self):
            cleaned_data = super(Resch_guideForm, self).clean()
            sts          = cleaned_data.get('status')
            degree       = cleaned_data.get('degree')
            
            
            # validating the status
            
            if degree != 'PHD':
                if sts == 'THES':                  
                   raise ValidationError(u'Check the degree please!')
               
  
    def __init__(self, *args, **kwargs):
        super(Resch_guideForm,self).__init__(*args, **kwargs)
        self.fields['student_name'].required = True
        self.fields['degree'].required = True
        self.fields['title_thesis'].required = True
        self.fields['status'].required = True
        self.fields['prj_url'].required = True
        self.fields['email'].required = False
        
        
class Fellow_AwardForm(forms.ModelForm):
     
    class Meta:
        model = Fellow_Award
        fields = "__all__"
                    
        widgets = {
             'fellow_type' : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'name_fellow' : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'name_body'   : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'prj_lvl'     : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),             
             'prj_url'     : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Fellow_AwardForm,self).__init__(*args, **kwargs)
        self.fields['fellow_type'].required = True
        self.fields['name_fellow'].required = True
        self.fields['name_body'].required = True
        self.fields['prj_lvl'].required = True
        self.fields['prj_url'].required = True
        self.fields['email'].required = False
        
        
class Lecture_PaperForm(forms.ModelForm):
     
    class Meta:
        model = Lecture_Paper
        fields = "__all__"
                    
        widgets = {
             'invitation_type' : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}), 
             'title_lecture'   : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'seminer'         : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'organizer'       : widgets.Textarea(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'venue'           : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'duration'        : widgets.TextInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
             'prj_lvl'         : widgets.Select(attrs={'class':'form-control','style': 'width:600px;height:3em;text-transform:uppercase'}),             
             'prj_url'         : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(Lecture_PaperForm,self).__init__(*args, **kwargs)
        self.fields['invitation_type'].required = True
        self.fields['title_lecture'].required = True
        self.fields['seminer'].required = True
        self.fields['organizer'].required = True
        self.fields['venue'].required = True
        self.fields['duration'].required = True
        self.fields['prj_lvl'].required = True
        self.fields['prj_url'].required = True
        self.fields['email'].required = False
        
        

class E_LearningForm(forms.ModelForm):
     
    class Meta:
        model = E_Learning
        fields = "__all__"
                    
        widgets = {
             'model_name'      : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                                                         'rows': 3,'cols': 40}),
             'course_name'     : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                                                         'rows': 3,'cols': 40}),
             'program_name'    : widgets.Textarea(attrs={'class':'form-control', 'style': 'height: 4em;text-transform:uppercase',
                                                         'rows': 3,'cols': 40}),
             'prj_url'         : widgets.URLInput(attrs={'class':'form-control','style': 'width:600px;height:3em;'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(E_LearningForm,self).__init__(*args, **kwargs)
        self.fields['model_name'].required = True
        self.fields['course_name'].required = True
        self.fields['program_name'].required = True
        self.fields['prj_url'].required = True
        self.fields['email'].required = False
        

        