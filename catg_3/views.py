from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse,HttpRequest
from django.forms import formset_factory
from django.test import tag
from . models import Jrnl_pub,Pub_other,Resch_proj,Resch_cons,Prj_outcm, Resch_guide,Fellow_Award,Lecture_Paper,E_Learning,JrnlPaper_UGC
from . forms import Jrnl_pubForm, Pub_otherForm,Resch_projForm,Prj_outcmForm, Resch_guideForm, Fellow_AwardForm,Lecture_PaperForm,E_LearningForm,Resch_consForm,JrnlPaper_UGCForm                  
from account.models import Account,Academic,Research,PriorPost,PresentPost,Orientation,ApiCatg_I,ApiCatg_II,TeachingExp,CasFormSts
from account.forms import AccountCasForm,SubmitForm
from django.contrib import messages
from django.db.models import Avg,Min,Max,Sum
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

import time

# Create your views here.


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def LetterView(request,*args, **kwargs):   
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
      
    account = Account.objects.get(pk=user_id) # applicant row
    casfrmsts=CasFormSts.objects.get(pk=user_id)
   
    
    if not casfrmsts.final_sts:
        sts_idx=""
        #sts_idx="Part A/Part B(a)/Part C(b)/Part D/Part E/Catg-I/Catg-II/Catg-III E(ii)"
        
        if not casfrmsts.general_sts:
            sts_idx=sts_idx+"Part A"
            
        if not casfrmsts.academy_sts:
            sts_idx=sts_idx+" Part B(a)"
    
        if not casfrmsts.present_post_sts:
            sts_idx=sts_idx+" Part C(b)"
    
        if not casfrmsts.teaching_sts:
            sts_idx=sts_idx+" Part D"
    
        if not casfrmsts.orientation_sts:
            sts_idx=sts_idx+" Part E"
    
        if not casfrmsts.api_catg1_sts:
            sts_idx=sts_idx+" Catg-I"

        if not casfrmsts.api_catg2_sts:
            sts_idx=sts_idx+" Catg-II"

        if not casfrmsts.lecture_paper_sts:
           sts_idx=sts_idx+" Catg-III E(ii)"
            
        sts_idx="Please update below all mandatory pages to proceed  viz."+sts_idx
        
        messages.error(request,(sts_idx))
        
        return redirect("account:home", user_id=request.user.id)
     	
    context = {}
    
    if request.method == "GET":
        if user_id == 0:
            form = SubmitForm()           
        else:
            act = Account.objects.get(pk=user_id)
            form = SubmitForm(instance=act)

                        
            context = {
                'account': account,
                'pk_var': pk_var,
                'user_var': user_var,
                'form':form,
                'act':act,
                
            }
            
        
        
        return render(request, "catg_3/steps_for_final_submission.html", context)
    else:
    
        if user_id == 0:
            form = SubmitForm(request.POST)
        else:
            act = Account.objects.get(pk=user_id)
            form = SubmitForm(request.POST, request.FILES, instance=act)
            
            
        if form.is_valid():
            
            if form.cleaned_data["is_submit"]:               
                act.frm_submitted = True
                print("line-83",act.frm_submitted)
            else:
                act.frm_submitted = False 
                print("line-86",act.frm_submitted)    
               
            if request.method=='POST' and 'btnform1'  in request.POST:
            
                if not form.cleaned_data["fwd_link"]:
                    messages.error(request,('Please upload your forwarding letter!'))
                elif form.cleaned_data["fwd_link"] and not form.cleaned_data["is_submit"]:
                    messages.success(request,('File uploaded successfully!'))
            
                form.save()
                
            if request.method=='POST' and 'btnform2' in request.POST:
            
                if form.cleaned_data["is_submit"] and form.cleaned_data["fwd_link"]:
                    messages.success(request,('Thank you for submission!'))
                     
                form.save()
                
                
                
                if not form.cleaned_data["is_submit"]:
                    while True:
                       time.sleep(6)
                    #messages.error(request,('You have not yet submitted!'))    
                    return redirect(request.path)
                    
                while True:
                   time.sleep(4)             
                return redirect("account:home", user_id=request.user.id)

                                          
        else:
        
            messages.error(request,('Record has not been saved!'))
            
        return redirect(request.path)
        #return redirect("account:pdf_view", user_id=request.user.id)
       
    
