# coding: utf8
import datetime


def write_log(name):
    f = file("logs/%s.log" % name, "a+")
    f.write(str(datetime.datetime.now()))
    f.flush()
    f.close()
