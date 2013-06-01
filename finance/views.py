from django.http import HttpResponse,Http404
from django.shortcuts import *
from finance.forms import *
from django.contrib import auth
from django.forms.models import modelformset_factory
from datetime import date
from django.forms import *
import xlwt
from django.forms.extras.widgets import SelectDateWidget

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
            return HttpResponseRedirect('home/')
        else:
            loginform=LoginForm()
    return render_to_response('login.html',locals(),context_instance=RequestContext(request))
    
    
def logout(request):
    auth.logout(request)
    loginform=LoginForm()
    return HttpResponseRedirect('/ ')
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
            if request.method=='POST':
                advanceform=AdvanceForm(request.POST)
                if advanceform.is_valid():
                    advanceform1=advanceform.save(commit=False)
                    advanceform1.applied_date=date.today()
                    advanceform1.project=userprofile.project
                    advanceform1.save()
                    advanceform_success=True
                    advanceform=AdvanceForm()
                else:
                    advanceform_error=True
                    
                if "read" in request.POST:  
                    read1=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False)
                    for read2 in read1:
                        read2.read=True
                        read2.save()
                    advanceform_error=False
                #return HttpResponseRedirect('/advance')
            else:
                advanceform=AdvanceForm()  
            advance123=True #for making the top nav bar active
            advance_applications=Advance.objects.filter(project=userprofile.project).order_by('-applied_date')
            number_await_approval=len(Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=False))
            number_approved_not_rec=len(Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=False))
            number_rec_add_bills=len(Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=True).filter(bill_submitted=False))
            number_disapproved_unread=len(Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False))
            advance_applications_awaiting_approval=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=False).order_by('-applied_date')
            approved_not_rec=Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=False).order_by('-approved_date')
            rec_add_bills=Advance.objects.filter(project=userprofile.project).filter(approved=True).filter(received=True).filter(bill_submitted=False).order_by('-receive_date')
            disapproved_unread=Advance.objects.filter(project=userprofile.project).filter(approved=False).filter(disapproved=True).filter(read=False).order_by('-applied_date')
            return render_to_response('finance/advance.html',locals(),context_instance=RequestContext(request))     
        else:
            advancereq123=True #for making the top nav bar active
            pending_advance_app=Advance.objects.filter(approved=False).filter(disapproved=False)
            AdvanceCoreFormset=modelformset_factory(Advance,fields=('approved','disapproved','core_comment',))
            if request.method=='POST':
                advance_core_formset=AdvanceCoreFormset(request.POST,queryset=pending_advance_app)
                for form in advance_core_formset.forms:
                    if form.has_changed():
                        form.save()
                advance_request_form_success=True
            else:
                advance_core_formset=AdvanceCoreFormset(queryset=pending_advance_app)
            advancereq123=True #for making the top nav bar active
            pending_advance_app=Advance.objects.filter(approved=False).filter(disapproved=False)
            AdvanceCoreFormset=modelformset_factory(Advance,fields=('approved','disapproved','core_comment',))
                
        return render_to_response('finance/advance.html',locals(),context_instance=RequestContext(request))      
    else:
        raise Http404        
            
