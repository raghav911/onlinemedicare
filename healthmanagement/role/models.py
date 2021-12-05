from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField
# Create your models here.

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobileNumber=models.BigIntegerField()
    EC1=models.BigIntegerField(blank=True,null=True)
    EC2=models.BigIntegerField(blank=True,null=True)
    EC3=models.BigIntegerField(blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    gender=models.CharField(max_length=10)
    def __str__(self):
        return f"{self.name}"

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mobileNumber=models.BigIntegerField()
    workingAddress=models.CharField(max_length=200)
    fee=models.IntegerField(default=0)
    image=models.ImageField(blank=True,null=True,upload_to='upload/')
    specialization=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class appointmentP(models.Model):
    app_id=models.AutoField(primary_key=True)
    patient_id=models.IntegerField(default=0)
    doctor_id=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    bookedon=models.DateField(auto_now_add=True)
    date=models.DateField()
    time=models.TimeField()
    how=models.CharField(max_length=100) #in-person or video or chat

    def __str__(self):
        return f"{self.app_id}"
        
class Chat(models.Model):
    from_id=models.IntegerField(null=False,default=0)
    to_id=models.IntegerField(null=False,default=0)
    message=models.CharField(max_length=500)

class Prescription(models.Model):
    from_id=models.IntegerField(null=False,default=0)
    to_id=models.IntegerField(null=False,default=0)
    message=models.CharField(max_length=500)
    image=models.ImageField(blank=True,upload_to='upload/')
    

    def __str__(self):
        return f"{self.name}"
