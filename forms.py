from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField
import datetime


class ContactForm(Form):

	name = TextField("Name",[validators.Required("Please enter your name.")])
	# Gender = RadioField('Gender', choices=[('M','Male'),('F','Female')])
	message = TextAreaField("Message")
	email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	# Age = IntegerField("age")
	# language = SelectField('Languages', choices=[('cpp', 'C++'), ('py', 'Python')])
	submit = SubmitField("Submit")
	phone_number = TextField('Mobile',[validators.Required("Please Enter Your Mobile.")])

class TrainLiveStatus(Form):

	name = TextField("Train Name/Number",[validators.Required("Please enter Train name/Number.")])
	# doj = TextField("Running Date", [validators.Required("Please enter Train name/Number.")], default=datetime.datetime.now().strftime('%Y-%m-%d'))
	doj = TextField("Running Date", [validators.Required("Please enter Train name/Number.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))

	submit = SubmitField("Find")


class TrainRouteInformation(Form):

	name = TextField("Train Number",[validators.Required("Please enter Train name/Number.")])
	submit = SubmitField("Find")

class TrainDetails(Form):

	name = TextField("Train Name/Number",[validators.Required("Please enter Train name/Number.")])
	submit = SubmitField("Find")

class TrainCancelled(Form):

	# doj = TextField("Running Date", [validators.Required("Please enter Train name/Number.")], default=datetime.datetime.now().strftime('%Y-%m-%d'))
	doj = TextField("Running Date", [validators.Required("Please enter Running Date.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))

	submit = SubmitField("Find")

class TrainReschedule(Form):
	doj = TextField("Running Date", [validators.Required("Please enter Running Date.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))

	# doj = TextField("Running Date", [validators.Required("Please enter Train name/Number.")], default=datetime.datetime.now().strftime('%Y-%m-%d'))
	submit = SubmitField("Find")

class TrainPNR(Form):

	name = TextField("PNR",[validators.Required("Please enter PNR.")])
	submit = SubmitField("Find")
class StationName(Form):

	name = TextField("Station",[validators.Required("Please enter Station Name.")])
	submit = SubmitField("Find")
class StationCode(Form):

	name = TextField("Station",[validators.Required("Please enter Station Code.")])
	submit = SubmitField("Find")
class TrainBTStation(Form):

	s_code = TextField("Source",[validators.Required("Please enter Source Station Code.")])
	d_code = TextField("Destination",[validators.Required("Please enter Destination Station Code.")])
	# doj = TextField("Running Date", [validators.Required("Please enter Train name/Number.")], default=datetime.datetime.now().strftime('%Y-%m-%d'))
	doj = TextField("Running Date", [validators.Required("Please enter Running Date.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))

	submit = SubmitField("Find")

class TrainSuggest(Form):

	name = TextField("Train Name/Number",[validators.Required("Please enter Train name/Number.")])
	submit = SubmitField("Find")
class StationSuggest(Form):

	name = TextField("Station Name/Code",[validators.Required("Please enter Station Name/Code.")])
	submit = SubmitField("Find")

class TrainSeatAvailibity(Form):

	name = TextField("Train Number",[validators.Required("Please enter Train Number.")])
	source = TextField("Source",[validators.Required("Source should not be empty.")])

	destination = TextField("Destination",[validators.Required("Destination should not be empty.")])
	doj = TextField("Running Date", [validators.Required("Please enter Running Date.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))
	class_code = SelectField('Classes', choices=[('1A', '1A-First class Air-Conditioned (AC)'), 
								('2A', '2A-AC 2-tier sleeper'),('FC','FC-First Class'),
								('3A','3A-AC 3 Tier'),('3 E','3 E - AC 3 Tier Economy'),('CC','Chair Car'),
								('SL','SL-Sleeper Class '),('2S','2S-Second Sitting')])
	quota_code = SelectField('Quota', choices=[('GN', 'General Quota'), 
								('LD', 'Ladies Quota'),('HO','Head quarters/high official Quota'),
								('DF','Defence Quota'),('PH','Parliament house Quota'),('FT','Foreign Tourist Quota'),
								('DP','Duty Pass Quota'),('TQ','Tatkal Quota'),
								('PT','Premium Tatkal Quota'),('SS','Female(above 45 Year)/Senior Citizen/Travelling alone')
								,('HP','Physically Handicapped Quota'),('RE','Railway Employee Staff on Duty for the train'),
								('GNRS','General Quota Road Side'),('OS','Out Station'),
								('PQ','Pooled Quota'),('RC(RAC)','Reservation Against Cancellation'),('RS','Road Side'),
								('YU','Yuva'),('LB','Lower Berth')])

	submit = SubmitField("Find")

class TrainFairEnquiry(Form):

	name = TextField("Train Number",[validators.Required("Please enter Train Number.")])	
	source_station = TextField("Source",[validators.Required("Please enter From station.")])
	dest_station = TextField("Destination",[validators.Required("Please enter To station.")])
	age = IntegerField("Age",[validators.Required("Please enter To Age .")])
	quota_code = SelectField('Quota', choices=[('GN', 'General Quota'), 
								('LD', 'Ladies Quota'),('HO','Head quarters/high official Quota'),
								('DF','Defence Quota'),('PH','Parliament house Quota'),('FT','Foreign Tourist Quota'),
								('DP','Duty Pass Quota'),('TQ','Tatkal Quota'),
								('PT','Premium Tatkal Quota'),('SS','Female(above 45 Year)/Senior Citizen/Travelling alone')
								,('HP','Physically Handicapped Quota'),('RE','Railway Employee Staff on Duty for the train'),
								('GNRS','General Quota Road Side'),('OS','Out Station'),
								('PQ','Pooled Quota'),('RC(RAC)','Reservation Against Cancellation'),('RS','Road Side'),
								('YU','Yuva'),('LB','Lower Berth')])
	doj = TextField("Running Date", [validators.Required("Please enter Running Date.")], default=datetime.datetime.now().strftime('%d-%m-%Y'))
	submit = SubmitField("Find")

class Blog_Comment(Form):

	comment = TextAreaField("Comment",[validators.Required("Please enter views .")])
	submit = SubmitField("Post Comment")
