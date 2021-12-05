from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor , appointmentP , Chat , Prescription
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.files.storage import FileSystemStorage
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from .svm import do_something
import os
from datetime import date
import jwt
import requests
import json
from time import time

def home(request):
    if request.method == 'POST':
        if request.POST.get("sp"):
            return redirect(registerP)
        if request.POST.get("sd"):
            return redirect(registerD)
    return render(request, 'role/landing.html')

def dashboardD(request):
    username = request.user.username
    doctor_id = request.user.id
    dt=Doctor.objects.all() # Collect all records from table 
    apt=appointmentP.objects.all() # Collect all records from table 
    pt=Patient.objects.all() # Collect all records from table 
    chat=Chat.objects.all() # Collect all records from table 
    
    total_patients=0
    for apts in apt :
        if apts.doctor_id == doctor_id :
            total_patients = total_patients + 1
                            
    return render(request, 'role/dashboardD.html', {'username':username , 'doctor_id':doctor_id , 'total_patients':total_patients ,  'dt':dt , 'pt':pt , 'apt':apt , 'chat':chat } )


def dashboardP(request):
    username = request.user.username
    patient_id = request.user.id
    dt=Doctor.objects.all() # Collect all records from table 
    apt=appointmentP.objects.all() # Collect all records from table 
    pt=Patient.objects.all() # Collect all records from table 
    return render(request, 'role/dashboardP.html', {'username':username , 'patient_id':patient_id ,  'dt':dt , 'pt':pt , 'apt':apt} )

def editProfileD(request , doctor_id):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("editProfileD"):
            print("edit profile doctor_id:" + str(doctor_id))            
            dt=Doctor.objects.all() # Collect all records from table
            for dts in dt :
                if dts.user_id == doctor_id :
                    uname = request.POST['username']
                    mno = request.POST['mobilenumber']
                    email = request.POST['email']
                    password = request.POST['pw1']
                    wa = request.POST['wa']
                    spc = request.POST['spc']
                    fee = request.POST['fee']
                    
                    dts.name = uname
                    dts.email = email
                    dts.mobileNumber = mno
                    dts.password = password
                    dts.workingAddress = wa
                    dts.specialization = spc
                    dts.fee = fee
                    dts.save()
                    break
            
            return redirect('dashboardD')
    username = request.user.username
    doctor_id = request.user.id
    dt=Doctor.objects.all() # Collect all records from table 
    return render(request, 'role/editProfileD.html', {'username':username , 'doctor_id':doctor_id , 'dt':dt } )

def editProfileP(request , patient_id):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("editProfileP"):
            print("edit profile patient_id:" + str(patient_id))            
            pt=Patient.objects.all() # Collect all records from table
            for pts in pt :
                if pts.user_id == patient_id :
                    uname = request.POST['username']
                    mno = request.POST['mobilenumber']
                    email = request.POST['email']
                    password = request.POST['pw1']
                    pts.name = uname
                    pts.email = email
                    pts.mobileNumber = mno
                    pts.password = password
                    pts.save()
                    break
            
            return redirect('dashboardP')
    username = request.user.username
    patient_id = request.user.id
    pt=Patient.objects.all() # Collect all records from table 
    return render(request, 'role/editProfileP.html', {'username':username , 'patient_id':patient_id , 'pt':pt } )

