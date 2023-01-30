import itertools
import argparse
import os
from pathlib import Path
import re
from io import StringIO
from colorama import Fore, Back, Style
from os.path import exists

class FindUrl:
    def __init__(self) -> None:
        pass
        
    home = str(Path.home())

    

    home = home+"\Aletheia"
    def find(self,name):
            for root, dirs, files in os.walk("C:\\"):
                if name in files:
                    return os.path.join(root, name)


    def ascii_group_formatter(self, iterable):
        self.BEGIN_PRINTABLES =33
        self.END_PRINTABLES = 126
        return ''.join(
            chr(x) if self.BEGIN_PRINTABLES <= x <= self.END_PRINTABLES else ' '
            for x in iterable)

    def hex_viewer(self, filename, chunk_size=128):
        yield ''
        template = '   {:<53}'

        text = ""
        with open(filename, 'rb') as stream:
            for chunk_count in itertools.count(1):
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                text = text+ self.ascii_group_formatter(chunk)
            yield template.format(text)
            

    def doFind(self,buf):
        ret = []
        for l in re.findall("((http|ftp|mailto|telnet|ssh)(s){0,1}\:\/\/[\w|\/|\.|\#|\?|\&|\=|\-|\%]+)+",buf):
            for url in l:
                if len(url) > 8 and url not in ret:
                    ret.append(url)
        
        return ret
    
    def findIP(self,buf):
        ret = []
        for l in re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',buf):
            for url in l:
                if len(url) > 8 and url not in ret:
                    ret.append(url)
        
        return ret
        
    def urlExtract(self,file,):
        urlfinders = [
            re.compile("((http|ftp|mailto|telnet|ssh)(s){0,1}\:\/\/[\w|\/|\.|\#|\?|\&|\=|\-|\%]+)+", re.IGNORECASE | re.MULTILINE)
        ]
        
        f = open(file, "r")
        buf = f.read()
        ret = []
        
        for x in urlfinders:
            ret += self.doFind(buf)
        if len(ret) > 0:
            print(Style.BRIGHT+Fore.YELLOW+"\nASCII URLs\n")
            for url in ret:
                print (Style.BRIGHT+Fore.YELLOW+" - "+Style.RESET_ALL+url)


    def IP_extract(self,file):
        urlfinders = [
            re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ]
        
        f = open(file, "r")
        buf = f.read()
        ret = []
        
        for x in urlfinders:
            ret += self.findIP(buf)
        if len(ret) > 0:
            print(Style.BRIGHT+Fore.YELLOW+"\nIPs\n")
            for url in ret:
                print (Style.BRIGHT+Fore.YELLOW+" - "+Style.RESET_ALL+url)
        else:
            print(Style.BRIGHT+Fore.RED+" No IP Found ! "+Style.RESET_ALL)

    def main(self,f,filename):
            parser = argparse.ArgumentParser(description='Hexadeciaml viewer.')
            parser.add_argument('file', nargs='?', default=f, help='the file to process')
            args = parser.parse_args()
            file = os.path.splitext(filename)[0]+"_URL.txt"
            filepath = self.home+"\\"+file
            if(exists(filepath)):
                open(filepath, "w").close()
            with open(filepath,"a") as f:
                for line in self.hex_viewer(args.file):
                    f.write(line+"\n")
                f.close()
            self.urlExtract(filepath)
            self.IP_extract(filepath)
            os.remove(filepath)
        
                
        