from flask import Flask, render_template, request, flash,redirect, url_for,send_file
from forms import ContactForm,TrainLiveStatus,TrainRouteInformation, TrainDetails, TrainCancelled,TrainPNR,TrainReschedule,StationName,StationCode,TrainBTStation,StationSuggest,TrainSuggest,TrainSeatAvailibity,TrainFairEnquiry,Blog_Comment
from irctc import RAIL_API
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wh
from send_email import SendEmail

import json
import datetime
import urllib2
import json

from base64 import b64encode
import operator
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from io import BytesIO
import base64


app = Flask(__name__, template_folder='templates')
app.secret_key = 'hey1234##'

# result = RAIL_API("http://api.railwayapi.com/v2/",'mia22f6h')
# result = RAIL_API("http://api.railwayapi.com/",'mia22f6h')
#new api key Kiran
result = RAIL_API("http://api.railwayapi.com/v2/",'bxkpbko307')

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:honey@localhost/irctc'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://b29e7c6015fc57:49812c5e@us-cdbr-iron-east-03.cleardb.net/heroku_6341d6eb54cb201'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE']='whoosh'

db = SQLAlchemy(app)

#news api credential
news_api_url = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=5f00de8ea9924424951ecc01d2df0939"
# news_api_url = "https://newsapi.org/v1/articles?source=google-news&sortBy=top&apiKey=5f00de8ea9924424951ecc01d2df0939"

class Blog(db.Model):
	__searchable__=['title','content']
	
	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	content = db.Column(db.String(1000))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	image_name = db.Column(db.String(3000))
	image_data = db.Column(db.LargeBinary)
     
wh.whoosh_index(app,Blog)

class Contact(db.Model):
	
	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	email = db.Column(db.String(50))
	phone_number = db.Column(db.String(10))
	message = db.Column(db.String(1000))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class News(db.Model):

	id = db.Column('id', db.Integer, db.Sequence('news_id_seq',start=1), primary_key=True,)
	source = db.Column(db.String(500))
	description = db.Column(db.Text(50000))
	title = db.Column(db.String(500), unique=True)
	news_url = db.Column(db.String(10000))
	publish_date = db.Column(db.DateTime)
	image_url = db.Column(db.String(10000))
	create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Comment(db.Model):

	id = db.Column('id', db.Integer, db.Sequence('comment_id_seq',start=1), primary_key=True,)
	comment = db.Column(db.Text)
	create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@app.route("/view_contact_summary")
