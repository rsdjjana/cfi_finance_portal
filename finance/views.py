from django.http import HttpResponse,Http404
from django.shortcuts import *
from finance.forms import *
from django.contrib import auth
from django.forms.models import modelformset_factory
from datetime import date

def login(request):
    if request.method=='POST':
        loginform=LoginForm(request.POST)
        if loginform.is_valid():
            username1=loginform.cleaned_data["username"]
            password1=loginform.cleaned_data["password"]
            user=auth.authenticate( username=username1, password=password1 )
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    return HttpResponseRedirect('home/')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse("User is not registered")
                
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        else:
            loginform=LoginForm()
    return render_to_response('login.html',locals(),context_instance=RequestContext(request))
    
    
def logout(request):
    auth.logout(request)
    loginform=LoginForm()
    return HttpResponseRedirect('/')
    #return render_to_response('login.html',locals(),context_instance=RequestContext(request))
    
def home(request):
    if request.user.is_authenticated():
        home123=True
        userprofile=UserProfile.objects.get(user=request.user)
        return render_to_response('finance/home.html',locals(),context_instance=RequestContext(request))
    else:
        return HttpResponse("oops wrong page!")
        
        
def advance(request):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if not userprofile.is_core:
            advance123=True #for making the top nav bar active
            advance_applications=Advance.objects.filter(project=userprofile.project)
            number_await_approval=len(Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=False))
            number_approved_not_rec=len(Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=False))
            number_rec_add_bills=len(Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=True).filter(bill_submitted=False))
            number_disapproved_unread=len(Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False))
            advance_applications_awaiting_approval=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=False)
            approved_not_rec=Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=False)
            rec_add_bills=Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=True).filter(bill_submitted=False)
            disapproved_unread=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False)
            if request.method=='POST':
                advanceform=AdvanceForm(request.POST)
                if advanceform.is_valid():
                    advanceform1=advanceform.save(commit=False)
                    advanceform1.applied_date=date.today()
                    advanceform1.project=userprofile.project
                    advanceform1.save()
                else:
                    advanceform_error=True
                    
                if "read" in request.POST:  
                    print "hello there"
                    read1=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False)
                    for read2 in read1:
                        read2.read=True
                        read2.save()
                return HttpResponseRedirect('/advance')
                
            else:
                advanceform=AdvanceForm()  
            
        else:
            advancereq123=True #for making the top nav bar active
            pending_advance_app=Advance.objects.filter(approved=False).filter(disapproved=False)
            AdvanceCoreFormset=modelformset_factory(Advance,fields=('approved','disapproved','core_comment'))
            if request.method=='POST':
                #advance_form_core_approval=AdvanceFormCoreApproval(request.POST,instance=)
                advance_core_formset=AdvanceCoreFormset(request.POST,queryset=pending_advance_app)
                for form in advance_core_formset.forms:
                    if form.has_changed():
                        form.save()
                return HttpResponseRedirect('/advance')
            else:
                advance_core_formset=AdvanceCoreFormset(queryset=pending_advance_app)
                
        return render_to_response('finance/advance.html',locals(),context_instance=RequestContext(request))      
    else:
        raise Http404        
            
def advance_bill(request,advance_id):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            advance_application=Advance.objects.get(id=advance_id)
            qset=BillDetail.objects.filter(is_advance=True).filter(advance=advance_application)
            return render_to_response('finance/advance_bill.html',locals(),context_instance=RequestContext(request))
            
        else:
            BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','purchase_detail','amount','dated'),extra=2,  can_delete=True)
            advance_application=Advance.objects.get(id=advance_id)
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=True).filter(advance=advance_application)
            
            if request.method=='POST':
                billformset=BillFormset(request.POST,queryset=qset)
                for form in billformset.forms:
                    if form.has_changed():
                        if form not in billformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            form_instance.is_advance=True
                            form_instance.project=userprofile.project
                            form_instance.advance=advance_application
                            form_instance.save()
                        else:
                            if BillDetail.objects.filter(id=form.instance.id):
                                form_instance=BillDetail.objects.get(id=form.instance.id)
                                form_instance.delete()
                                
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=True).filter(advance=advance_application)
            billformset=BillFormset(queryset=qset)
            return render_to_response('finance/advance_bill.html',locals(),context_instance=RequestContext(request))
    else:
        raise Http404            


def advance_bill_view(request,advance_id):
    if request.user.is_authenticated():
        advance123=True
        userprofile=UserProfile.objects.get(user=request.user)
        advance_application=Advance.objects.get(id=advance_id)
        qset=BillDetail.objects.filter(is_advance=True).filter(advance=advance_application)
        return render_to_response('finance/advance_bill_view.html',locals(),context_instance=RequestContext(request))
            
            
            
