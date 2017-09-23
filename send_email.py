import smtplib

from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail():

	def send_email_from_website(self, name,sender, receivers, message,phone):
		print "sender,receivers,message=========",sender,receivers,message
		host = 'smtp.gmail.com:587'
		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "RailEasy: Enquiry"
		msg['From'] = sender
		msg['To'] = receivers

		# Create the body of the message (a plain-text and an HTML version).
		text = message
		text+='\n'+"Contact"+":"+str(phone)
		# text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
		# html = """\
		# <html>
		#   <head></head>
		#   <body>
		#     <p>Hi!<br>
		#        How are you?<br>
		#        Here is the <a href="http://www.python.org">link</a> you wanted.
		#     </p>
		#   </body>
		# </html>
		# """
		# Record the MIME types of both parts - text/plain and text/html.
		print "text",text
		part1 = MIMEText(text, 'plain')
		# part2 = MIMEText(html, 'html')

		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		msg.attach(part1)
		# msg.attach(part2)

		
		try:
		   smtpObj = smtplib.SMTP(host)
		   smtpObj.ehlo()
		   smtpObj.starttls()
		   smtpObj.login(receivers, '7718015847')
		   smtpObj.sendmail(sender, receivers, msg.as_string())
		   smtpObj.close()       
		   print "Successfully sent email"
		except SMTPException,err:
		   print "Error: unable to send email ",err
