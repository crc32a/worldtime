from flask import Flask, render_template

import datetime
import dateutil.tz
import dateutil
import yaml
import sys
import os
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

def load_yaml(file_path):
    full_path = os.path.abspath(os.path.expanduser(file_path))
    fp = open(full_path,"r")
    obj = yaml.safe_load(fp)
    fp.close()
    return obj

app = Flask(__name__)


@app.route("/")
def index():
    dt = datetime.datetime.now(dateutil.tz.tzlocal())
    los_angeles = dt.astimezone(dateutil.tz.gettz("America/Los_Angeles"))
    chicago = dt.astimezone(dateutil.tz.gettz("America/Chicago"))
    utc = dt.astimezone(dateutil.tz.tzutc())
    london = dt.astimezone(dateutil.tz.gettz('Europe/London'))
    india = dt.astimezone(dateutil.tz.gettz('Asia/Kolkata'))
    manila = dt.astimezone(dateutil.tz.gettz("Asia/Manila"))
    tokyo = dt.astimezone(dateutil.tz.gettz('Asia/Tokyo'))
    times = [
             ["Los Angeles", printdt(los_angeles)],
             ["Chicago", printdt(chicago)],
             ["UTC", printdt(utc)],
             ["London", printdt(london)],
             ["India", printdt(india)],
             ["Manila", printdt(manila)],
             ["Tokyo", printdt(tokyo)],
            ]
    ctx = {"times": times}
    return render_template('worldtime.html', **ctx)

if __name__ == "__main__":
    conf = load_yaml("~/worldtime.yaml")
    app.run(host=conf["host"], port=conf["port"])