def advance_bill(request,advance_id):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            advanceapp123=True
            advance_application=Advance.objects.get(id=advance_id)
            purchase_details=PurchaseDetail.objects.all()
            qset=BillDetail.objects.filter(is_advance=True).filter(advance=advance_application)
            return render_to_response('finance/advance_bill.html',locals(),context_instance=RequestContext(request))
            
        else:
            n=1
            m=1
            advance123=True
            BillFormset=modelformset_factory(BillDetail, fields=('shop_name','bill_number','amount','dated','date'), extra=n, can_delete=True)
            #PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'),extra=m, can_delete=True,)
            advance_application=Advance.objects.get(id=advance_id)
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=True).filter(advance=advance_application)
            #qset_purchase=PurchaseDetail.objects.all()
            
            #purchase1=PurchaseDetail.objects.all()
            """
            does_exist=False
            for qset1 in qset:
                for purchase2 in purchase1:
                    if purchase2.bill == qset1:
                        does_exist=True
                if not does_exist:
                    new=PurchaseDetail(bill=qset1)
                    new.save()
            """
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
                if "add_more" in request.POST:
                    n=1 
                    BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','amount','dated','date'),extra=n,  can_delete=True)
                
                qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=True).filter(advance=advance_application)
                bill_ids=[]
                for bill123 in qset:
                    bill_ids.append(int(bill123.id))
                print bill_ids
                
                for bill_id in bill_ids:
                    if str(bill_id) in request.POST:
                        bill_id_final=bill_id
                        return HttpResponseRedirect('/advance/bill/purchase_details/' + str(advance_id) + '/' + str(bill_id_final))
                        
                """                       
                purchasedetailformset=PurchaseDetailFormset(request.POST,queryset=qset_purchase)
                for form in purchasedetailformset.forms:
                    if form.has_changed():
                        if form not in purchasedetailformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            bill2=BillDetail.objects.get(id=bill_id_final)
                            form_instance.bill=bill2
                            form_instance.save()
                        else:
                            if PurchaseDetail.objects.filter(id=form.instance.id):
                                form_instance=PurchaseDetail.objects.get(id=form.instance.id)
                                form_instance.delete()
                if "add_more1" in request.POST:
                    m=1 
                    PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'),extra=m, can_delete=True)
               """
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=True).filter(advance=advance_application)
            #qset_purchase=PurchaseDetail.objects.all()
            billformset=BillFormset(queryset=qset)
            #purchasedetailformset=PurchaseDetailFormset(queryset=qset_purchase)
            return render_to_response('finance/advance_bill.html',locals(),context_instance=RequestContext(request))
    else:
        raise Http404            


def advance_bill_view(request,advance_id):
    if request.user.is_authenticated():
        advance123=True
        userprofile=UserProfile.objects.get(user=request.user)
        advance_application=Advance.objects.get(id=advance_id)
        qset=BillDetail.objects.filter(is_advance=True).filter(advance=advance_application)
        purchase_details=PurchaseDetail.objects.all()
        return render_to_response('finance/advance_bill_view.html',locals(),context_instance=RequestContext(request))
   
def bill_purchase_detail(request,advance_id,bill_id):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        advance_application=Advance.objects.get(id=advance_id)
        if not userprofile.is_core:
            m=0
            advance123=True
            PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'), can_delete=True)
            current_bill=BillDetail.objects.get(id=bill_id)
            qset_purchase=PurchaseDetail.objects.filter(bill=current_bill)
            if request.method=='POST':
                purchasedetailformset=PurchaseDetailFormset(request.POST,queryset=qset_purchase)
                for form in purchasedetailformset.forms:
                    if form.has_changed():
                        if form not in purchasedetailformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            bill2=BillDetail.objects.get(id=bill_id)
                            form_instance.bill=bill2
                            form_instance.save()
                        else:
                            if PurchaseDetail.objects.filter(id=form.instance.id):
                                form_instance=PurchaseDetail.objects.get(id=form.instance.id)
                                form_instance.delete()
                if "add_more" in request.POST:
                    m=2 
                    PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'),extra=m, can_delete=True)
            qset_purchase=PurchaseDetail.objects.filter(bill=current_bill)
            purchasedetailformset=PurchaseDetailFormset(queryset=qset_purchase)
            return render_to_response('finance/bill_purchase_detail.html',locals(),context_instance=RequestContext(request))
    else:
        return Http404
            
