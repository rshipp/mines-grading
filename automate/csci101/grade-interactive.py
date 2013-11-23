#!/usr/bin/env python

# This is a not-very-automated script for interacting with Hellman's grading
# site for CSCI101. You'll have to log in using your Mymail (Google) info.
# Navigating his site required a lot of back-and-forth between various pages
# when all I really wanted was to batch download and grade submissions. This
# mostly accomplished that, but I have no idea if/how well it currently works.

# Anyone is free to test/modify/butcher this code as they please, but use it at
# your own risk. I take no responsiblity for any terrible consequences that may
# result from you running this code, but I'll happily take credit for anything
# good that happens.

# Everything should work with Python 2.7+, although I haven't explicitly tested
# it on 3+. The logging/debugging stuff makes use of the BeautifulSoup library
# for parsing HTML (http://www.crummy.com/software/BeautifulSoup), but it's not
# technically required so I've left that code commented out. However, you will
# need Mechanize from http://wwwsearch.sourceforge.net/mechanize if you don't
# have it already.

import mechanize, getpass, re, time, zipfile, glob, os, subprocess, sys
from bs4 import BeautifulSoup

# Logging: Write BeautifulSoup HTML to file
def writeHTML(page, filename):
	with open(filename + '.html', 'w') as f:
		f.write(page.prettify().encode('utf8'))

# Present the items in a list with their indices, user selects one
def chooseOne(items):
	choice = -1
	while True:
		for index, item in enumerate(items):
			print "{}:\t{}".format(index, item[(item.rfind('/') + 1):])
		try:
			choice = input("Your choice: ")
			if int(choice) in xrange(len(items)):
				break
			else:
				raise Exception
		except KeyboardInterrupt:
			break
		except:
			print "Invalid choice. Try again."
	return choice

# Run the given script and return the result
def runScript(script):
	try:
		print
		result = subprocess.call(["python", "-u", script])
	except Exception as e:
		print e
		sys.stdout.flush()
		# Allow time for flushing output before continuing
		time.sleep(1)
	finally:
		print
		return result

# Create a browser
browser = mechanize.Browser(factory=mechanize.RobustFactory())
browser.set_handle_robots(False)
browser.set_handle_refresh(False)

# Navigate to grading website
print "Loading https://cs.mcprogramming.com/djintro/entry/"
initialResponse = browser.open("https://cs.mcprogramming.com/djintro/entry/")
homeHTML = BeautifulSoup(initialResponse.get_data())
# writeHTML(homeHTML, 'home')

# Find the login link using BeautifulSoup and follow it
loginLink = homeHTML.find('a', 'mymaillogin')
loginResponse = browser.follow_link(browser.find_link(text=loginLink.get_text()))

# Log in via Google
isLoggedIn  = False
while not isLoggedIn :
	try:
		# Select the first form on the page (should be the login form)
		browser.select_form(nr=0)
		# Checkbox to stay signed in
		# browser.form['PersistentCookie']
		email = raw_input("Email: ")
		pw = getpass.getpass()
		browser.form['Email'] = email
		browser.form['Passwd'] = pw
		print "Authenticating..."
		googleResponse = browser.submit()
	except mechanize._mechanize.FormNotFoundError:
		# loginHTML = BeautifulSoup(loginResponse.get_data())
		# writeHTML(loginHTML, 'login')
		print "No form, check login.html"
	except Exception as e:
		print e
		exit(1)

	# Check if login was successful
	loggedInHTML = BeautifulSoup(googleResponse.get_data())
	if loggedInHTML.title.get_text() == "Google Accounts":
		print "Error signing in, try again."
		continue
	else:
		print "Success. Loading assignments page..."
		isLoggedIn = True
	# writeHTML(loggedInHTML, 'loggedIn')

# Find assignments page link using Beautiful Soup and follow it
assignmentsLink = loggedInHTML.find('a')
assignmentsResponse = browser.follow_link(browser.find_link(text=assignmentsLink.get_text()))
# BeautifulSoup doesn't like the <meta> tag specifying us-ascii encoding, so get rid of it
# badAssignmentsHTML = assignmentsResponse.get_data()
# metaTag = re.compile('<meta .+/>')
# fixedAssignmentsHTML = metaTag.sub('', badAssignmentsHTML)
# assignmentsPageHTML = BeautifulSoup(fixedAssignmentsHTML)
# writeHTML(assignmentsPageHTML, 'assignmentsPage')

# Ask for a specific assignment and navigate to its submissions page
validAssignmentName = False
while not validAssignmentName:
	try:
		assignmentName = raw_input("Assignment name: ").strip()
		submissionsLink = browser.find_link(text=assignmentName)
	except mechanize._mechanize.LinkNotFoundError:
		print "Invalid assignment name, try again."
		continue
	except Exception as e:
		print e
		exit(1)
	validAssignmentName = True
submissionsResponse = browser.follow_link(submissionsLink)
# badSubmissionsHTML = submissionsResponse.get_data()
# fixedSubmissionsHTML = metaTag.sub('', badSubmissionsHTML)
# submissionsHTML = BeautifulSoup(fixedSubmissionsHTML)
# writeHTML(submissionsHTML, 'submissions')

# Determine download URL
downloadLink = browser.find_link(url_regex=re.compile('../downloadgrading/\?pgk='))
downloadPath = re.compile('/grading/.+')
fullDownloadPath = downloadPath.sub(downloadLink.url[2:], downloadLink.base_url)
# Ask where to save the file
downloadLoc = raw_input("Enter download location: ")
while not os.path.isdir(downloadLoc):
	downloadLoc = raw_input("Location must be a directory. Try again: ")
if downloadLoc[-1:] != '/':
	downloadLoc += '/'
downloadLoc += '{}_{}'.format(time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime()), assignmentName)
print "Downloading {} to {}".format(fullDownloadPath, downloadLoc)
# Download
submission = browser.retrieve(fullDownloadPath, filename=downloadLoc)

# Extract to 'submission' folder
z = zipfile.ZipFile(submission[0])
z.extractall('submission')
# Get submission ID
submissionID = fullDownloadPath[(fullDownloadPath.find('=') + 1):].replace('%3A', ':').replace('%40', '@')
print "ID is", submissionID

# Build list of python scripts
pythonScripts = []
correctFilename = True
for script in glob.glob("submission/*.py"):
	if os.path.isfile(script):
		pythonScripts.append(script)
# If there were no python scripts, list all files and select one to run
if len(pythonScripts) == 0:
	correctFilename = False
	print "No python scripts. Other files:"
	files = [item for item in glob.glob("submission/*") if os.path.isfile(item)]
	choice = chooseOne(files)
	result = runScript(files[choice])
# Otherwise, select a script to run
else:
	if len(pythonScripts) > 1:
		print "Multiple python scripts are present:"
		choice = chooseOne(pythonScripts)
	else:
		choice = 0
	result = runScript(pythonScripts[choice])

# Enter a grade for this submission?
gradeThis = raw_input("Grade this submission? (y/N)\n")
try:
	# This line *sometimes* fails with "OPTION outside of SELECT". I have no idea why.
	browser.select_form(nr=0)
	if gradeThis.lower() in ['y', 'yes']:
		print "Will grade"
	else:
		print "No grade"
		print browser.form.find_control(name=(submissionID + 'deferred'))
except Exception as e:
	print e
	with open('troublesome.html', 'w') as f:
		f.write(submissionsResponse.get_data())
