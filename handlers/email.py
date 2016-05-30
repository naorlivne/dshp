#!/usr/bin/python2.7
import sys
handler_json = sys.argv[1]
file = open("example.txt", "w")
file.write(handler_json)
file.close()