def advance_approved(request):
    if request.user.is_authenticated():
        advance
        userprofile=UserProfile.objects.get(user=request.user)
        advance_approved_form_error=False
        if userprofile.is_core:
            advanceapp123=True #for making the top nav bar active
            approved_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=True)   
            approved_not_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=False)
            ApprovedCoreFormset=modelformset_factory(Advance,fields=('received','receive_date','due_date','core_comment','bill_submitted'))
            if request.method=='POST':
                approved_core_formset=ApprovedCoreFormset(request.POST,queryset=approved_not_submitted)
                for form in approved_core_formset.forms:
                    if form.has_changed():
                        if form.is_valid():
                            form.save()
                        else:
                            advance_approved_form_error=True
                if not advance_approved_form_error:
                    advance_approved_form_success=True
            else:
                approved_core_formset=ApprovedCoreFormset(queryset=approved_not_submitted)
            advanceapp123=True #for making the top nav bar active
            approved_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=True)   
            approved_not_submitted=Advance.objects.filter(approved=True).filter(bill_submitted=False)
            ApprovedCoreFormset=modelformset_factory(Advance,fields=('received','receive_date','due_date','core_comment','bill_submitted'))
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
            qsetreimb=Reimb.objects.filter(request_sent=True).order_by('submitted')
            qsetreimb_not_yet_submitted=Reimb.objects.filter(submitted=False).filter(request_sent=True)
            qsetreimb_submitted_not_received=Reimb.objects.filter(submitted=True).filter(received=False).filter(request_sent=True)
            qsetreimb_submitted_received=Reimb.objects.filter(submitted=True).filter(received=True).filter(request_sent=True)
            
            #qsetreimbnotsub=Reimb.objects.filter(submitted=False)
            if request.method=='POST':
                if "one" in request.POST:
                    reimbformset1=ReimbFormset(request.POST,queryset=qsetreimb_not_yet_submitted)
                    #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(request.POST,queryset=qsetreimbnotsub)
                    for form in reimbformset1.forms:
                        if form.has_changed():
                            form.save()
                if "two" in request.POST:
                    reimbformset2=ReimbFormset(request.POST,queryset=qsetreimb_submitted_not_received)
                    #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(request.POST,queryset=qsetreimbnotsub)
                    for form in reimbformset2.forms:
                        if form.has_changed():
                            form.save()
                if "three" in request.POST:
                    reimbformset3=ReimbFormset(request.POST,queryset=qsetreimb_submitted_received)
                    #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(request.POST,queryset=qsetreimbnotsub)
                    for form in reimbformset3.forms:
                        if form.has_changed():
                            form.save()

  
                #for form in reimbformsetnotsubmitted.forms:
                    #if form.has_changed():
                        #form.save()        
            else:
                reimbformset1=ReimbFormset(queryset=qsetreimb_not_yet_submitted)
                reimbformset2=ReimbFormset(queryset=qsetreimb_submitted_not_received)
                reimbformset3=ReimbFormset(queryset=qsetreimb_submitted_received)
                
                #reimbformsetnotsubmitted=ReimbFormsetNotSubmitted(queryset=qsetreimbnotsub)
            reimbformset1=ReimbFormset(queryset=qsetreimb_not_yet_submitted)
            reimbformset2=ReimbFormset(queryset=qsetreimb_submitted_not_received)
            reimbformset3=ReimbFormset(queryset=qsetreimb_submitted_received)    
            reimb_submitted=Reimb.objects.filter(submitted=True).filter(request_sent=True)
            reimb_not_submitted=Reimb.objects.filter(submitted=False).filter(request_sent=True)
            qsetreimb_not_yet_submitted=Reimb.objects.filter(submitted=False).filter(request_sent=True)
            qsetreimb_submitted_not_received=Reimb.objects.filter(submitted=True).filter(received=False).filter(request_sent=True)
            qsetreimb_submitted_received=Reimb.objects.filter(submitted=True).filter(received=True).filter(request_sent=True)
            qset=BillDetail.objects.filter(is_advance=False)
            qsetreimb=Reimb.objects.filter(request_sent=True).order_by('submitted')
            purchase_details=PurchaseDetail.objects.all()
            return render_to_response('finance/reimb_bill.html',locals(),context_instance=RequestContext(request))
            
        else:
            reimb1=Reimb.objects.filter(request_sent=False)
            if not reimb1:
                reimb2=Reimb(project=userprofile.project)
                reimb2.save()
            else:
                for reimb3 in reimb1:
                    reimb2=reimb3
                
            return HttpResponseRedirect('/reimb/request/' + str(reimb2.id))
            '''
            reimb123=True
            extra1=2
            BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','purchase_detail','amount','dated','date'),extra=10,)
            reimb_applications=Reimb.objects.filter(project=userprofile.project)
            bills_limit=5
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=False)
            if request.method=='POST':
                reimbform=ReimbForm(request.POST)
                if reimbform.is_valid():
                    reimbform1=reimbform.save(commit=False)
                    reimbform1.applied_date=date.today()
                    reimbform1.project=userprofile.project
                    reimbform1.save()
                    form1_success=True
                else:
                    reimbform_error=True
                billformset=BillFormset(request.POST,queryset=qset)
                for form in billformset.forms:
                    if form.has_changed():
                        form_instance=form.save(commit=False)
                        form_instance.is_advance=False
                        form_instance.project=userprofile.project
                        form_instance.reimb=reimbform1
                        form_instance.save() 
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=False)
            bill_ids=[]
            for bill123 in qset:
                bill_ids.append(int(bill123.id))
            for bill_id in bill_ids:
                if str(bill_id) in request.POST:
                    bill_id_final=bill_id
                    return HttpResponseRedirect('/reimb/bill/purchase_details/' + str(bill_id_final))
                
            else:
                reimbform=ReimbForm()
            reimbform=ReimbForm()
            reimbset_not_received=Reimb.objects.filter(project=userprofile.project).filter(received=False)
            reimbset_received=Reimb.objects.filter(project=userprofile.project).filter(received=True)
            qset=BillDetail.objects.filter(project=userprofile.project).filter(is_advance=False)
            #BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','purchase_detail','amount','dated'),extra=2, can_    delete=T    rue)
            qset1=BillDetail.objects.filter(id=0)
            billformset=BillFormset(queryset=qset1)
            return render_to_response('finance/reimb_bill.html',locals(),context_instance=RequestContext(request))        
            '''
    else:
        raise Http404
        
