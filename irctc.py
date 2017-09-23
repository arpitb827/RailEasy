import urllib2
import json

# apikey = 'mia22f6h'
# Api_uri = 'http://api.railwayapi.com/'

class RAIL_API():
	def __init__(self,url,api_key):
		self.API_URI=url
		self.api_key=api_key


	def get_train_live_status(self,train_no,date_joing):
		"""Calling function to get the train live status"""

		#format for date sending 20170601
		# Api_url= self.API_URI+'/live/train/'+str(train_no)+'/doj/'+str(date_joing)+'/apikey/'+str(self.api_key)+'/'
		Api_url= self.API_URI+'live/train/'+str(train_no)+'/date/'+str(date_joing)+'/apikey/'+str(self.api_key)+'/'

		print "url====",Api_url
		result = self.get_request(Api_url)
		# result = urllib2.urlopen(Api_url)

		print "result==========",result
		# response = json.load(result)
		return result

		
	def get_train_pnr_status(self,pnr_no):
		"""Get PNR status"""
		Api_url= self.API_URI+'pnr-status/pnr/'+str(pnr_no)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result
		
	def get_train_route_information(self,train_no):
		"""A function to get the train route information"""
		Api_url= self.API_URI+'/route/train/'+str(train_no)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result		

	def get_train_seat_availabity(self,train_no,source_station_code,destination_code,date_joining,class_code,quota_code):
		#format date of joing <doj in DD-MM-YYYY>
		Api_url= self.API_URI+'check-seat/train/'+str(train_no)+'/source/'+str(source_station_code)+'/dest/'+str(destination_code)+'/date/'+str(date_joining)+'/class/'+str(class_code)+'/quota/'+str(quota_code)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result
		# response = json.load(result)
		# print "response=========",response

		
	def get_train_between_stations(self,source_station_code,destination_code,date):
		"""Get Trains Between Station"""
		Api_url= self.API_URI+'between/source/'+str(source_station_code)+'/dest/'+str(destination_code)+'/date/'+str(date)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result
		

	def get_train_name_number(self,train_name_number):
		"""A Function to get the train details"""
		#format <name or number>
		# Api_url= self.API_URI+'/name_number/train/'+str(train_name_number)+'/apikey/'+str(self.api_key)+'/'
		Api_url= self.API_URI+'name-number/train/'+str(train_name_number)+'/apikey/'+str(self.api_key)+'/'

		result = self.get_request(Api_url)

		print "result==========",result
		return result
		

	def get_train_fair_enquiry(self,train_no,source_station_code,destination_code,age,quota_code,doj):
		Api_url= self.API_URI+'fare/train/'+str(train_no)+'/source/'+str(source_station_code)+'/dest/'+str(destination_code)+'/age/'+str(age)+'/quota/'+str(quota_code)+'/date/'+str(doj)+'/apikey/'+str(self.api_key)+'/'
		
		result = self.get_request(Api_url)

		print "result==========",result
		return result

	def get_train_arrival_station(self,station_code,hours_to_arrival):
		Api_url= self.API_URI+'/arrivals/station/'+str(station_code)+'/hours/'+str(hours_to_arrival)+'/apikey/'+str(self.api_key)+'/'
		result = urllib2.urlopen(Api_url)

		print "result==========",result
		response = json.load(result)
		print "response=========",response

	# def get_train_arrival_station():
	# 	Api_url= self.API_URI+'/arrivals/station/<station code>/hours/<hours to search within>/apikey/'+str(self.api_key)+'/'
	# 	result = urllib2.urlopen(Api_url)

	# 	print "result==========",result
	# 	response = json.load(result)
	# 	print "response=========",response


	def get_cancelled_trains(self,doj):
		"""Function to get all cancelled trains"""
		Api_url= self.API_URI+'/cancelled/date/'+str(doj)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result

	def get_rescheduled_trains(self,doj):
		Api_url= self.API_URI+'/rescheduled/date/'+str(doj)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result

	def get_train_name_to_code(self,station_name):
		"""Find train by code"""
		Api_url= self.API_URI+'name-to-code/station/'+str(station_name)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result
		return result

	def get_train_code_to_name(self,station_code):
		"""Find train by station code"""
		Api_url= self.API_URI+'/code-to-name/code/'+str(station_code)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)
		print "result==========",result
		
		return result
		
	def get_train_suggest_station(self,station):
		"""Suggest station name by name"""
		Api_url= self.API_URI+'suggest-station/name/'+str(station)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)

		print "result==========",result

		return result

	def get_suggest_train(self,train_name_number):
		"""Get Automatic suggestive train""" #<partial train name or number>
		Api_url= self.API_URI+'suggest-train/train/'+str(train_name_number)+'/apikey/'+str(self.api_key)+'/'
		result = self.get_request(Api_url)
		print "result==========",result
		
		return result


	def get_request(self,url):
		print "url========",url
		req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		try:
			response = urllib2.urlopen(req)
			the_page = json.load(response)
			# d = dict(xmltodict.parse(str(the_page))['response'])
			return the_page
		except urllib2.HTTPError, e:
			raise IOError('Got the error during processing the HTTP request. error message : %s , error code : %s' %(str(e.msg), str(e.code)))
		except urllib2.URLError, e1:
			raise IOError('It seems like the Input URL is wrong. error code : ' + str(e1.reason.errno))


	def get_request_from_news(self,url):
		print "url========",url
		req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		try:
			response = urllib2.urlopen(req)
			the_page = json.load(response)
			# d = dict(xmltodict.parse(str(the_page))['response'])
			return the_page
		except urllib2.HTTPError, e:
			raise IOError('Got the error during processing the HTTP request. error message : %s , error code : %s' %(str(e.msg), str(e.code)))
		except urllib2.URLError, e1:
			raise IOError('It seems like the Input URL is wrong. error code : ' + str(e1.reason.errno))