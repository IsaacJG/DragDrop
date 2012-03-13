#!/usr/bin/python
#coding: utf-8
from ftplib import FTP
import sys, os

__author__ = 'Isaac Grant'

def cmd(command):
        pipe = os.popen(command)
        output, status = pipe.read(), pipe.close()
        return output, status

def parseArgs():
        args = {}
        for arg in sys.argv:
                if '-encrypt' in arg:
                        args['encrypt'] = arg[9:]
                if '-host' in arg:
                        args['host'] = arg[6:]
                if '-username' in arg:
                        args['username'] = arg[10:]
                if '-password' in arg:
                        args['password'] = arg[10:]
                if '-directory' in arg:
                        args['directory'] = arg[11:]
                if '-help' in arg:
                        args['help'] = True
        return args

def parseConfig():
        hold = open('F:\\Dropbox\\Python\\DragDrop\\config.txt', 'r')
        config = hold.read()
        hold.close()
        encrypt = config[config.find('encrypt')+8:]
        encrypt = bool(config[:config.find('\n')])
        host = config[config.find('host')+5:]
        host = host[:host.find('\n')]
        username = config[config.find('username')+9:]
        username = username[:username.find('\n')]
        password = config[config.find('password')+9:]
        password = password[:password.find('\n')]
        directory = config[config.find('directory')+10:]
        directory = directory[:directory.find('\n')]
        return { 'host': host, 'username': username,
                'password': password, 'directory': directory,
                'encrypt': encrypt }

def main(host, username, password, directory, encrypt):
        print 'Signing on to %s as %s...' % (host, username)
        if encrypt:
                print 'Encryption is being used...'
                ftp = FTP(host, username, password.decode('base64'))
        else:
                print 'WARNING: Password is stored in raw text'
                ftp = FTP(host, username, password)
        print 'SUCCESS!'
        print ftp.getwelcome()
        if len(sys.argv) > 1:
                filename = sys.argv[1].split('\\')[-1]
                f = open(sys.argv[1], 'r')
                print 'Uploading %s to %s...' % (filename, directory)
                ftp.cwd(directory)
                ftp.storbinary('STOR %s' % filename, f)
                raw_input('Completed! Press enter to exit')
                f.close()
        else:
                print 'No file to upload, exiting...'
                sys.exit(0)

if __name__ == '__main__':
        data = parseConfig()
        args = parseArgs()
        toAdd = {}
        for i in data:
                for j in args:
                        if i == j:
                                if data[i] != args[j]:
                                        data[i] = args[j]
                        elif j not in data:
                                toAdd[j] = args[j]
        for i in toAdd:
                data[i] = toAdd[i]
        try:
                if data['help']:
                        print '''Usage: dragdrop.exe [file] [-args]\n
Ex: dragdrop.exe X:\Foo.bar -arg=value
Arguments:\n
-------------------------------------
-encrypt        |       password passed in config or as a flag is encrypted with base64\n
        true | false\n
-host           |       ftp host to upload to\n
        (ftp.microsoft.com)\n
-username       |       username to log on to ftp server with\n
-password       |       ftp password\n
-directory      |       directory on ftp server where file will be uploaded\n
-help           |       this dialogue\n
------------------------------------------------------------------------
http://github.com/waterwolf20/DragDrop'''
                sys.exit(0)
        except Exception, e:
                pass
        main(data['host'], data['username'],
             data['password'], data['directory'],
             data['encrypt'])
