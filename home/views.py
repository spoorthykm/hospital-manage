from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
#from .forms import Token,StudentSearchForm

# Create your views here.
from home.models import patient,token,report,bill,doctor,receptionist,ambulance
from home.forms import Token,SearchForm,patientcreateform,billform,UserRegisterForm,reportform
from django.contrib import messages


def home_view(request):
    temp='/login-doctor/'
    tempP='/login-patient/'
    tempR='/login-r/'
    tempE='/Emergency/'
    tempPS='/Create/'
    p=patient.objects.all()[:]
    r=receptionist.objects.all()[:]
    d=doctor.objects.all()[:]
    return render(request,'mainhome.html',{'temp':temp,'tempP':tempP,'tempR':tempR,'tempE':tempE,'tempPS':tempPS,'p':p,'r':r,'d':d})



def printt(request):
    form=token.objects.all()[:]
    return render(request, 'print.html', {'form': form})

def createpatient(request):
    if request.method=='POST':
        form=patientcreateform(request.POST)
        if form.is_valid():
            pat=patient.objects.create(patient_name=form.cleaned_data.get('patient_name'),
            Sex=form.cleaned_data.get('Sex'),Dob=form.cleaned_data.get('Dob'),
            Age=form.cleaned_data.get('Age'),Address=form.cleaned_data.get('Address'),
            Email=form.cleaned_data.get('Email'),Blood_group=form.cleaned_data.get('Blood_group'),
            Password=form.cleaned_data.get('Password'))
            pat.save()
            name=request.session['patient_name']=pat.patient_name
            messages.success(request,"create sucessfully!!")    
            temp='/tokenT/'+name
            return redirect(temp)
        else:    
            return render(request,'create.html',{'form':form,'value':'create'})
    else:
        form=patientcreateform()
        return render(request,'create.html',{'form':form,'value':'Create'})

