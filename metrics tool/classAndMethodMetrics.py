import sys
import os
import numpy as np
sys.path.append("../") 
from project_Info import projects, project_names
import time

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


times = []
granularities = ["class", "method"]
for project in projects:
    t = time.time()
    extractMetrics(project)
    times.append(time.time() - t)
with open('time-ck.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
    f.write("Total\t{:.2f}\n".format(np.sum(times)))