def display_contact_summary():
	# engine = create_engine('mysql+mysqldb://root:honey@localhost/irctc')
	engine = create_engine('mysql+mysqldb://b29e7c6015fc57:49812c5e@us-cdbr-iron-east-03.cleardb.net/heroku_6341d6eb54cb201')

	# print engine
	cnx = engine.connect()
	x = cnx.execute("select name,count(id) from contact group by name")
	cnx.close()

	l1=[]
	l2=[]
	l3=[]
	for each in x:
	#     print each
	#     if each[1] not in l1:
	        l1.append(len(each[0]))
	        l3.append(each[0])
	#     if each[3] not in l2:
	        l2.append(int(each[1]))
	print l1,l2,l3


	# plt.plot(l1, l2,'o-')
	# plt.title('Example')
	# plt.xlabel('hey')
	# plt.ylabel('jey')
	# plt.show()
	explode=[]
	if len(l3):
		for each in range(0,len(l3)):
			if each==1:
				explode.append(0.1)
			else:
				explode.append(0)
	# explode = (0, 0.1, 0, 0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
	fig1, ax1 = plt.subplots()
	ax1.pie(l2, explode=tuple(explode), labels=l3, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	# DPI = fig1.get_dpi()
	# print "DPI:", DPI
	# DefaultSize = fig1.get_size_inches()
	# print "Default size in Inches", DefaultSize
	# fig1.set_size_inches( (DefaultSize[0]*5, DefaultSize[1]*5) )
	# Size = fig1.get_size_inches()
	# print "Size in Inches", Size
	fig1.savefig("contact_summ.png")
	figfile = BytesIO()
	fig1.savefig(figfile, format='png')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	result = figdata_png


	return render_template("fig_contact_smmary.html", result=result)

@app.route("/dashboard")
def show_dashboard():
	
	

	return render_template("dashboard.html")

@app.route("/post_comment",methods=['GET', 'POST'])
def post_comments():
	print "calling post comment"
	form = Blog_Comment()
	if request.method=='POST':
		if request.form['comment']:
			post =Comment(comment=request.form['comment'])
			db.session.add(post)
			db.session.commit()
			return redirect(url_for('response_blog'))
		else:
			flash("Please enter some text to post message")
			return redirect(url_for('response_blog'))
	return render_template("easy_blog.html",form=form)


@app.route("/")
def index():
	form ={}
	data ={}
	# data_to_show=[]
	# # print "datetime.datetime.utcnow",datetime.datetime.utcnow,(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
	# current_news = News.query.filter(News.create_date <= (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")).all()
	# # print "current_news====",current_news
	# if current_news:
	# 	for each in current_news:
	# 		data_to_show.append({'description':each.description,'title':each.title,
	# 				'url':each.news_url,'publishedAt':each.publish_date,'urlToImage':each.image_url})
	# 	form={'articles':data_to_show}
	# else:
	try:
		data = result.get_request_from_news(news_api_url)
	except Exception as e:
		pass
	# print "dataaaaaa",data
	if 'status' in data and data.get('status')=='ok':
		form =data

		# creating all news into the databases
		# news_to_add = False
		# if 'articles' in form and form.get('articles'):
		# 	# if data_to_show:
		# 	# 	data.get('articles',[])+data_to_show
		# 	# print "form.get('articles')=====",data.get('articles'),type(data.get('articles'))
		# 	for each in form.get('articles'):
		# 		print "each=====",each
		# 		existing_news = News.query.filter(News.create_date <= datetime.datetime.now()).filter_by(title=each.get('title')).all()
		# 		print "Existing news=======",existing_news
		# 		if not existing_news:
		# 			news_to_add = News(source=data.get('source'),description=each.get('description'), 
		# 						title=each.get('title'),news_url=each.get('url'),image_url = each.get('urlToImage'),
		# 						publish_date = str(each.get('publishedAt')).replace('T',' ').replace('Z', ' '))
		# 			db.session.add(news_to_add)
		# 			db.session.commit()
		# 		else:
		# 			pass
	# else:
	# 	form={'articles':data_to_show}

	return render_template("index.html",rows=form)


@app.route("/disclaimer")
def get_disclaimer():
	return render_template("disclamier.html")


@app.route("/home_page")
def home_page():
   return render_template("index.html")

@app.route("/mobile_app")
def mobile_app():
   return render_template("mobile_app.html")

@app.route("/response_blog")
def response_blog():
	new_data = []
	posts = Blog.query.all()
	# posts = Blog.query.filter_by(id=7).first()
	# print 'response==========',posts
	new_data = [(each.title,each.created_date,each.content,b64encode(each.image_data)if each.image_data else '') for each in posts]
	# print "new_data====",new_data

	#sort by date
	new_data.sort(key=operator.itemgetter(1),reverse=True)
	
	# if posts.image_data:
	# image = b64encode(posts.image_data)
	comment_data =Comment.query.all()

	new_c_data = [(each.comment,each.create_date) for each in comment_data]
	# print "new_data====",new_data

	#sort by date
	new_c_data.sort(key=operator.itemgetter(1),reverse=True)
	return render_template("response_blog.html",posts=new_data,form=Blog_Comment(),comments=new_c_data)

@app.route("/response_contact")
def response_contact():
	return render_template("response_contact.html")

#for whoosh search
@app.route("/search")
def search():
	posts = Blog.query.whoosh_search(request.args.get('query')).all()

	return render_template("response_blog.html",posts=posts)

@app.route("/add",methods=['GET', 'POST'])
def add_easy_blog():
	if request.method=='POST':
		file = request.files['inputfile']
		post =Blog(title=request.form['title'],content=request.form['content'], image_name=file.filename, image_data=file.read())
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('response_blog'))
	return render_template("easy_blog.html")
	# return redirect(url_for('response_blog'))


@app.route('/contact_form',methods=['GET', 'POST'])
def contact():
   form = ContactForm()
   if request.method == 'POST':
	if form.validate() == False:
	   flash('All fields are required.')
	   return render_template('contact_form.html', form=form)
	else:
		post =Contact(name=request.form['name'],email=request.form['email'],phone_number=request.form['phone_number'],message=request.form['message'])
		db.session.add(post)
		db.session.commit()
		name =request.form['name']
		sender_email = request.form['email']
		to_email = 'raileasyinfo@gmail.com'
		message = request.form['message']
		phone = request.form['phone_number']
		SendEmail().send_email_from_website(name,sender_email, to_email, message,phone)

	   # return render_template('success.html')
	   	return redirect(url_for('response_contact'))
   elif request.method == 'GET':
       return render_template('contact_form.html', form=form)

@app.route('/train_live_status',methods=['GET', 'POST'])
def train_live_status():
   form = TrainLiveStatus()
   if request.method == 'POST':
	if form.validate() == False:
	   flash('All fields are required.')
	   return render_template('train_live_status.html', form=form)
	else:
	   doj = request.form['doj']
	   train_name_number = request.form['name']
	   response={}
	   response = result.get_train_live_status(train_name_number,doj)#doj.replace("-",""))
	   return render_template('success.html',rows =[response])
   elif request.method == 'GET':
       return render_template('train_live_status.html', form=form)

@app.route('/train_route_information',methods=['GET', 'POST'])
def train_route_information():
    form = TrainRouteInformation()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_route_information.html', form=form)
		else:
		   train_name_number = request.form['name']
		   response={}
		   response = result.get_train_route_information(train_name_number)
		   return render_template('response_train_route.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_route_information.html', form=form)

@app.route('/train_details',methods=['GET', 'POST'])
def train_details():
    form = TrainDetails()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_details.html', form=form)
		else:
		   train_name_number = request.form['name']
		   response={}
		   response = result.get_train_name_number(train_name_number)
		   return render_template('response_train_details.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_details.html', form=form)

