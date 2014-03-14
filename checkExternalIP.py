#!/usr/bin/python
import httplib
import smtplib
import os

# sendemail function
def sendemail(externalIP):
	result = None
	
	sender = 'admin@example.com'
	receivers = ['receiver@example.com']

	template = """From: Admin <admin@example.com>
	To: Receiver <receiver@example.com>
	Subject: external Address has changed

	Your new external address is {0}
	"""

	message = template.format(externalIP)

	try:
	   smtpObj = smtplib.SMTP('localhost')
	   smtpObj.sendmail(sender, receivers, message)         
	   print "Successfully sent email"
	   result = True
	except Exception:
	   print "Error: unable to send email"
	return result;

# getExternaIPAddress function
# get current external ip address by retrieving result from
# whatismyipaddress.com
def getExternaIPAddress():
	# now connect to bot.whatismyipaddress.com 'api' service to check if it has changed
	ipServiceConn = httplib.HTTPConnection("bot.whatismyipaddress.com")
	ipServiceConn.request("GET", "/")
	ipServiceResponse = ipServiceConn.getresponse()
	status = ipServiceResponse.status

	if ( status == 200 ) : latestIP = ipServiceResponse.read()

	return latestIP

#
# main program execution begins...
#

# need to moved to script dir for running from cron
os.chdir('/root/scripts/utils')

# look up current external ip address that we have stored off previously
lastKnownIPFile = open('lastKnownIP')

# strip out trailing spaces as well after reading the 1st line (with next method)
lastKnownIP = lastKnownIPFile.next().strip()

print "Read current as : ", lastKnownIP

# make external internet call to get the external ip address assign by my ISP
latestIP = getExternaIPAddress().strip()

print "latest external IP address is :", latestIP 

if( lastKnownIP == latestIP ) :
	print "static IP still the same, all ok - no need for any action"
else :
	print "static IP address has changed, will need to issue email alert"
	emailSent = sendemail(latestIP)
	
	# write latest IP to file storage if we assume the email was delivered outbound 
	if emailSent:
		# re-open our file storage - this time in 'write' mode for writing
		lastKnownIPFile = open('lastKnownIP', 'w')
		lastKnownIPFile.write(latestIP)
		print "updated IP address into lastKnownIPFile"

#
# mail program execution ends.
#
