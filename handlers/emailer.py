#!/usr/bin/python2.7
import sys, json, os, smtplib

json_args = json.loads(sys.argv[1])
hostname = json_args["hostname"]
ip = json_args["ip"]
time = json_args["time"]
try:
    mail_from = os.environ["MAIL_FROM"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = os.environ["SMTP_PORT"]
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    try:
        smtp_tls = os.environ["SMTP_TLS"]
    except:
        pass
    mail_to = os.environ["MAIL_TO"].split(",")
except:
    print "unable to send mail - missing one of the envvars of the emailer.py handler"
    exit(2)

try:
    smtpObj = smtplib.SMTP(host=smtp_server,port=smtp_port)
    try:
        if smtp_tls == "True":
            smtpObj.starttls()
    except:
        pass
    smtpObj.login(smtp_user, smtp_pass)
    for mail_address in mail_to:
        message = """\
From: %s
To: %s
Subject: %s

%s\
""" % (mail_from, mail_address,"DSHP alert: " + hostname + " access attempt detected", "there have an attempet to access " + hostname + " at " + time + " from ip address " + ip)
        smtpObj.sendmail(mail_from, mail_to, message)
        smtpObj.quit()
except:
    print "unable to send mail - something went wrong"
