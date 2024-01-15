import sys
import os
sys.path.append("../") 
from project_Info import projects
from time import time

def extractMetrics(project):
    srcfile = '..\\projects\\' + project
    jdk = 'jdk11\\bin\\java.exe'
    outfile = '..\\metrics\\' + project + '-'
    jar = 'ck.jar'
    parameters = 'True 0 False'
    cmd = [jdk, '-jar', jar, srcfile, parameters, outfile]
    cmd = " ".join(cmd)                                  
    print(cmd)
    e = os.popen(cmd)
    e.close()

t = time()
granularities = ["class", "method"]
for project in projects:
    extractMetrics(project)
print('cost time:', time()-t)


