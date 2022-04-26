#!/bin/python3

import os
import sys
import itertools
import shutil
import shlex
import subprocess


def error(msg, obj=None):
    if obj is None:
        print(f'error: {msg}')
    else:
        print(f'error: \'{obj}\': {msg}')


def check_args(args, *checks):
    if len(args) < len(checks):
        error('too few args')
        return False
    if len(args) > len(checks):
        error('too many args')
        return False
    for a, check in zip(args, checks):
        if not check:
            continue
        if not check[0](a):
            error(check[1], a)
            return False
    return True


def ls(args):
    if not check_args(args):
        return
    print(*os.listdir(os.getcwd()))


def pwd(args):
    if not check_args(args):
        return
    print(os.getcwd())


def cd(args):
    if not check_args(args, (os.path.isdir, 'not a directory')):
        return
    os.chdir(args[0])


def cp(args):
    if not check_args(args, (os.path.exists, 'file not exists'), ()):
        return
    shutil.copyfile(args[0], args[1])


def mv(args):
    if not check_args(args, (os.path.exists, 'file not exists'), ()):
        return
    shutil.move(args[0], args[1])


def rm(args):
    if not check_args(args, (os.path.isfile, 'not exists or not a regular file')):
        return
    os.remove(args[0])


def rmdir(args):
    if not check_args(args, (os.path.isdir, 'not a directory')):
        return
    try:
        os.rmdir(args[0])
    except:
        error('directory is not empty')


def mkdir(args):
    if not check_args(args, ()):
        return
    try:
        os.mkdir(args[0])
    except:
        error('directory already exists')


def run(args):
    args = [list(g)
            for k, g in itertools.groupby(args, lambda x: x != '|') if k]
    with open('in.pipe', 'wt'):
        pass
    for i, arg in enumerate(args):
        with open('out.pipe', 'wt') as pipe_out:
            with open('in.pipe', 'rt') as pipe_in:
                subprocess.run(arg, stdin=pipe_in if i else sys.stdin,
                               stdout=pipe_out if i != len(args) - 1 else sys.stdout)
            os.remove('in.pipe')
            os.rename('out.pipe', 'in.pipe')
    with open('in.pipe') as f:
        print(f.read(), end='')
    os.remove('in.pipe')


commands = {
    'ls': ls,
    'pwd': pwd,
    'cd': cd,
    'cp': cp,
    'mv': mv,
    'rm': rm,
    'rmdir': rmdir,
    'mkdir': mkdir,
    'run': run
}

if __name__ == '__main__':
    print('hey yo, welcome, that\'s shell')

    while True:
        cmd = shlex.split(input('> '))
        if not cmd:
            continue
        if cmd[0] == 'exit':
            break
        try:
            commands[cmd[0]](cmd[1:])
        except:
            error('no such command')
