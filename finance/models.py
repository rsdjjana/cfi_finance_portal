from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    name=models.CharField(max_length=40)
    year=models.IntegerField(max_length=4,blank=True)
    def __unicode__(self):
        return self.name
    
    
class UserProfile(models.Model):
    user=models.ForeignKey(User)
    name=models.CharField(max_length=30)
    phone_number=models.CharField(max_length=15,blank=True)
    hostel=models.CharField(max_length=20,blank=True)
    room_number=models.CharField(max_length=7,blank=True)
    is_core=models.BooleanField(default=False)
    project=models.ForeignKey(Project,blank=True,null=True)
    def __unicode__(self):
        return self.name
    
    
class Advance(models.Model):
    applied_date=models.DateTimeField(blank=True,null=True)
    approved_date=models.DateTimeField(blank=True,null=True)
    amount=models.FloatField(max_length=10)
    split_up=models.TextField(blank=True,null=True)
    approved=models.BooleanField(default=False,blank=True)
    disapproved=models.BooleanField(default=False,blank=True)
    received=models.BooleanField(default=False,blank=True)
    receive_date=models.DateTimeField(blank=True,null=True)
    due_date=models.DateTimeField(blank=True,null=True)
    project=models.ForeignKey(Project)
    core_comment=models.TextField(blank=True,null=True)
    bill_submitted=models.BooleanField(blank=True,default=False)
    read=models.BooleanField(blank=True,default=False) 
    
class Reimb(models.Model):
    applied_date=models.DateTimeField(blank=True,null=True)
    amount=models.FloatField(null=True)
    received=models.BooleanField(default=False,blank=True)
    received_date=models.DateTimeField(blank=True,null=True)
    project=models.ForeignKey(Project)
    submitted=models.BooleanField(default=False,blank=True)    
    request_sent=models.BooleanField(default=False,blank=True)

class BillDetail(models.Model):
    shop_name=models.CharField(max_length=40)
    bill_number=models.CharField(max_length=20)
    purchase_detail=models.TextField(blank=True)
    amount=models.FloatField(blank=True)
    is_advance=models.BooleanField(default=False)
    project=models.ForeignKey(Project,blank=True,null=True)
    dated=models.BooleanField(default=True)
    date=models.DateTimeField(blank=True,null=True)
    core_submitted=models.BooleanField(default=False)
    advance=models.ForeignKey(Advance,blank=True,null=True)
    reimb=models.ForeignKey(Reimb,blank=True,null=True)
    excel=models.BooleanField(blank=True,default=False)
    
class PurchaseDetail(models.Model):
    item_name=models.CharField(max_length=40,blank=True,null=True)
    amount=models.FloatField(blank=True,null=True)
    bill=models.ForeignKey(BillDetail)
    bill_id1=models.FloatField(blank=True,null=True)
