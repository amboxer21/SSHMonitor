#!/usr/bin/env python

import os
import re
import sys
import time
import logging.handlers

from optparse import OptionParser

class ensures(object):

    @classmethod
    def instancemethod(cls,func):
        def wrapper(*arguments):
            if not [arg for arg in arguments if re.match('<__main__.*object at.*>',str(arg))]:
                raise SyntaxError('Method must be an instance method of a class!')
            [func(arg) for arg in arguments[1:]]
        return wrapper

    @classmethod
    def dictionary(cls,func):
        @accepts.instancemethod
        def wrapper(*arguments):
            for arg in arguments[1:]:
                if not isinstance(arg, dict):
                    raise TypeError('"' + str(arg) + '" is not a dictionary!')
            return func(cls,arguments[0])
        return wrapper

class Logger(object):

    def __init__(cls, **kwargs):
        print(kwargs)

    @classmethod
    def log(cls,level,message,logfile="/var/log/sshmonitor.log"):
        comm = re.search("(WARN|INFO|ERROR)", str(level), re.M)
        try:
            handler = logging.handlers.WatchedFileHandler(
                os.environ.get("LOGFILE",logfile)
            )
            formatter = logging.Formatter(logging.BASIC_FORMAT)
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.setLevel(os.environ.get("LOGLEVEL", str(level)))
            root.addHandler(handler)
            # Log all calls to this class in the logfile no matter what.
            if comm is None:
                print(str(level) + " is not a level. Use: WARN, ERROR, or INFO!")
                return
            elif comm.group() == 'ERROR':
                logging.error(str(time.asctime(time.localtime(time.time()))
                    + " - SSHMonitor - "
                    + str(message)))
            elif comm.group() == 'INFO':
                logging.info(str(time.asctime(time.localtime(time.time()))
                    + " - SSHMonitor - "
                    + str(message)))
            elif comm.group() == 'WARN':
                logging.warn(str(time.asctime(time.localtime(time.time()))
                    + " - SSHMonitor - "
                    + str(message)))
            if options.verbose or str(level) == 'ERROR':
                print("(" + str(level) + ") "
                    + str(time.asctime(time.localtime(time.time()))
                    + " - SSHMonitor - "
                    + str(message)))
        except IOError as eIOError:
            if re.search('\[Errno 13\] Permission denied:', str(eIOError), re.M | re.I):
                print("(ERROR) SSHMonitor - Must be sudo to run SSHMonitor!")
                sys.exit(0)
            print("(ERROR) SSHMonitor - IOError in Logging class => "
                + str(eIOError))
            logging.error(str(time.asctime(time.localtime(time.time()))
                + " - SSHMonitor - IOError => "
                + str(eIOError)))
        except Exception as eLogging:
            print("(ERROR) SSHMonitor - Exception in Logging class => "
                + str(eLogging))
            logging.error(str(time.asctime(time.localtime(time.time()))
                + " - SSHMonitor - Exception => " 
                + str(eLogging)))
            pass
        return

# The config filename is passed to this class in the ImageCapture classes __init__ method.
# The option is the default value set in optparser and is blank by default. See the
# optparser declaration at the bottom in the if __name__ == '__main__' check.
class ConfigFile(object):

    def __init__(self, file_name):
        self.args_list = []
        self.file_name = file_name
        if file_name:
            try:
                self.config_file = open(file_name,'r').read().splitlines()
                self.config_file_syntax_sanity_check()
            except IOError:
                Logger.log("ERROR","Config file does not exist.")
                sys.exit(0)

    def __getattr__(self, key):
        pass

    def __setattr__(self, key, val):
        pass

    # If a config file is 'NOT' passed via command line then this method will set the global
    # base variables for the config_dict data structure using the optparsers default values.
    # ---
    # If a config file 'IS' passed via command line then this method will read in the options
    # values and set the base options for the global config_dict data structure. If the config
    # files options have empty values then those options are loaded into an array nested inside
    # of the config_dict data structure. Which will later be used as a reference against the
    # config_data structure so it knows to use optparsers default values for these options.
    def config_options(self):
        # If config file is 'NOT' supplied use optparsers default values.
        if not self.file_name:
            for default_opt in config_dict[0].keys():
                config_dict[0][default_opt][0] = config_dict[0][default_opt][1]
                Logger.log("INFO", "Setting option("
                    + default_opt + "): "
                    + str(config_dict[0][default_opt][0]))
            return
        # If the config file exists and the syntax is correct we will have to convert the
        # 'bool' values in the file which are being loaded in as strings to actual bool values.
        # The same applies for integers otehrwise load the values in as is.
        for line in self.config_file:
            comm = re.search(r'(^.*)=(.*)', str(line), re.M | re.I)
            if comm is not None:
                if not comm.group(2):
                    config_dict[1].append(comm.group(1))
                elif re.search('true', comm.group(2), re.I) is not None:
                    config_dict[0][comm.group(1)][0] = True
                elif re.search('false', comm.group(2), re.I) is not None:
                    config_dict[0][comm.group(1)][0] = False
                elif re.search('([0-9]{1,6})', comm.group(2)) is not None:
                    config_dict[0][comm.group(1)][0] = int(comm.group(2))
                else:
                    config_dict[0][comm.group(1)][0] = comm.group(2)
        return config_dict

    # If command line options 'ARE' passed via optparser/command line then this method
    # will override the default values set with optparser as well as override the options
    # in the config file that was passed.
    def override_values(self):
        for default_opt in config_dict[0].keys():
            comm = re.search('-(\w{0,9}|)'
                + config_dict[0][default_opt][2], str(sys.argv[1:]), re.M)
            if comm is not None:
                Logger.log("INFO", "Overriding "
                    + str(default_opt)
                    + " default value with command line switch value("
                    + str(config_dict[0][default_opt][1]) + ")")
                config_dict[0][default_opt][0] = config_dict[0][default_opt][1]

    # If a config file is supplied then this method will use the default options
    # in optparser if the option in the config file has no value. So if the password
    # option in the config file looks like this -> password= then it will be populated
    # by this method.
    def populate_empty_options(self):
        if config_dict[1] and self.config_file_supplied():
            for opt in config_dict[1]:
                config_dict[0][opt][0] = config_dict[0][opt][1]

    def config_file_supplied(self):
        if re.search(r'(\-C|\-\-config\-file)',str(sys.argv[1:]), re.M) is None:
            return False
        return True

    def config_file_syntax_sanity_check(self):
        for line in self.config_file:
            comm = re.search(r'(^.*)=(.*)', str(line), re.M | re.I)
            if comm is not None:
                try:
                    config_dict[0][comm.group(1)]
                except KeyError:
                    Logger.log("ERROR", "Config file option("
                        + comm.group(1)
                        + ") is not a recognized option!")
                    sys.exit(0)

if __name__ == '__main__':

    configFile = ConfigFile('test.txt')
