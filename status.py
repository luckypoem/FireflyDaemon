#!/usr/bin/env python
# coding: utf8
"""
查看服务器状态
@name: status.py 
@author: cbwfree
@create: 15/12/31 10:13
"""
import sys, psutil, time


def getServerInfo(pid):
    """
    获取服务器状态
    :return:
    """
    process = psutil.Process(pid)
    result = {
        'pid': process.pid,
        'cwd': process.cwd(),
        'name': process.name(),
        'children': {}
    }
    process.cpu_percent(interval=None)
    for proc in process.children():
        proc.cpu_percent(interval=None)
        result['children'][proc.pid] = {
            'pid': proc.pid,
            'cwd': proc.cwd(),
            'name': proc.name()
        }
    time.sleep(1)
    result['cpu'] = process.cpu_percent(interval=None)
    result['mem'] = process.memory_percent()
    result['used'] = bytes2human(process.memory_info()[0])
    result['create'] = process.create_time()
    result['status'] = process.status()
    result['threads'] = process.num_threads()
    for proc in process.children():
        result['children'][proc.pid]['cpu'] = proc.cpu_percent(interval=None)
        result['children'][proc.pid]['mem'] = proc.memory_percent()
        result['children'][proc.pid]['used'] = bytes2human(proc.memory_info()[0])
        result['children'][proc.pid]['create'] = proc.create_time()
        result['children'][proc.pid]['status'] = proc.status()
        result['children'][proc.pid]['threads'] = proc.num_threads()
    content = [
        "Name\tPID\tTIME\t\tCPU(%)\tMEM(%)\tUsed\t\tTHREADS\tSTATUS\t\tPATH",
        "%s\t%s\t%s\t%s\t%s\t%s\t\t%s\t%s\t%s" % (
            "master",
            result.get("pid"),
            formatRunTime(result.get("create")),
            result.get("cpu"),
            float("%.2f" % result.get("mem")),
            result.get("used"),
            result.get("threads"),
            result.get("status") + ("\t" if result.get("status") == "running" else ""),
            result.get("cwd")
        )
    ]
    for cpid, proc in result.get("children", {}).items():
        child = "%s\t%s\t%s\t%s\t%s\t%s\t\t%s\t%s\t%s"  % (
            proc.get("name"),
            cpid,
            formatRunTime(proc.get("create")),
            proc.get("cpu"),
            float("%.2f" % proc.get("mem")),
            proc.get("used"),
            proc.get("threads"),
            proc.get("status") + ("\t" if proc.get("status") == "running" else ""),
            proc.get("cwd")
        )
        content.append(child)
    return content


def formatRunTime(create):
    """
    格式化运行时间
    :param create:
    :return:
    """
    diff = int((time.time() - create))
    hour = diff // 3600
    diff-= hour * 3600
    minutes = diff // 60
    diff-= minutes * 60
    hour = str(hour)
    hour = "0" * (2 - len(hour)) + hour
    minutes = str(minutes)
    minutes = "0" * (2 - len(minutes)) + minutes
    diff = str(diff)
    diff = "0" * (2 - len(diff)) + diff
    return "%s:%s:%s%s" % (hour, minutes, diff, " " * (4 - len(hour)))


def bytes2human(n):
    """
    转换字节单位
    :param n:
    :return:
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f%s' % (value, s)
    return '%.2fB' % n


def curses_console(pid):
    try:
        import curses
        refresh = True
    except:
        refresh = False
    if refresh:
        stdscr = curses.initscr()
        curses.start_color()
        #文字和背景色设置，设置了两个color pair，分别为1和2
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        #关闭屏幕回显
        curses.noecho()
        try:
            while True:
                result = "\n".join(getServerInfo(pid))
                stdscr.addstr(0, 0, result, curses.color_pair(1))
                stdscr.refresh()
                time.sleep(0.5)
        except:
            pass
        finally:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            print "\n".join(getServerInfo(pid))
    else:
        print "\n".join(getServerInfo(pid)) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    if not len(args):
        print "Please enter the need to monitor the process ID..."
        sys.exit()
    try:
        ppid = int(args[0])
    except:
        print "The process ID must be an integer"
        sys.exit()
    curses_console(ppid)

