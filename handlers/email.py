#!/usr/bin/python2.7
import sys, json, os

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
    mail_to = os.environ["MAIL_TO"]
except:
    print "unable to send mail - missing one of the envvars of the email.py handler"
    exit(2)

print hostname, ip, time, mail_from, smtp_user