#!/usr/bin/python2.6

import sys
import os
import datetime
import datestring_functions
import redhat.pythonsetup
import redhat.altinstall

# NOTE:
# This script is meant to be run under Python 2.6.6 (the default version on 
# RHEL 6 x64) in order to make and install Python 2.7.3 as an altinstall.

def logfile_open(scripttype):
    """
    Returns an open logfile with a timestamp. It is left to the 
    calling function to write to the file and close it.
    
    This function will terminate the calling function if an IOError 
    occurs while opening the file.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
    """
    rundir = os.getcwd()
    logsdir = "/install/logs/"
    prefix = "install_" + scripttype + "_"
    dt = datetime.datetime
    date_suffix = "null"
    try:
        date_suffix = datestring_functions.datestring(dt)
    except ValueError as ve:
        print "ValueError:\n %s" % ve
        print "Bad datetime object, could not generate logfile name."
        print "Script will terminate."
        exit(1)
    # Assumes rundir is not terminated with a "/"
    logfile_path = rundir + logsdir + prefix + date_suffix + ".log"
    
    try:
        logfile = open(logfile_path, 'w')
        return logfile
    except IOError as ioe:
        print "IOError:\n %s" % ioe
        print "Could not open logfile at %s for writing." % logfile_path
        print "Script will terminate."
        exit(1)

def scriptrunner(scripttype, logfile):
    """
    Chooses and runs an installation script, and which logfile 
    that script will write its output to.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
           Supported values: "pythonsetup", "altinstall"
        2. logfile: The logfile to pass to the installation script.
    """ 
    if scripttype == "pythonsetup":
        logfile = redhat.pythonsetup.run(logfile)
    elif scripttype == "altinstall":
        logfile = redhat.altinstall.run(logfile)
    else:
        logfile.write("Error: python273_altinstall.py invoked with invalid command: %s" % scripttype)
        print "Error: python273_altinstall.py invoked with invalid command: %s" % scripttype
    return logfile

def main():
    if len(sys.argv) != 2:
        print "Usage: python273_altinstall.py < --pythonsetup | --altinstall >"
        print "--pythonsetup: Install packages needed to build Python 2.7.3 from source."
        print "--altinstall: Build and install Python 2.7.3 as an altinstall."
    else:
        args = sys.argv[1:]
        scripttype = args[0].strip()[2:]
        
        logfile = logfile_open(scripttype)
        logfile = scriptrunner(scripttype,logfile)
        logfile.close()

if __name__ == '__main__':
    main()