@app.route('/train_cancelled',methods=['GET', 'POST'])
def train_cancelled():
    form = TrainCancelled()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_cancelled.html', form=form)
		else:
		   running_date = request.form['doj']
		   response={}
		   # running_date =datetime.datetime.strptime(str(running_date), '%Y-%m-%d').strftime('%d-%m-%Y')
		   # running_date =datetime.datetime.strptime(str(running_date))

		   response = result.get_cancelled_trains(running_date)
		   return render_template('response_train_cancelled.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_cancelled.html', form=form)

@app.route('/train_reschedule',methods=['GET', 'POST'])
def train_reschedule():
    form = TrainReschedule()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_reschedule.html', form=form)
		else:
		   running_date = request.form['doj']
		   response={}
		   # running_date =datetime.datetime.strptime(str(running_date), '%Y-%m-%d').strftime('%d-%m-%Y')
		   response = result.get_rescheduled_trains(running_date)
		   return render_template('response_train_reschedule.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_reschedule.html', form=form)

@app.route('/train_pnr',methods=['GET', 'POST'])
def train_pnr_status():
    form = TrainPNR()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_pnr.html', form=form)
		else:
		   pnr = request.form['name']
		   response={}
		   response = result.get_train_pnr_status(pnr)
		   return render_template('response_pnr_status.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_pnr.html', form=form)

@app.route('/station_name',methods=['GET', 'POST'])
def train_station_name():
    form = StationName()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_station_name.html', form=form)
		else:
		   st_name = request.form['name']
		   response={}
		   response = result.get_train_name_to_code(st_name)
		   return render_template('response_train_station_name.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_station_name.html', form=form)

@app.route('/station_code',methods=['GET', 'POST'])
def train_station_code():
    form = StationCode()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_station_code.html', form=form)
		else:
		   st_name = request.form['name']
		   response={}
		   response = result.get_train_code_to_name(st_name)
		   return render_template('response_train_station_code.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_station_code.html', form=form)

@app.route('/train_btw_station',methods=['GET', 'POST'])
def train_between_station():
    form = TrainBTStation()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_btw_station.html', form=form)
		else:
		   s_name = request.form['s_code']
		   d_name = request.form['d_code']
		   running_date = request.form['doj']
		   # modify_running_date =datetime.datetime.strptime(str(running_date), '%Y-%m-%d').strftime('%d-%m-%Y')
		   response={}
		   # response = result.get_train_between_stations(s_name,d_name,modify_running_date[:5])
		   response = result.get_train_between_stations(s_name,d_name,running_date)

		   return render_template('response_train_btw_station.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_btw_station.html', form=form)

@app.route('/suggest_train',methods=['GET', 'POST'])
def suggest_train():
    form = TrainSuggest()
    if request.method == 'POST':
    	# train_name = request.form['name']
    	# response={}
    	# response = result.get_suggest_train(train_name)
    	# print "response========",response.keys(),type(response)
    	# return json.dumps(response)
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_suggest.html', form=form)
		else:
		   train_name = request.form['name']
		   response={}
		   response = result.get_suggest_train(train_name)
		   return render_template('response_train_suggest.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_suggest.html', form=form)

@app.route('/suggest_station',methods=['GET', 'POST'])
def suggest_station():
    form = StationSuggest()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('station_suggest.html', form=form)
		else:
		   station_name = request.form['name']
		   response={}
		   response = result.get_train_suggest_station(station_name)
		   return render_template('response_station_suggest.html',rows =[response])
    elif request.method == 'GET':
       return render_template('station_suggest.html', form=form)

@app.route('/train_seat_availability',methods=['GET', 'POST'])
def get_seat_availability():
    form = TrainSeatAvailibity()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_seat_availability.html', form=form)
		else:
		   train_name = request.form['name']
		   source = request.form['source']
		   destination = request.form['destination']
		   doj = request.form['doj']
		   class_code = request.form['class_code']
		   quota = request.form['quota_code']
		   response={}
		   response = result.get_train_seat_availabity(train_name,source,destination,doj,class_code,quota)
		   return render_template('response_seat_availability.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_seat_availability.html', form=form)

@app.route('/fair_enquiry',methods=['GET', 'POST'])
def get_train_fair_enquiry():
    form = TrainFairEnquiry()
    if request.method == 'POST':
		if form.validate() == False:
		   flash('All fields are required.')
		   return render_template('train_fair_enquiry.html', form=form)
		else:
		   train_no = request.form['name']
		   source = request.form['source_station']
		   destination = request.form['dest_station']
		   age = request.form['age']
		   quota_code = request.form['quota_code']
		   doj = request.form['doj']
		   response={}
		   response = result.get_train_fair_enquiry(train_no,source,destination,age,quota_code,doj)
		   return render_template('response_train_fair_enquiry.html',rows =[response])
    elif request.method == 'GET':
       return render_template('train_fair_enquiry.html', form=form)



if __name__ == '__main__':
   app.run(debug=True)
