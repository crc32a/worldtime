from flask import Flask, render_template

import datetime
import dateutil.tz
import dateutil
import sys
import re

time_re = re.compile("([0-9]+)-([0-9]+)-([0-9]+)\s+([0-9]+):([0-9]+):([0-9]+)")
td_zero = datetime.timedelta(0)


def printf(format,*args): sys.stdout.write(format%args)


def chop(line):
    return line.replace("\r","").replace("\n","")

def lpad(n,*args,**kw):
    pad_char = kw.pop("pad_char","0")
    if(len(args)>=1):
        digits = kw.pop("digits",2)
    else:
        digits = 2
    str_val = str(n)
    return pad_char*(digits - len(str_val)) + str_val

def printdt(dt):
    out = ""
    out += lpad(dt.year,4) + "-"
    out += lpad(dt.month) + "-"
    out += lpad(dt.day) + " "
    out += lpad(dt.hour) + ":"
    out += lpad(dt.minute) + ":"
    out += lpad(dt.second)
    return out

app = Flask(__name__)


@app.route("/")
def index():
    dt = datetime.datetime.now(dateutil.tz.tzlocal())

    utc = dt.astimezone(dateutil.tz.tzutc())
    loc = dt.astimezone(dateutil.tz.tzlocal())
    india = dt.astimezone(dateutil.tz.gettz('Asia/Kolkata'))
    tokyo = dt.astimezone(dateutil.tz.gettz('Asia/Tokyo'))
    london = dt.astimezone(dateutil.tz.gettz('Europe/London'))
    doha = dt.astimezone(dateutil.tz.gettz('GMT+3'))
    times = [["server local", printdt(loc)],
             ["UTC", printdt(utc)],
             ["India", printdt(india)],
             ["Tokyo", printdt(tokyo)],
             ["London", printdt(london)],
             ["Doha", printdt(doha)],
            ]
    ctx = {"times": times}
    return render_template('worldtime.html', **ctx)

if __name__ == "__main__":    
    app.run()