class LetterPDF(View):

	def get(self, request, *args, **kwargs):
            user_id = kwargs.get("user_id")
            
            account = Account.objects.get(pk=user_id)
            user = request.user
            global pk_var 
            
            if account.is_admin:
                messages.success(request,"You can get PDF of your applicant's ! Pl.click on your member's row")
                
            if Account.is_admin:
                account = Account.objects.get(pk=user_id)
            else:
                account = Account.objects.get(pk=request.user.id)  
            
    
            context={}
    
    
            if account :
                        context['username'] = account.username.upper()                        
                        context['Department'] = account.Department                        
                        context['from_dsg'] = account.get_from_dsg_display
                        context['to_dsg'] = account.get_to_dsg_display
                         
                        pdf = render_to_pdf('catg_3/pdf_endoltr.html', context)
                        
                        return HttpResponse(pdf, content_type='application/pdf')

    

def jrnl_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
   
    context = {}
   
    account = Account.objects.get(pk=user_id)         
    jrnl = account.jrnl_pub_set.all()
   
    jrnl_count = jrnl.count()            
   
    context = {        
        'jrnl': jrnl,                            
        'jrnl_count': jrnl_count,
        'pk_var': pk_var,
        'user_var': user_var,
       
    }
    return render(request, "catg_3/jrnl_pub.html", context)

def jrnl_edit(request, pk):
    
    jrnl = Jrnl_pub.objects.get(id=pk)
    
    form1 = Jrnl_pubForm(instance=jrnl)
    user_id=jrnl.email_id
    jrnl_id=jrnl.id
    
    if request.method == 'POST':
            form1 = Jrnl_pubForm(request.POST, request.FILES, instance=jrnl)
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
            
            else:
                #print(form2.errors)
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
              
    msg1='Record has been modified successfully!'            
    context = {
        'form1': form1,
        'user_id': user_id,
        'jrnl_id': jrnl_id,
        'jrnl':jrnl,
        
        }
    
    return render(request, 'catg_3/edit_jrnlpub.html', context)
    
@login_required(login_url="login")
def jrnl_add(request):
    
    form1 = Jrnl_pubForm()
    
    js=0
    jrnl_type=""
    imp_fac=0
    
    
    if request.method == 'POST':
    
            form1 = Jrnl_pubForm(request.POST, request.FILES)
            
            if form1.is_valid():
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added succesfully!'))
                return redirect("catg_3:jrnl-pub", user_id=rec.email_id)
            else:                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)
    context = {
        'form1': form1,
    }
    
    return render(request, 'catg_3/jrnl_register1.html', context) #This is for adding new records

def jrnl_delete(request, pk):
    Jrnl = Jrnl_pub.objects.get(id=pk)
    
    if request.method == "POST":
        Jrnl.delete()
        return redirect("catg_3:jrnl-pub", user_id=Jrnl.email_id)
        
    context = {'item':Jrnl}
    return render(request, 'catg_3/jrnl_delete.html', context)


 #---------------IIIB(i & ii) Publications other than Journals / Referring of Journal Papers from UGC list -------------------


def pub_other_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
     
    account = Account.objects.get(pk=user_id)    
    

    context = {}
    
    pub = account.pub_other_set.all()
    jrnl_paper=account.jrnlpaper_ugc_set.all()    
    pub_count = pub.count()
       
    context = {       
        'pub': pub,
        'jrnl_paper':jrnl_paper,        
        'pub_count': pub_count,
        'pk_var': pk_var,
        'user_var': user_var,
        
    }

    return render(request, "catg_3/pub_other.html", context)
    
    
@login_required(login_url="login")
def pub_other_add(request):
        
    form1 = Pub_otherForm()
   
    if request.method == 'POST':
         
            form1 = Pub_otherForm(request.POST, request.FILES)
            if form1.is_valid():
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:pub-other", user_id=rec.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)                
                return redirect(request.path) 
   
    context = {
        'form1': form1,
    }
    return render(request, 'catg_3/pub_other_add.html', context)