'''
def reimb(request):
    userprofile=UserProfile.objects.get(user=request.user)
    
    if request.method=='POST':
        reimbform=ReimbForm(request.POST)
        if reimbform.is_valid():
            reimbform1=reimbform.save(commit=False)
            reimbform1.applied_date=date.today()
            reimbform1.project=userprofile.project
            reimbform1.save()
        else:
            reimbform_error=True
        return HttpResponseRedirect('/reimb')
        
    else:
        reimbform=ReimbForm()  
    return render_to_response('finance/reimb.html',locals(),context_instance=RequestContext(request))      
    
'''
    
    
def advance_approved(request):
    if request.user.is_authenticated():
        advance
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            advanceapp123=True #for making the top nav bar active
            approved_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=True)   
            approved_not_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=False)
            ApprovedCoreFormset=modelformset_factory(Advance,fields=('received','receive_date','due_date','core_comment','bill_submitted'))
            if request.method=='POST':
                approved_core_formset=ApprovedCoreFormset(request.POST,queryset=approved_not_submitted)
                for form in approved_core_formset.forms:
                    if form.has_changed():
                        form.save()
                return HttpResponseRedirect('/advance/approved')
            else:
                approved_core_formset=ApprovedCoreFormset(queryset=approved_not_submitted)
            return render_to_response('finance/advance_approved.html',locals(),context_instance=RequestContext(request))    
        else:
            raise Http404
    else:
        raise Http404
            
def reimb(request):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            reimb123=True
            ReimbFormset=modelformset_factory(Reimb,fields=('received','received_date','submitted'))
            #ReimbFormsetNotSubmitted=modelformset_factory(Reimb,fields=('received','received_date','submitted'))
            qsetreimb=Reimb.objects.all().order_by('submitted')
            #qsetreimbnotsub=Reimb.objects.filter(submitted=False)
            if request.method=='POST':
                reimbformset=ReimbFormset(request.POST,queryset=qsetreimb)
                #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(request.POST,queryset=qsetreimbnotsub)
                for form in reimbformset.forms:
                    if form.has_changed():
                        form.save()
                #for form in reimbformsetnotsubmitted.forms:
                    #if form.has_changed():
                        #form.save()        
            else:
                reimbformset=ReimbFormset(queryset=qsetreimb)
                #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(queryset=qsetreimbnotsub)
            reimb_submitted=Reimb.objects.filter(submitted=True)
            reimb_not_submitted=Reimb.objects.filter(submitted=False)
            qset=BillDetail.objects.filter(is_advance=False)
            qsetreimb=Reimb.objects.all().order_by('submitted')
            return render_to_response('finance/reimb_bill.html',locals(),context_instance=RequestContext(request))
            
        else:
            reimb123=True
            BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','purchase_detail','amount','dated'),extra=2, can_delete=True)
            reimb_applications=Reimb.objects.filter(project=userprofile.project)
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=False)
            if request.method=='POST':
                reimbform=ReimbForm(request.POST)
                if reimbform.is_valid():
                    reimbform1=reimbform.save(commit=False)
                    reimbform1.applied_date=date.today()
                    reimbform1.project=userprofile.project
                    reimbform1.save()
                else:
                    reimbform_error=True
                billformset=BillFormset(request.POST,queryset=qset)
                for form in billformset.forms:
                    if form.has_changed():
                        if form not in billformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            form_instance.is_advance=False
                            form_instance.project=userprofile.project
                            form_instance.reimb=reimbform1
                            form_instance.save()
                        else:
                            if BillDetail.objects.filter(id=form.instance.id):
                                form_instance=BillDetail.objects.get(id=form.instance.id)
                                form_instance.delete()            
                
                return HttpResponseRedirect('/reimb')
                
            else:
                reimbform=ReimbForm()
            reimbset=Reimb.objects.filter(project=userprofile.project).order_by('received')
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=False)
            #BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','purchase_detail','amount','dated'),extra=2, can_    delete=T    rue)
            qset1=BillDetail.objects.filter(id=0)
            billformset=BillFormset(queryset=qset1)
            return render_to_response('finance/reimb_bill.html',locals(),context_instance=RequestContext(request))        
    else:
        raise Http404
            
def bills(request):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            bills123=True
            advance_bills_not_sub=BillDetail.objects.filter(core_submitted=False).filter(is_advance=True)
            reimb_bills_not_sub=BillDetail.objects.filter(core_submitted=False).filter(is_advance=False)
            advance_bills_sub=BillDetail.objects.filter(core_submitted=True).filter(is_advance=True)
            reimb_bills_sub=BillDetail.objects.filter(core_submitted=True).filter(is_advance=False)
            return render_to_response('finance/bills.html',locals(),context_instance=RequestContext(request))

        else:
            raise Http404()
    else:
        raise Http404