def reimb_request(request,reimb_id):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if not userprofile.is_core:
            reimb123=True
            current_reimb=Reimb.objects.get(id=reimb_id)
            BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','amount','dated','date'),can_delete=True)
            qset=BillDetail.objects.filter(reimb=current_reimb)
            if request.method=='POST':
                billformset=BillFormset(request.POST,queryset=qset)
                for form in billformset.forms:
                    if form.has_changed():
                        if form not in billformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            form_instance.is_advance=False
                            form_instance.project=userprofile.project
                            form_instance.reimb=current_reimb
                            form_instance.save()
                        else:
                            if BillDetail.objects.filter(id=form.instance.id):
                                form_instance=BillDetail.objects.get(id=form.instance.id)
                                form_instance.delete()
                                
                reimbform=ReimbForm(request.POST,instance=current_reimb)
                if reimbform.is_valid():
                    reimbform1=reimbform.save(commit=False)
                    reimbform1.applied_date=date.today()
                    reimbform1.project=userprofile.project
                    reimbform1.save()
                    if "send_request" in request.POST:
                        current_reimb.request_sent=True
                        current_reimb.save()
                        print current_reimb.id
                        form1_success=True
                        reimb1=Reimb.objects.filter(request_sent=False)
                        if not reimb1:
                            reimb2=Reimb(project=userprofile.project)
                            reimb2.save()
                        else:
                            for reimb3 in reimb1:
                                reimb2=reimb3
                        current_reimb=Reimb.objects.get(id=reimb2.id)
                    
                else:
                    reimbform_error=True
                 
                if "add_more" in request.POST:
                    BillFormset=modelformset_factory(BillDetail,fields=('shop_name','bill_number','amount','dated','date'),extra=2,can_delete=True) 
                qset=BillDetail.objects.filter(reimb=current_reimb)
                bill_ids=[]
                for bill123 in qset:
                    bill_ids.append(int(bill123.id))
             
                for bill_id in bill_ids:
                    if str(bill_id) in request.POST:
                        bill_id_final=bill_id
                        return HttpResponseRedirect('/reimb/bill/purchase_details/' + str(reimb_id) + '/' + str(bill_id_final))
            print current_reimb.id
            reimbform=ReimbForm(instance=current_reimb)
            billformset=BillFormset(queryset=qset)
            reimbset_not_received=Reimb.objects.filter(project=userprofile.project).filter(received=False).filter(request_sent=True)
            reimbset_received=Reimb.objects.filter(project=userprofile.project).filter(received=True).filter(request_sent=True)
            qset_display=BillDetail.objects.all()
            purchase_details=PurchaseDetail.objects.all()
        return render_to_response('finance/reimb_bill.html',locals(),context_instance=RequestContext(request))        
            
    else:
        raise Http404       
     
     