@login_required(login_url="login")
def jrnl_paper_add(request):
   
    form1 = JrnlPaper_UGCForm()
    
    
    if request.method == 'POST':
         
            form1 = JrnlPaper_UGCForm(request.POST, request.FILES)
            
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:pub-other", user_id=rec.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)
    
    context = {
        'form1': form1,        
    }
    
    return render(request, 'catg_3/jrnl_paper_add.html', context)



def pub_edit(request, pk):

    pub = Pub_other.objects.get(id=pk)
    
    form1 = Pub_otherForm(instance=pub)
    user_id=pub.email_id
    pub_id=pub.id
    
    if request.method == 'POST':
            form1 = Pub_otherForm(request.POST, request.FILES, instance=pub)
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
           
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'pub_id': pub_id,
        'pub':pub,
        
        }
    
    return render(request, 'catg_3/edit_pub_other.html', context)

def jrnl_paper_edit(request, pk):    
    jrnl_paper = JrnlPaper_UGC.objects.get(id=pk) 
    form1 = JrnlPaper_UGCForm(instance=jrnl_paper)
    user_id=jrnl_paper.email_id
    jrnl_paper_id=jrnl_paper.id
    
    if request.method == 'POST':
            form1 = JrnlPaper_UGCForm(request.POST, request.FILES, instance=jrnl_paper)
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
           
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'jrnl_paper_id': jrnl_paper_id,
        'jrnl_paper':jrnl_paper
        
        }
    
    return render(request, 'catg_3/edit_jrnl_paper.html', context)


def pub_delete(request, pk):
    pub = Pub_other.objects.get(id=pk)
    
    if request.method == "POST":
        pub.delete()
        return redirect("catg_3:pub-other", user_id=pub.email_id)
        
    context = {'item':pub}
    return render(request, 'catg_3/pub_delete.html', context)

def jrnl_paper_delete(request, pk):
    jrnl_paper=JrnlPaper_UGC.objects.get(id=pk)
    
    if request.method == "POST":
        jrnl_paper.delete()
        return redirect("catg_3:pub-other", user_id=jrnl_paper.email_id)
        
    context = {'item':jrnl_paper}
    return render(request, 'catg_3/jrnl_paper_delete.html', context)


def resch_proj_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 

    global prj_tg
    prj_tg="abc"
    
    
    account = Account.objects.get(pk=user_id)    
     

    context = {}
    
    res = account.resch_proj_set.all()
    cons = account.resch_cons_set.all()
    prj = account.prj_outcm_set.all()
    
         
    context = {               
        'res': res,
        'cons':cons,
        'pk_var': pk_var,
        'user_var': user_var,
        'prj': prj,
    }
        
    return render(request, "catg_3/resch_proj.html", context)

@login_required(login_url="login")
def resch_sponsor_add(request):

    form1 = Resch_projForm()
    
    
    if request.method == 'POST':
         
            form1 = Resch_projForm(request.POST, request.FILES)
            
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id
                rec.proj_tag="spon"                
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:resch-view", user_id=rec.email_id)                
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)  
                
    context = {
        'form1': form1,
    }
    
    return render(request, 'catg_3/resch_proj_add.html', context)
    
@login_required(login_url="login")
def resch_cons_add(request):

    form1 = Resch_consForm()
     
    
    if request.method == 'POST':
         
            form1 = Resch_consForm(request.POST, request.FILES)
            if form1.is_valid():
                rec = form1.save(commit=False)
                rec.email_id = request.user.id
                rec.proj_tag="cons"                
                rec.save()
                messages.success(request,('Record has been added successfully!'))                
                return redirect("catg_3:resch-view", user_id=rec.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)          
            
    
    context = {
        'form1': form1,
    }
    
    return render(request, 'catg_3/resch_cons_add.html', context)
      
   

def resch_edit(request, pk):
    res = Resch_proj.objects.get(id=pk)
    
    form1 = Resch_projForm(instance=res)
    user_id=res.email_id
    res_id=res.id
    
    if request.method == 'POST':
            form1 = Resch_projForm(request.POST, request.FILES, instance=res)
            if form1.is_valid():                
                form1.save()
                print("Saved")    
                messages.success(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
            
                
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'res_id': res_id,
        'res':res,
        
        }
    
    return render(request, 'catg_3/edit_resch_proj.html', context)
    
    

