import os
import sys
from time import time
sys.path.append("../") 
from project_Info import projects

def generate_SBT(project):
    srcDir = 'data/java_files/' + project
    jdk = 'java'
    outfile = 'data/' + project + '.csv'
    jar = 'SBT.jar'
    cmd = [jdk, '-jar', jar, srcDir, outfile]
    cmd = " ".join(cmd)                                  
    print(cmd)
    e = os.popen(cmd)
    e.close()

t = time()
for project in projects:
    generate_SBT(project)
print('cost time:', time()-t)