#!/usr/bin/python2.7
import socket, sys, json, os, subprocess, datetime, time
from thread import *


# function that sets config variables with the following priority chain
# envvar > config file > default value
def read_config(conf_var):
    try:
        conf_value = os.environ[conf_var.upper()]
        if conf_var == "handlers":
            conf_value_list = conf_value.split(",")
            return conf_value_list
    except:
        try:
            conf_value = conf_file[conf_var]
        except:
            try:
                conf_value = default_conf[conf_var]
            except:
                print "critical - missing config value for " + conf_var
                sys.exit(2)
    return conf_value


# function to handle connections
def client_thread(conn):
    # Sending message to connected client
    conn.send(reply)
    # came out of loop
    conn.close()


# function to run handlers
def run_handlers(handlers):
    now = datetime.datetime.now()
    current_run_unix_time = time.time()
    if current_run_unix_time > float(last_run_unix_time + timeout):
        for handler in handlers:
            json_reply = str(json.dumps({
   "hostname": hostname,
   "ip": offender_ip,
   "time": now.isoformat()
}))
            subprocess.call([handler_exec + " " + handler + " '" + json_reply + "'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="handlers")
        return current_run_unix_time
    else:
        return last_run_unix_time


# set config variables
default_conf = {"port": 8888, "interface": "", "reply": "", "timeout": 300, "handler_exec": "/usr/bin/python2.7"}
try:
    conf_file = json.load(open("conf.json"))
    print "loaded conf.json file"
except:
    print "Warning - unable to load correctly phrased json config file"
try:
    port = int(read_config('port'))
    interface = str(read_config('interface'))
    timeout = int(read_config('timeout'))
    reply = str(read_config('reply'))
    handlers = read_config('handlers')
    handler_exec = read_config('handler_exec')
    hostname = socket.gethostname()
    last_run_unix_time = 0
except:
    print "critical - problem setting config variable"
    sys.exit(2)

# bind socket and start listening
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
try:
    s.bind((interface, port))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit(2)
print 'Socket bind complete'
s.listen(5)
print 'Socket now listening'

# keep waiting for connections
while 1:
    conn, addr = s.accept()
    offender_ip = addr[0]
    print "attempted connection from " + offender_ip
    last_run_unix_time = run_handlers(handlers)
    start_new_thread(client_thread, (conn,))

s.close()