import logging
import os

logging.basicConfig(level=logging.DEBUG)

class FileHelper():
    def WriteToFile(fn:str,txt:str): # this will write text to log file
        """
        Write to file\n
        - fn: file name\n
        - txt: text to write
        """
        file_path = os.path.dirname(os.path.realpath(__file__))
        LogFile=file_path+'/'+fn
        with open(LogFile, "a") as file1:
            file1.write(txt+ '\n')
        file1.close
        logging.info('Writing into file: '+LogFile)

    def ReadFile(fn:str):
            """
            Read from file\n
            - fn: file name \n
            Return file content
            Return 0 if error
            """
            try:
                with open(fn,"r") as text:
                    res=text.read()
            except:
                logging.error('Error opening file')
                return '0'
            return res

class Helper():
    """
    this is helper class
    """
             
    def ReadConfigFile(fn:str): #read user data
        """
        Read config file\n
        - fn: file name \n
        - '#' will be ignored\n
        - new lines will be ignored\n
        Return dict
        """
        res = {}
        try:
            with open(fn,"r") as text:
                for line in text:
                    if not line[0]=='#' and not line=='\n': #remove comments and new lines
                        key, value = line.split('=')
                        if len(key)>1 :     
                                if value[-1]=='\n': res[key] = value[:-1]
                                else: res[key] = value
        except:
            logging.error('Error opening config file')
        return res
    
    def UpdateConfigFile(fn:str,keyIn:str,valIn:str): #update value user data
        """
        Update config file\n
        - fn: file name \n
        - keyIn: key to modify\n
        - valIn: new value\n
        Return true if key found
        """
        listos=FileHelper.ReadConfigFile(fn)
        if len(listos)==0 or keyIn not in list(listos.keys()):
            logging.error('Key not found')
            return False
        else:
            try:
                
                with open(fn,"r") as text:
                    data = text.readlines()
                    counter=0
                    for line in data:
                        if not line[0]=='#' and not line=='\n': #remove comments and new lines
                            key, value = line.split('=')
                            if len(key)>1 and key == keyIn: #bingo  
                                data[counter]=keyIn+'='+valIn
                        counter+=1
                    with open(fn, 'w') as file:
                        file.writelines(data)
            except Exception as e:
                logging.error('Error opening config file: '+e)
                return False
            return True
