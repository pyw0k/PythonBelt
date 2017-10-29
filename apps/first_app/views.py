from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import User, Appointment
from django.core.exceptions import ObjectDoesNotExist
import time
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z ]+$')

def index(request):
	return render(request,'first_app/index.html')

def register(request):
	flagged = True
	if(len(request.POST['username'])< 2):
		messages.error(request,'Name must have at least 2 characters.')
		flagged= True
	if(not NAME_REGEX.match(request.POST['username'])):
		messages.error(request, 'Name can only consist of letters, please reenter your name')
		flagged= False
	if(not EMAIL_REGEX.match(request.POST['email'])):
		messages.error(request, "Please enter a valid email address")
		flagged = False
	if (len(request.POST['password']) < 8):
		messages.error(request, "Password must be at least 8 characters.")
		flagged = False
	if (request.POST['password'] != request.POST['password_confirm']):
		messages.error(request, "Passwords must match")
		raise ValidationError('Sorry, someone already has that [...]')
		flagged = False
	if(len(request.POST['dob'])< 1):
		messages.error(request, "Please enter your date of birth")
		flagged = False
	if not flagged:
		return redirect ('/')

	User.objects.create(name=request.POST['username'], password=request.POST['password'], email=request.POST['email'], date_of_birth=request.POST['dob'])
	request.session['current_user'] = User.objects.get(email=request.POST['email']).id
	return redirect('/display_appointments')

def login(request):
	try:
		users = User.objects.get(email=request.POST['email'], password=request.POST['password'])

	except ObjectDoesNotExist:
		messages.error(request,'Invalid username or password')
		return redirect('/')

	else:
		context = {}
		request.session['current_user'] = User.objects.get(email=request.POST['email'], password=request.POST['password']).id
		if "current_user" in request.session.keys():
			return redirect('/display_appointments')

def display_appointments(request):
	if 'current_user' in request.session.keys():
		context = {
			'user': User.objects.get(pk=request.session['current_user']),
			'today': datetime.datetime.now().date(),
			'appointments_today': Appointment.objects.filter(user_id=User.objects.get(pk=request.session['current_user'])).filter(date=datetime.datetime.now().date()).order_by('time'),
			'appointments_future' : Appointment.objects.filter(user_id=User.objects.get(pk=request.session['current_user'])).exclude(date=datetime.datetime.now().date()).order_by('date'),
			'appointments': Appointment.objects.all()
		}
		return render(request,'first_app/display_appointments.html', context)

def add_appointment(request):
	flagged = True

	if len(request.POST['date']) < 6:
		messages.error(request, "Please enter a valid date")
		flagged = True
	if datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d').date() < datetime.datetime.now().date():
		messages.error(request, "Date must be today or a future date")
		flagged=False
	if len(request.POST['time']) <4:
		messages.error(request,"Please enter a valid time")
	if len(request.POST['name']) < 1:
		messages.error(request, "please enter a task")
		flagged = False
	if not flagged:
		return redirect('/display_appointments')

	try:
		Appointment.objects.get(time=request.POST['time'], date=request.POST['date'])

	except ObjectDoesNotExist:
		pass
	else:
		messages.error(request, "You have an exisiting appointment at this time")
		return redirect('display_appointments')
	Appointment.objects.create(user_id=(User.objects.get(pk=request.session['current_user'])), name=request.POST['name'], status="Pending", date=request.POST['date'], time=request.POST['time']) 
	return redirect('/display_appointments')

def update_appointment(request,id):
	flagged = True
	if len(request.POST['date']) < 6:
		messages.error(request, 'Please enter a valid date')
		flagged = False
	if datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d').date() < datetime.datetime.now().date():
		messages.error(request, 'Date must be today or a future date')
		flagged = False
	if len(request.POST['time']) < 4:
		messages.error(request, 'Please enter a valid time')
	if len(request.POST['name']) < 1:
		messages.error(request, "Please enter a task")
		flagged = False
		return redirect('/')
	if not flagged:
		return redirect('/edit' + str(Appointment.objects.get(id=id).id))
	try:
		Appointment.objects.exclude(id=id).get(time=request.POST['time'], date=request.POST['date'])
	except ObjectDoesNotExist:
		pass
	else:
		messages.error('You have another appointment at this time, please select another time')
		return redirect('/edit/'+ str(Appointment.objects.get(id=id).id))
	appointment = Appointment.objects.get(id=id)
	appointment.name = request.POST['name']
	appointment.status = request.POST['status']
	appointment.date = request.POST['date']
	appointment.time = request.POST['time']
	appointment.save()
	return redirect('/display_appointments')

def edit(request,id):
	context = {
		'appointment': Appointment.objects.get(id=id),
		'date': str(Appointment.objects.get(id=id).date),
		'time': str(Appointment.objects.get(id=id).time),
	}
	return render(request, 'first_app/edit_appointments.html', context)

def delete(request, id):
	Appointment.objects.get(id=id).delete()
	return redirect('/display_appointments')

def logout(request):
	request.session.clear()
	messages.add_message(request, messages.INFO, 'Successfully logged out')
	return redirect('/')