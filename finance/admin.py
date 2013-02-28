from django.contrib import admin
from finance.models import UserProfile, Project
from django.contrib.sites.models import Site

class ProjectAdmin(admin.ModelAdmin):
    list_display=['name']
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['name','is_core']

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.unregister(Site)