def patientlogin(request):
    if request.method=='POST':
        username=request.POST.get('patient_name')
        password=request.POST.get('Password')
        try:
            user=patient.objects.get(patient_name=username)
            if user:
                if user.Password==password:
                    name=user.patient_name
                    temp='/PatientPage/'+name
                    return redirect(temp)
                else:
                    return HttpResponse('incorrect password')
        except patient.DoesNotExist:
            user=None
            print('Someone tried to login and failed')
            print('they used username:{} password:{}'.format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        #return redirect('/')
        return render(request,'action.html',{})

    
def InPatient(request,name):
    form=token.objects.filter(name__contains=name)
    bo=report.objects.filter(patient__patient_name=name)
    bi=bill.objects.filter(patient__patient_name=name)
    temp='/patient/'+name
    value=0
    return render(request, 'print.html', {'form': form,'bo':bo,'bi':bi,'temp':temp,'value':value})


def createbill(request):
    if request.method=='POST':
        form=billform(request.POST)
        if form.is_valid():
            bil=bill.objects.create(patient=form.cleaned_data.get('patient'),
            room=form.cleaned_data.get('room'),report=form.cleaned_data.get('report'),
            fee=form.cleaned_data.get('fee'),operation=form.cleaned_data.get('operation'),ndays=form.cleaned_data.get('ndays'))
            bil.tot=(bil.room*bil.ndays)+bil.report+bil.fee+bil.operation
            bil.save()           
            messages.success(request,"create sucessfully!!")    
            return redirect('/')
        else:
            return render(request,'create.html',{'form':form,'value':'create'})
    else:
        form=billform()
        return render(request,'create.html',{'form':form,'value':'Create'})

def patientpage(request,name):
    form=patient.objects.get(patient_name__contains=name)
    temp='/tokenT/'+name
    temph='/patient/'+name
    return render(request, 'Ppage.html', {'form':form,'temp':temp,'temph':temph})

def receptionistlogin(request):
    if request.method=='POST':
        username=request.POST.get('doctor')
        Pass=request.POST.get('pas')
        try:
            user=receptionist.objects.get(recp_name=username)
            if user:
                if user.pa==Pass:
                    request.session['Name']=username
                    temp='/receptionist/'+username
                    return redirect(temp)
                else:
                    return HttpResponse('incorrect password')
        except receptionist.DoesNotExist:
            #user=None
            print('Someone tried to login and failed')
            print('they used username:{} password:{}'.format(username,Pass))
            return HttpResponse("Invalid login details given")
    else:
        return render(request,'receplogin.html',{})

def ReceptionistPage(request,name):
    value=1
    form=receptionist.objects.get(recp_name__contains=name)
    if request.session['id']:
        result=ambulance.objects.filter(id__contains=request.session['id'])
        request.session['id']=None
        value=0
        return render(request,'Rpage.html',{'result':result,'value':value})
    else:
        return render(request,'Rpage.html',{'form':form,'value':value})

def AReport(request):
    form=report.objects.all()[:]
    value=1
    return render(request,'print.html',{'bo':form,'value':value})

def ABill(request):
    form=bill.objects.all()[:]
    value=1
    return render(request,'print.html',{'bi':form,'value':value})

def AToken(request):
    form=token.objects.all()[:]
    value=1
    return render(request,'print.html',{'form':form,'value':value})

def TokenT(request,name):
    uname=patient.objects.get(patient_name=name)
    if request.method == 'POST':
        form=Token(request.POST)
        if form.is_valid():
            #temp = form.cleaned_data.get('Doctor')
            p=token.objects.create(Date=form.cleaned_data.get
            ('Date'),Doctor=form.cleaned_data.get('Doctor'))
            p.name=uname.patient_name
            countt=0
            result=token.objects.filter(Doctor__doctor_name=p.Doctor).filter(Date__contains=p.Date)
            for i in result:
                countt=countt+1
            p.identity=countt
            print(p.identity)
            p.save()
            messages.success(request,'Create Successfully!')
            return render(request,'Rtoken.html',{'form':result,'count':countt})
    else:
        form=Token()
    return render(request, 'Ftoken.html', {'form': form})

def search(request):
    #del request.session['id']
    #if request.session['id']==1:
    if request.method=='POST':
        search=SearchForm(request.POST)
        print(search)
        if search.is_valid():
            name=search.cleaned_data.get('q')
            form=(token.objects.filter(name__contains=name))|(token.objects.filter(Doctor__doctor_name=name))
            bo=report.objects.filter(patient__patient_name=name)
            bi=bill.objects.filter(patient__patient_name=name)
            temp='/patient/'+name
            value=1
            return render(request, 'print.html', {'form': form,'bo':bo,'bi':bi,'temp':temp,'value':value})
    else:
        form=SearchForm()
        result=token.objects.all()
        return render(request,'home.html',{'form':form})

def register(request):
    registered=False
    user_form=UserRegisterForm(request.POST)
    if request.method=='POST':
        if user_form.is_valid():
            amb=ambulance.objects.create(Name=user_form.cleaned_data.get('Name'),
            Address=user_form.cleaned_data.get('Address'),Contact=user_form.cleaned_data.get('Contact'))
            amb.save()
            request.session['id']=amb.id
            return redirect('/')

        else:
            print(user_form.errors)
    else:
        user_form=UserRegisterForm()
    return render(request,'ambulances.html',{'form':user_form,'registered':registered,'value':'Signup'})


# def receptionistaccount(request):
#     if request.session['Name']:
#         result=ambulance.objects.filter(Name__contains=request.session['Name'])
#         request.session['Name']=None
#         return render(request,'Rpage.html',{'result':result})
#     else:
#         return redirect('/createbill/')

def doctorlogin(request):
    if request.method=='POST':
        username=request.POST.get('doctor')
        password=request.POST.get('pas')
        try:
            user=doctor.objects.get(doctor_name=username)
            if user:
                if user.pa==password:
                    temp='/doctorpage/'+user.doctor_name
                    return redirect(temp)
                else:
                    return HttpResponse('incorrect password')
        except doctor.DoesNotExist:
            user=None
            print('Someone tried to login and failed')
            print('they used username:{} password:{}'.format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request,'doctorlogin.html',{})

def doctorpage(request,name):
    form=doctor.objects.get(doctor_name=name)
    temp='/DToken/'+name
    return render(request, 'Dpage.html', {'form':form,'temp':temp})

def DoctorToken(request,name):
    form=token.objects.filter(Doctor__doctor_name=name)
    value=1
    return render(request, 'print.html', {'form': form,'value':value})

def createreport(request):
    if request.method=='POST':
        form=reportform(request.POST)
        if form.is_valid():
            bil=report.objects.create(patient=form.cleaned_data.get('patient'),
            Hemoglobin=form.cleaned_data.get('Hemoglobin'),Neutrophils=form.cleaned_data.get('Neutrophils'),
            lymphocytes=form.cleaned_data.get('lymphocytes'),monocytes=form.cleaned_data.get('monocytes'),
            basophils=form.cleaned_data.get('basophils'),eosinophils=form.cleaned_data.get('eosinophils'),
            rbc=form.cleaned_data.get('rbc'),platelets=form.cleaned_data.get('platelets'))
            bil.save()
            messages.success(request,"create sucessfully!!")    
            return redirect('/')
        else:
            return render(request,'create.html',{'form':form,'value':'create'})
    else:
        form=reportform()
        return render(request,'create.html',{'form':form,'value':'Create'})

def reportgen(request):
    nam=request.session['patient_name']
    pat=patient.objects.get(patient_name=nam)
    bil=report.objects.get(patient=pat)
    if request.method=='POST':
        modelform=billform(request.POST,instance=pat)
        if modelform.is_valid():
            print(pat)
            #form=modelform.save()
            return render(request,'report.html',{'fo':pat,'bo':bill})
    else:
        modelform=billform(instance=pat)
        return render(request,'report.html',{'fo':pat,'bo':bil})   
    

    