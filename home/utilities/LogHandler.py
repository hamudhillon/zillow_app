import sys,os
from os import path as os_path
from sys import path as sys_path
import logging
from traceback import format_tb
from logging.handlers import RotatingFileHandler
from os.path import dirname, abspath
root_path = dirname(abspath(__file__))
sys.path.insert(0, root_path)

MAX_FILE_SIZE = 50000
MAX_FILES = 30

class DologHandler():
    def __init__(self,error_file,run_with):
        
        # Checks if dir exists or not else creates
        self.parent_dir = root_path
        self.path = os.path.join(self.parent_dir, 'logs/scrappers.log')
        self.check = os.path.isfile(self.path)
        print('Path exists -',self.check)
        if self.check==False:
            os.mkdir(os.path.join(self.parent_dir, 'logs/'))
        # ---------------------------------------------------------
        self.stream_logger = logging.StreamHandler(stream = sys.stderr)
        # Logging Path
        self.full_filepath = root_path+str('/logs/scrappers.log')
        
        self.file_logger = RotatingFileHandler(filename=self.full_filepath,maxBytes=MAX_FILE_SIZE, backupCount=MAX_FILES)
        self.formatter = logging.Formatter("%(asctime)s %(levelname)-9s %(name)-8s %(thread)5s %(message)s")
        self.stream_logger.setFormatter(self.formatter)
        self.file_logger.setFormatter(self.formatter)
        self.logger = logging.getLogger(error_file)
        self.logger.setLevel(logging.DEBUG)
        self.file_logger.setLevel(logging.DEBUG)
        self.RUN_WITH = run_with
        # both,stream,file
        
        if self.RUN_WITH=='both':
            self.logger.addHandler(self.file_logger)
            self.logger.addHandler(self.stream_logger)
        elif self.RUN_WITH=='stream':
            self.logger.addHandler(self.stream_logger)
        elif self.RUN_WITH=='file':
            self.logger.addHandler(self.file_logger)
        
    def dolog(self,method_name,log_type,log_msg):
        if log_type=='INFO':
            log_msg = method_name+'  '+str(log_msg)
            self.logger.info(log_msg)
            # print(log_msg)
        elif log_type=='ERROR':
            str_msg = self.format_exception_info(log_msg)
            self.logger.error(str_msg)


    def format_exception_info(self, objexp):
            max_tb_level=1
            e_msg = objexp[1]
            cla, exc, trbk = objexp
            exc_name = cla.__name__
            try:
                exc_args = exc.__dict__["args"]
            except KeyError:
                exc_args = "<key exception>"
            exc_tb = format_tb(trbk, max_tb_level)
            return (exc_name, exc_args, exc_tb , e_msg)
        
# objc = DologHandler('main.py','file')
# objc.doStreamlog('INFO','Going to Process the Records')

# try:
#     a = {'user':'navdeep'}
#     cc= a['jj']
# except:
#     objc.doStreamlog('ERROR',sys.exc_info())

# for _ in range(10000):
#     objc.dolog('TEST','INFO','Going to Process the Records')