def registerP(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("signupP"):
            print("hello")
            print(request.POST)
            uname = request.POST['username']
            mno = request.POST['mobilenumber']
            name = request.POST['name']
            gender = request.POST['gender']
            email = request.POST['email']
            password = request.POST['pw1']
            us = User.objects.create_user(uname, email, password)
            std = Patient.objects.create(
                user=us, name=name, gender=gender ,  email=email, mobileNumber=mno)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return render(request,'role/loginP.html')
        if request.POST.get("loginP"):
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboardP')
            else:
                messages.success(request, f'Wrong Credentials')
    return render(request, 'role/loginP.html')


def registerD(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get("signupD"):
            print("hello")
            print(request.POST)
            uname = request.POST['username']
            mno = request.POST['mobilenumber']
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['pw1']
            workingaddres=request.POST['wa']
            spc=request.POST['spc']
            fees=request.POST['fee']
           
            us = User.objects.create_user(uname, email, password)
            std = Doctor.objects.create(
                user=us, name=name, email=email, mobileNumber=mno,workingAddress=workingaddres , fee=fees, specialization=spc)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return render(request,'role/loginD.html')
        if request.POST.get("loginD"):
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboardD')
            else:
                messages.success(request, f'Wrong Credentials')
    return render(request, 'role/loginD.html')
    
def logout(request):
    return render(request, 'role/logout.html')

def doctors(request):
    dt=Doctor.objects.all() # Collect all records from table 
    return render(request,'role/doctors.html',{'dt':dt})

def patients(request):
    pt=Patient.objects.all() # Collect all records from table 
    return render(request,'role/patients.html',{'pt':pt})

def suicide_test(request , patient_id):
    print("suicide_test:" + str(patient_id))
    if request.POST.get("suicide_test"):
        answer1 = request.POST['answer1']
        answer2 = request.POST['answer2']
        answer3 = request.POST['answer3']
        response = do_something(patient_id , answer1 , answer2 , answer3)
        print("response:", response)
        messages.success(request, response)
    
        return render(request,'role/suicide_test.html' , {'patient_id':patient_id , 'response':response})
    
    return render(request,'role/suicide_test.html' , {'patient_id':patient_id , 'response':''})

    
def get_appointment(request , doctor_id):
    print("get_appointment:" + str(doctor_id))
    print(request.POST)
    if request.POST.get("book_appointment"):
        print("book_appointment:" + str(doctor_id))
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        amount = request.POST['amount']
        doc_id = request.POST['doctor_id']
        how = request.POST['how']
        print(appointment_date)
        print(appointment_time)   
        print(amount)   
        print(doc_id)   
        print(how) 
        apt = appointmentP.objects.create(date=appointment_date, time=appointment_time, how=how, doctor_id=doc_id, patient_id=request.user.id , amount=amount)            
        dt=Doctor.objects.all() # Collect all records from table 
        today = date.today()        
        return render(request,'role/book_appointment.html' , {'doctor_id':doctor_id , 'dt':dt , 'today':today})
    else:    
        dt=Doctor.objects.all() # Collect all records from table 
        today = date.today()
        return render(request,'role/book_appointment.html' , {'doctor_id':doctor_id , 'dt':dt , 'today':today})
    
def charts(request):
    return render(request,'role/charts.html')   
    
def breadcrumb_pagination(request):
    return render(request,'role/breadcrumb_pagination.html')   

def prescription(request , patient_id):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        file_name = os.path.basename(file_url)
        pt=Patient.objects.all() # Collect all records from table
        doctor_id=request.user.id
        
        prescription = Prescription.objects.create(from_id=doctor_id, to_id=patient_id , image=file_name)
    return render(request, 'role/prescription.html' , {'patient_id':patient_id })

    
def uploadD(request , doctor_id):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        file_name = os.path.basename(file_url)
        dt=Doctor.objects.all() # Collect all records from table
        count =0        
        updated_row=0
        for dts in dt :
            count = count + 1
            if dts.user_id == doctor_id :
                updated_row = count
                dts.image = file_name
                dts.save()

        return redirect('dashboardD')
    return render(request, 'role/uploadD.html')
    
def uploadP(request , patient_id):
    print("upload patient_id:" + str(patient_id))
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        print(upload.name)
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        print(file_url)
        
        file_name = os.path.basename(file_url)
        pt=Patient.objects.all() # Collect all records from table
        count =0        
        updated_row=0
        for pts in pt :
            count = count + 1
            if pts.user_id == patient_id :
                updated_row = count
                pts.image = file_name
                pts.save()

        return redirect('dashboardP')
    return render(request, 'role/uploadP.html')
    
def chatP(request , from_id , to_id , pd):  #pd=1 patient , pd=2 doctor
    if request.method == 'POST':
        message = request.POST['message']
        print(message)
        chat = Chat.objects.create(from_id=from_id, to_id=to_id , message=message)
    
    
    dt=Doctor.objects.all() # Collect all records from table   
    pt=Patient.objects.all() # Collect all records from table   
    chat=Chat.objects.all() # Collect all records from table 
    return render(request,'role/chatP.html' , {'from_id':from_id , 'to_id':to_id  , 'dt':dt , 'pt':pt , 'chat':chat , 'pd':pd})   

def prescriptionP(request):  
    dt=Doctor.objects.all() # Collect all records from table   
    pt=Patient.objects.all() # Collect all records from table   
    prescription=Prescription.objects.all() # Collect all records from table 
    patient_id=request.user.id
    print("patient_id:", patient_id)
    return render(request,'role/prescriptionP.html' , {'patient_id':patient_id , 'dt':dt , 'pt':pt , 'prescription':prescription})   


def chatD(request , from_id , to_id , pd):  #pd=1 patient , pd=2 doctor
    if request.method == 'POST':
        message = request.POST['message']
        print(message)
        chat = Chat.objects.create(from_id=from_id, to_id=to_id , message=message)
    
    
    dt=Doctor.objects.all() # Collect all records from table   
    pt=Patient.objects.all() # Collect all records from table   
    chat=Chat.objects.all() # Collect all records from table 
    return render(request,'role/chatD.html' , {'from_id':from_id , 'to_id':to_id  , 'dt':dt , 'pt':pt , 'chat':chat , 'pd':pd})   

def videoP(request , from_id , to_id , pd):  #pd=1 patient , pd=2 doctor
    if request.method == 'POST':
        message = request.POST['message']
        print(message)
    
    
    payload = {'exp': time() + 5000,
           'iss': 'KT7_jK0MRXui0D3KpcL8EA'    
          }     
    token = jwt.encode(payload, 'rLOMNSVkcABthVss1qnelEUAuXBJsFyRHR3J' , algorithm='HS256')

    #conn = http.client.HTTPSConnection("api.zoom.us")
    headers = {
            'authorization': "Bearer " + token,
            'content-type': "application/json"
              }
    
    # create json data for post requests
    meetingdetails = {"topic": "Online Medicare zoom meeting",
                  "type": 2,
                  "start_time": "2021-12-01T16: 30: 00",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
  
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
  
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings', 
      headers=headers, data=json.dumps(meetingdetails))
  
    print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
  
    print(
        f'\n here is your zoom meeting link {join_URL} and your \
        password: "{meetingPassword}"\n')
  
    subject = 'Zoom Meeting Request Online Medicare'
    message = f'\n here is your zoom meeting link {join_URL} and your \
        password: "{meetingPassword}"\n'
    from_email = 'celab2010@gmail.com'
    to_email = ''
    
    pt=Patient.objects.all() # Collect all records from table   
    for pts in pt :
        if pts.user_id == from_id :
            to_email = [pts.email]

    if subject and message and from_email and to_email:
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    
    to_email = ''
    dt=Doctor.objects.all() # Collect all records from table   
    for dts in dt :
        if dts.user_id == to_id :
            to_email = [dts.email , ]
    
    if subject and message and from_email and to_email:
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    
                
    return render(request,'role/videoP.html' , {'from_id':from_id , 'to_id':to_id  , 'dt':dt , 'pt':pt , 'join_URL':join_URL , 'meetingPassword':meetingPassword })   
