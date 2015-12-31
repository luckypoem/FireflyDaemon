#!/usr/bin/env python
# coding:utf8
"""
编译脚本
"""
from py_compile import compile, PyCompileError
import os


BUILD_PATH = "./compile/"
SRC_PATH = "./"
IGNORE_LIST = [
    "compile",
    '.idea',
    '.svn',
    "compile.py",
    "setting.sample.py"
]


def build_path(src, build, path="", rx=None, quiet=1):
    build = os.path.join(build, path)
    src = os.path.join(src, path)
    try:
        names = os.listdir(src)
    except os.error:
        print "Can't list", src
        names = []
    # 检查 build 目录
    if not os.path.exists(build):
        os.makedirs(build, 00755)
    # 开始编译
    for name in names:
        if name in IGNORE_LIST:
            continue
        srcname = os.path.join(src, name)
        if not os.path.isdir(srcname):
            head, tail = name[:-3], name[-3:]
            if tail != ".py":
                continue
            buildname = os.path.join(build, head + ".pyc")
            try:
                compile(srcname, buildname, doraise=True)
            except PyCompileError, e:
                print "[ERROR] %s" % e.message
            print "SRC: %s" % srcname
            print "-> BUILD: %s" % buildname
        elif name != os.curdir and name != os.pardir and os.path.isdir(srcname) and not os.path.islink(srcname):
            build_path(src, build, name, rx=rx, quiet=quiet)


if __name__ == "__main__":
    print "Compile Start ..."
    build_path(SRC_PATH, BUILD_PATH)
    print "Compile Finished!"