def bill_purchase_detail_reimb(request,reimb_id,bill_id):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if not userprofile.is_core:
            m=0
            reimb123=True
            PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'), can_delete=True)
            current_bill=BillDetail.objects.get(id=bill_id)
            qset_purchase=PurchaseDetail.objects.filter(bill=current_bill)
            if request.method=='POST':
                purchasedetailformset=PurchaseDetailFormset(request.POST,queryset=qset_purchase)
                for form in purchasedetailformset.forms:
                    if form.has_changed():
                        if form not in purchasedetailformset.deleted_forms:
                            form_instance=form.save(commit=False)
                            bill2=BillDetail.objects.get(id=bill_id)
                            form_instance.bill=bill2
                            form_instance.save()
                        else:
                            if PurchaseDetail.objects.filter(id=form.instance.id):
                                form_instance=PurchaseDetail.objects.get(id=form.instance.id)
                                form_instance.delete()
                if "add_more" in request.POST:
                    m=2 
                    PurchaseDetailFormset=modelformset_factory(PurchaseDetail,fields=('item_name','amount'),extra=m, can_delete=True)
            qset_purchase=PurchaseDetail.objects.filter(bill=current_bill)
            purchasedetailformset=PurchaseDetailFormset(queryset=qset_purchase)
            return render_to_response('finance/bill_purchase_detail_reimb.html',locals(),context_instance=RequestContext(request))
    else:
        return Http404
            
def bills(request):
    if request.user.is_authenticated():
        userprofile=UserProfile.objects.get(user=request.user)
        if userprofile.is_core:
            bills123=True
            ExcelFormset=modelformset_factory(BillDetail,fields=('core_submitted','excel',))
            qset=BillDetail.objects.all()
            for bill in qset:
                    bill.excel=False
                    bill.save()
            excelformset=ExcelFormset(queryset=qset)
            if request.method=='POST':
                excelformset=ExcelFormset(request.POST,queryset=qset)
                for form in excelformset.forms:
                    if form.has_changed():
                        form.save()
                if 'excel' in request.POST:
                    excel_create=BillDetail.objects.filter(excel=True)
                    workbook=xlwt.Workbook()
                    worksheet=workbook.add_sheet('excelsheet',cell_overwrite_ok=True)
                    worksheet.write(0,0,"Shop Name")
                    worksheet.write(0,1,"Bill Number")
                    worksheet.write(0,2,"Purchase Detail")
                    worksheet.write(0,3,"Amount")
                    i=1
                    j=0
                    for bill in excel_create:
                        worksheet.write(i,j,bill.shop_name)
                        j+=1
                        worksheet.write(i,j,bill.bill_number)
                        j+=1
                        worksheet.write(i,j,bill.purchase_detail)
                        j+=1
                        worksheet.write(i,j,bill.amount)
                        i+=1
                        j=0
                    return xls_to_response(workbook,'CFI_Bills.xls')
                qset=BillDetail.objects.all()
                for bill in qset:
                    bill.excel=False
                    bill.save()
            else:
                excelformset=ExcelFormset(queryset=qset)
            purchase_details=PurchaseDetail.objects.all()
            advance_bills_not_sub=BillDetail.objects.filter(core_submitted=False).filter(is_advance=True)
            reimb_bills_not_sub=BillDetail.objects.filter(core_submitted=False).filter(is_advance=False)
            advance_bills_sub=BillDetail.objects.filter(core_submitted=True).filter(is_advance=True)
            reimb_bills_sub=BillDetail.objects.filter(core_submitted=True).filter(is_advance=False)
            return render_to_response('finance/bills.html',locals(),context_instance=RequestContext(request))

        else:
            raise Http404()
    else:
        raise Http404
        
        
def xls_to_response(workbook,fname):
    response=HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition']='attachment; filename=%s' %fname
    workbook.save(response)
    return response
