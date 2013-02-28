from django.conf.urls import *
from django.conf.urls.defaults import *
from django.views.generic.simple import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'finance.views.login', name='login'),
    url(r'^logout/$', 'finance.views.logout', name='logout'),
    url(r'^home/$','finance.views.home',name='home'),
    url(r'^advance/$','finance.views.advance',name='advance'),
    url(r'^advance/bill/(?P<advance_id>\d+)/$','finance.views.advance_bill',name='advance_bill'),
    url(r'^advance/approved/$','finance.views.advance_approved',name='advance_approved'),
    url(r'^reimb/$','finance.views.reimb',name='reimb'),
    url(r'^bills/$','finance.views.bills',name='bills'),
    # url(r'^cfi_finance_portal/', include('cfi_finance_portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
