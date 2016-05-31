# DSHP - Damn Simple HoneyPot

This is a honeypot designed to be as simple as possible while allowing enough modularity to automate event handling (such as email alerts, SMS or even kicking a user out).
I wrote this after not being able to find a truly zero interaction HP to stick inside a VPC that will alert only when attempted to be accessed.

### Design
DSHP opens a listening socket on the specified port and waits for any connection attempts, whenever a connection is made DSHP will return to the connection origin a configurable reply (noting by default) then close the connection, this allows you to set a fake false message or a warning if you wish.

Whenever a connection is made to the listening socket DSHP will also activate any listening handlers configured behind the scenes, by default only a email handler is included but the handler component is designed to be modular to allow easy expandability.

### Installing
The program itself is a single Python file (which isn't much longer then this guide) but it's recommended to use the  docker container version for easier use.

**Installing Via Docker**
The attached dockerfile uses alpine linux as it's base image layer, this ensures the minimum size possible for the docker image.

Run `docker run -d -p 8888:8888 -e SMTP_SERVER=<yoursmtpserveraddress> -e SMTP_TLS=True -e SMTP_USER=<yourmailuser> -e MAIL_FROM=<fakeemail@yourmailprovider.com> -e SMTP_PASS=<yourmailpass> -e SMTP_PORT=<smtpserverport>  -e MAIL_TO=yourmail@mailprovider.com -e HANDLERS='emailer.py' naorlivne/dshp`
(obviously replace everything in <> with your own values, remove "-e SMTP_TLS=True" if your SMTP doesn't use TLS)
The above example runs DSHP on port 8888 on all interfaces and emails "yourmail@mailprovider.com" whenever it's triggered, consulate the "Configuring" section below on how to configure it to your needs.

In regards to the port the recommended way is to keep the container to port 8888 and bind whatever port you wish to it (for example -p 3306:8888), note that if you are using any port other then 8888 in your conf.json\envvar you will need to expose it in the dockerfile.

**Installing Via Git**
While the recommended way to run DSHP is via docker it might be easier to run it locally for debugging:

Requires Python 2.7.x module installed.
Run `git clone git@github.com:naorlivne/DSHP.git && chmod +x dshp/dshp.py` to clone and set the file to executable.
Run `dshp.py` to run DSHP.

### Configuring 
DSHP is configured in 2 ways, the first being a conf.json file in the app root directory & the 2nd is via envvars, envvars take priority over the config file as this allows you to set a standard docker container and only change it where needed.

**Configure via conf.json file**
uses the following format:

```
{
  "port": 8888,
  "timeout": 300,
  "interface": "",
  "reply": "",
  "handlers": ["emailer.py"],
  "handler_exec": "/usr/bin/python2.7"
}
```

port = the port to listen to, defaults to 8888.
timeout = the amount of time in seconds to ignore triggering a new "handler run" should the an attacker retry accessing the DSHP port (to avoid spamming the recipients and\or overloading the handlers), defaults to 300.
interface = the interface to bind to, empty field (default) means bind to all interfaces.
reply = the reply to send to the attacker, defaults to non.
handlers = a list of handlers to trigger on each new incident, handlers root folder is the <DSHP_root_folder>/handlers folder- at least one handler must be set or DSHP won't run.
handler_exec = the handler runtime exec, defaults to /usr/bin/python2.7, you must use the same language for all handlers.

**Configure via envvar**
configure the same keys as in the conf.json, the only difference is that the keys are in all CAPS.
allowed keys are: INTERFACE,PORT,REPLY,HANDLERS,TIMEOUT

The HANDLERS requires a list format of all handlers and their parameters exactly like it would using the conf.json file (for example `HANDLERS="/usr/bin/python2.7 emailer.py","/usr/bin/python2.7 made_up_handler.py"`).

### Adding custom handlers
Installing a new handler is simply a matter of dropping it in DSHP `handlers` folder, to use it simply configure the "handlers" parameter in either the conf.json file or via the "HANDLERS" envvar ot run it (loosely inspired by nagios\sensu method of using handlers).

Handlers can be written in every language, the default docker container only includes Python, it's up to you the ensure installing any other requirements should you chose to use it as your container base image.

Whenever an event triggers it pipes to the handler a JSON file in the following format as the first command line argument (sys.argv[1]):

```
{
   "hostname": "DSHP",
   "ip": "123.123.123.123",
   "time": "2014-09-26T16:34:40.278298"
}
```

Where "hostname" is the hostname of the DSHP server, "ip" is the IP address that originated the connection (the offender) & time is ISO format timestamp of the incident. 

#### Builtin EMail handler

The builtin email handler will email every address in the "MAIL_TO" envvar, it accepts a comma seperated list of emails, it is extermly basic as it is mostly designed to help showcase DSHP handlers & assist in writing handlers.
for example `"yourmail@mailprovider.com","anothermail@fakemailprovider.com","yetanothermail@yourfakemail.com"`
it's other required config variables (all via envars) are:
MAIL_FROM: the email from address
SMTP_SERVER: the smtp server address
SMTP_PORT: the smtp server port
SMTP_USER: the smtp server user
SMTP_PASS: the smtp server password
SMTP_TLS: if set to "True" will use TLS