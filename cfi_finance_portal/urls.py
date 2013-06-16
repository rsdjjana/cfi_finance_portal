from django.conf.urls import *
from django.conf.urls.defaults import *
from django.views.generic.simple import *
#from django.conf import settings
from cfi_finance_portal import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^portal/finance/$', 'finance.views.login', name='login'),
    url(r'^portal/finance/logout/$', 'finance.views.logout', name='logout'),
    url(r'^portal/finance/home/$','finance.views.home',name='home'),
    url(r'^portal/finance/home/project_detail/(?P<project_id>\d+)/$','finance.views.project_detail',name='project_detail'),
    url(r'^portal/finance/advance/$','finance.views.advance',name='advance'),
    url(r'^portal/finance/advance/bill/(?P<advance_id>\d+)/$','finance.views.advance_bill',name='advance_bill'),
    url(r'^portal/finance/advance/bill/view/(?P<advance_id>\d+)/$','finance.views.advance_bill_view',name='advance_bill_view'),
    url(r'^portal/finance/project/detail/advance/bill/view/(?P<advance_id>\d+)/$','finance.views.project_detail_advance_bill_view',name='project_detail_advance_bill_view'),
    url(r'^portal/finance/advance/approved/$','finance.views.advance_approved',name='advance_approved'),
    url(r'^portal/finance/reimb/$','finance.views.reimb',name='reimb'),
    url(r'^portal/finance/reimb/request/(?P<reimb_id>\d+)/$','finance.views.reimb_request',name='reimb_request'),
    url(r'^portal/finance/bills/$','finance.views.bills',name='bills'),
    url(r'^portal/finance/advance/bill/purchase_details/(?P<advance_id>\d+)/(?P<bill_id>\d+)/$','finance.views.bill_purchase_detail',name='bill_purchase_detail'),
    url(r'^portal/finance/reimb/bill/purchase_details/(?P<reimb_id>\d+)/(?P<bill_id>\d+)/$','finance.views.bill_purchase_detail_reimb',name='bill_purchase_detail_reimb'),
    # url(r'^cfi_finance_portal/', include('cfi_finance_portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^media/(?P<path>.*)$' , 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT }),
    
)
print settings.MEDIA_ROOT
