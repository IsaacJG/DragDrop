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
        runpath  = config[config.find('runpath')+8:]
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
        for i in data:
                for j in args:
                        if i == j:
                                if data[i] != args[j]:
                                        data[i] = args[j]
        main(data['host'], data['username'],
             data['password'], data['directory'],
             data['encrypt'])