def resch_cons_edit(request, pk):
    cons = Resch_cons.objects.get(id=pk)
    
    form1 = Resch_consForm(instance=cons)
    user_id=cons.email_id
    cons_id=cons.id
    
    if request.method == 'POST':
            form1 = Resch_consForm(request.POST, request.FILES, instance=cons)
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
            
                
    context = {
        'form1': form1,
        'user_id': user_id,
        'cons_id': cons_id,
        'cons':cons,
        
        }
    
    return render(request, 'catg_3/edit_resch_cons.html', context)    

def resch_delete(request, pk):
    res = Resch_proj.objects.get(id=pk)
    
    if request.method == "POST":
        res.delete()
        return redirect("catg_3:resch-view", user_id=res.email_id)
        
    context = {'item':res}
    return render(request, 'catg_3/resch_delete.html', context)
    
def resch_cons_delete(request, pk):
    res = Resch_cons.objects.get(id=pk)
    
    if request.method == "POST":
        res.delete()
        return redirect("catg_3:resch-view", user_id=res.email_id)
        
    context = {'item':res}
    return render(request, 'catg_3/resch_cons_delete.html', context)    


@login_required(login_url="login")
def prj_add(request):

    form1 = Prj_outcmForm()
    
    
    if request.method == 'POST':
         
            form1 = Prj_outcmForm(request.POST, request.FILES)
            if form1.is_valid():
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:resch-view", user_id=rec.email_id)
                # return redirect(request.path)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)                
     
    context = {
        'form1': form1,
            
        }
    return render(request, 'catg_3/prj_add.html', context)


def prj_delete(request, pk):
    prj = Prj_outcm.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:resch-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/prj_delete.html', context)


def prj_edit(request, pk):
    prj = Prj_outcm.objects.get(id=pk)
    
    form1 = Prj_outcmForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Prj_outcmForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!')) 
                #return redirect("catg_3:resch-view", user_id=prj.email_id)                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_prj_outcm.html', context)
    
    
def resch_guide_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
    
    
    account = Account.objects.get(pk=user_id)    
    

    context = {}
    prj = account.resch_guide_set.all()
    
    prj_count = prj.count()
       
    context = {                
        'prj': prj,                            
        'prj_count': prj_count,
        'pk_var': pk_var,
        'user_var': user_var,
    }

    return render(request, "catg_3/resch_guide.html", context)

@login_required(login_url="login")
def resch_guide_add(request):
     
    form1 = Resch_guideForm()
    
    
    
    if request.method == 'POST':
         
            form1 = Resch_guideForm(request.POST, request.FILES)
            
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:resch-guide-view", user_id=rec.email_id)
                # return redirect(request.path)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)     
                
    
            
    context = {
        'form1': form1,
             
        }
    return render(request, 'catg_3/resch_guide_add.html', context) 

    
def resch_guide_delete(request, pk):
    prj = Resch_guide.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:resch-guide-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/resch_guide_delete.html', context)
    
    
def resch_guide_edit(request, pk):
    prj = Resch_guide.objects.get(id=pk)
    
    form1 = Resch_guideForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Resch_guideForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.success(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_resch_guide.html', context)    
    

    
def fellow_award_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
    
    
    account = Account.objects.get(pk=user_id) 
    
    api_cap = 0
    
    if account.to_dsg == 'Stage 2':
        api_cap = 4        
    elif account.to_dsg == 'Stage 3':
        api_cap = 10 
    elif account.to_dsg == 'Stage 4':
        api_cap = 15     
    elif account.to_dsg == 'Stage 5':
        api_cap = 20 
    

    context = {}
    prj = account.fellow_award_set.all()
    lec = account.lecture_paper_set.all()
    elearn = account.e_learning_set.all()
    
    prj_count = prj.count()
    lec_count = lec.count()
    elearn_count = elearn.count()
    
    context = {                
        'prj': prj,
        'lec': lec,    
        'prj_count': prj_count,
        'lec_count': lec_count,
        'pk_var': pk_var,
        'user_var': user_var,
        'elearn' : elearn,
        'elearn_count' : elearn_count,
        'account' : account,
        'api_cap' : api_cap,
    }

    return render(request, "catg_3/fellow_award_view.html", context)

        
@login_required(login_url="login")
def fellow_award_add(request):
      
    form1 = Fellow_AwardForm()
    
    
    
    if request.method == 'POST':
         
            form1 = Fellow_AwardForm(request.POST, request.FILES)
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:fellow-award-view", user_id=rec.email_id)
                #return redirect("fellow-award-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)     
                
    context = {
        'form1': form1,
    }
    
    return render(request, 'catg_3/fellow_award_add.html', context)
           
  
def fellow_award_delete(request, pk):
    prj = Fellow_Award.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/fellow_award_delete.html', context) 

def fellow_award_edit(request, pk):
    prj = Fellow_Award.objects.get(id=pk)
    
    form1 = Fellow_AwardForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Fellow_AwardForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_fellow_award.html', context)  

@login_required(login_url="login") 
def lecture_paper_add(request):

    form1 = Lecture_PaperForm()
    
    
    
    if request.method == 'POST':
         
            form1 = Lecture_PaperForm(request.POST, request.FILES)
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:fellow-award-view", user_id=rec.email_id)
                #return redirect("lecture-paper-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)     
    
    context = {
        'form1': form1,
    }
    return render(request, 'catg_3/lecture_paper_add.html', context)
    
def lecture_paper_delete(request, pk):
    prj = Lecture_Paper.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/lecture_paper_delete.html', context) 
        
        

def lecture_paper_edit(request, pk):
    prj = Lecture_Paper.objects.get(id=pk)
    
    form1 = Lecture_PaperForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = Lecture_PaperForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_lecture_paper.html', context)  

@login_required(login_url="login") 
def lecture_elearn_add(request):
 
    form1 = E_LearningForm()
    
    
    if request.method == 'POST':
         
            form1 = E_LearningForm(request.POST, request.FILES)
            
            if form1.is_valid():                            
                rec = form1.save(commit=False)
                rec.email_id = request.user.id    
                rec.save()
                messages.success(request,('Record has been added successfully!'))
                return redirect("catg_3:fellow-award-view", user_id=rec.email_id)
                #return redirect("lecture-elearn-add")
                # return redirect(request.path)
                # return redirect("catg_3:jrnl-pub", user_id=jrnl.email_id)
            else :                
                error_string = ' '.join([' '.join(x for x in l) for l in list(form1.errors.values())])
                messages.error(request,error_string)
                return redirect(request.path)     
      
                
    context = {
        'form1': form1,       
        }
    return render(request, 'catg_3/lecture_elearn_add.html', context)

   
def lecture_elearn_delete(request, pk):
    prj = E_Learning.objects.get(id=pk)
    
    if request.method == "POST":
        prj.delete()
        return redirect("catg_3:fellow-award-view", user_id=prj.email_id)
        
    context = {'item':prj}
    return render(request, 'catg_3/lecture_elearn_delete.html', context) 
        
        

def lecture_elearn_edit(request, pk):
    prj = E_Learning.objects.get(id=pk)
    
    form1 = E_LearningForm(instance=prj)
    user_id=prj.email_id
    prj_id=prj.id
    
    if request.method == 'POST':
            form1 = E_LearningForm(request.POST, request.FILES, instance=prj)
            
            if form1.is_valid():                
                form1.save()
                messages.error(request,('Record has been modified succesfully!'))                
                return redirect(request.path)
                 
    context = {
        'form1': form1,
        'user_id': user_id,
        'prj_id': prj_id,
        'prj':prj,
        
        }
    
    return render(request, 'catg_3/edit_lecture_elearn.html', context)  

    

def api_summary_view(request,*args, **kwargs):
    
    user_id = kwargs.get("user_id")
    user = request.user    
    
    if not request.user.is_authenticated:
        return redirect("login")    
    
    if user.is_admin:
        user_id = kwargs.get("user_id")
    else:        
        user_id = request.user.id
   
    global pk_var
    pk_var = user_id
    
    global user_var
    user_var = user_id 
    
    account = Account.objects.get(pk=user_id)

    valid_form=0
    if not account.frm_general_info:
        messages.error(request,"Please complete 'General Information' page")
        return redirect("account:home", user_id=request.user.id)
    valid_form=valid_form+1
    
    try :
        api1 = ApiCatg_I.objects.get(pk=user_id)
        if not api1.direct_teaching:
            messages.error(request,"Catg-I is incomplete")
            return redirect("account:home", user_id=request.user.id)
        valid_form=valid_form+1
        
    except ApiCatg_I.DoesNotExist:
        #return HttpResponse(messages,"API-Catg-I is not completed")
        messages.error(request,"Catg-I is incomplete")
        return redirect("account:home", user_id=request.user.id)
        
    else:
        pass      
            
    try :
      api2 = ApiCatg_II.objects.get(pk=user_id)
      if not api2.field_based_activities:
            messages.error(request,"Catg-II is incomplete")
            return redirect("account:home", user_id=request.user.id)
      valid_form=valid_form+1
      
    except ApiCatg_II.DoesNotExist:
        #return HttpResponse(messages,"API-Catg-II is not completed")
        messages.error(request,"Catg_II is incomplete")                
        return redirect("account:home", user_id=request.user.id)
        
    else:
        pass
        
    academy = account.academic_set.all()    
    curpost = account.presentpost_set.all() 
    
    try :
        teach = TeachingExp.objects.get(pk=user_id)
        valid_form=valid_form+1    
    except TeachingExp.DoesNotExist:
        teach = False
        pass
     
    orient = account.orientation_set.all()
    
    if academy :
        valid_form=valid_form+1
        
    if curpost :
        valid_form=valid_form+1
        
    if orient :
        valid_form=valid_form+1           
    else:            
        if account.from_dsg == "Stage 4":
            valid_form=valid_form+1
              
    print('l-1861',valid_form)
    
    casform = CasFormSts.objects.get(pk=user_id)
    
    if valid_form == 7:
            casform.final_sts=True 
    else:
            casform.final_sts=False
            
    if not casform.final_sts:
        messages.error(request,"Please check the mandatory pages")
        return redirect("account:home", user_id=request.user.id)
    
    #api1 = ApiCatg_I.objects.get(pk=user_id)
    #api2 = ApiCatg_II.objects.get(pk=user_id)
    
    jrnl = account.jrnl_pub_set.all()
    pub = account.pub_other_set.all()
    jrnl_paper = account.jrnlpaper_ugc_set.all()
    res = account.resch_proj_set.all()
    cons = account.resch_cons_set.all()
    out = account.prj_outcm_set.all()
    guide = account.resch_guide_set.all()
    
    
    fell = account.fellow_award_set.all()
    lec = account.lecture_paper_set.all()
    elearn = account.e_learning_set.all()
    
   
    
    context = {}
    
    context = {
                'account': account,
                
                'api1':api1,
                'api2':api2,
                
                'jrnl': jrnl,
                'pub': pub,
                'jrnl_paper':jrnl_paper,
                'res' : res,
                'cons': cons,
                'out' : out,
                'guide': guide,
                'fell': fell,
                'lec': lec,
                'elearn' : elearn,
            
                'pk_var': pk_var,
                'user_var': user_var,               
                
    }
    
    return render(request, "catg_3/api_summary_view.html", context)

def cas_sts_view(request,*args, **kwargs):

    user_id = request.user.id
    user = request.user
    
    if not request.user.is_authenticated:
        return redirect("login")
        
    context={}
    
    if user.is_admin:
        account=Account.objects.all().order_by('username')        
        academy  = Academic.objects.all().order_by('email_id')
        research = Research.objects.all().order_by('email_id')        
        priorpost = PriorPost.objects.all().order_by('email_id')
        presentpost = PresentPost.objects.all().order_by('email_id')                      
        teachingexp = TeachingExp.objects.all().order_by('email_id')                      
        orientation =  Orientation.objects.all().order_by('email_id')        
        api1 =     ApiCatg_I.objects.all().order_by('email_id')        
        api2 =     ApiCatg_II.objects.all().order_by('email_id')
        
        jrnl_pub = Jrnl_pub.objects.all().order_by('email_id')   
        pub_other = Pub_other.objects.all().order_by('email_id')
        ugs_jrnl = JrnlPaper_UGC.objects.all().order_by('email_id')       
        resch_proj = Resch_proj.objects.all().order_by('email_id')
        resch_cons = Resch_cons.objects.all().order_by('email_id')
        prj_outcm = Prj_outcm.objects.all().order_by('email_id')
        resch_guide = Resch_guide.objects.all().order_by('email_id')
        fellow_award = Fellow_Award.objects.all().order_by('email_id')
        lecture_paper = Lecture_Paper.objects.all().order_by('email_id')
        e_learning = E_Learning.objects.all().order_by('email_id')
        
        
        cas_sts = CasFormSts.objects.all()
        
        gen_info = account.filter(frm_general_info='True').count()
        frm_sub = account.filter(frm_submitted='True').count()
        tot_user = account.count() 
        only_reg = tot_user - gen_info
        gen_info = gen_info - frm_sub
        
        for i in cas_sts:
            c_no = 0
            for x in academy:
                if x.email_id == i.email_id:
                   c_no += 1                   
                   i.academy_sts = True
            i.academy_no = c_no
            
            c_no = 0
            for x in research:
                if x.email_id == i.email_id:
                   c_no += 1                   
                   i.research_paper_sts = True
            i.research_paper_no = c_no
           
            c_no = 0
            for x in priorpost:
                if x.email_id == i.email_id:
                   c_no += 1                   
                   i.priorpost_sts = True
            i.priorpost_no = c_no

            c_no = 0
            for x in presentpost:
                if x.email_id == i.email_id:
                   c_no += 1                   
                   i.present_post_sts = True
            i.present_post_no = c_no
            
            c_no = 0
            for x in teachingexp:
                if x.email_id == i.email_id and x.pg_class:
                   c_no += 1                   
                   i.teaching_sts = True
            i.teaching_no = c_no
            
            c_no = 0       
            for x in orientation:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.orientation_sts = True
            i.orientation_no = c_no
            
            c_no = 0
            for x in api1:
                if x.email_id == i.email_id and x.actl_api_dt:
                   c_no += 1
                   i.api_catg1_sts = True
            i.api_catg1_no = c_no
            
            c_no = 0
            for x in api2:
                if x.email_id == i.email_id and x.actl_api_fba:
                   c_no += 1
                   i.api_catg2_sts = True
            i.api_catg2_no = c_no
            c_no = 0

            for x in jrnl_pub:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.jrnl_pub_sts = True
            i.jrnl_pub_no = c_no
            c_no = 0
            
            for x in pub_other:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.pub_other_sts = True
            i.pub_other_no = c_no
            c_no = 0
            
            for x in ugs_jrnl:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.jrnlpaper_sts = True
            i.jrnlpaper_no = c_no
            c_no = 0

            for x in resch_proj:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.resch_proj_sts = True
            i.resch_proj_no = c_no
            c_no = 0

            for x in resch_cons:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.resch_cons_sts  = True
            i.resch_cons_no = c_no
            c_no = 0

            for x in prj_outcm:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.prj_outcm_sts = True
            i.prj_outcm_no = c_no
            c_no = 0

            for x in resch_guide:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.resch_guide_sts = True
            i.resch_guide_no = c_no
            c_no = 0

            for x in fellow_award:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.fellow_award_sts = True
            i.fellow_award_no = c_no
            c_no = 0

            for x in lecture_paper:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.lecture_paper_sts = True
            i.lecture_paper_no = c_no
            c_no = 0

            for x in e_learning:
                if x.email_id == i.email_id:
                   c_no += 1
                   i.e_learning_sts = True
            i.e_learning_no = c_no
            c_no = 0
            
        i.save()            
            
        #qs = Bank.objects.values('name').annotate(count=Count('name')).order_by('name').distinct()
       
        
        context={       
        "account"     : account,
        "cas_sts"     : cas_sts,
        "gen_info"    : gen_info,
        "frm_sub"     : frm_sub,
        "tot_user"    : tot_user,
        "only_reg"    : only_reg, 
        }
        
        
            
        return render(request, "catg_3/cas_sts_3.html", context)
        
    return redirect("account:home", user_id=request.user.id) 
     