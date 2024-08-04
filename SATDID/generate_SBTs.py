import os
import sys
import time
sys.path.append("../") 
from project_Info import projects, project_names
import numpy as np

def generate_SBT(project):
    srcDir = 'data\\java_files\\' + project
    jdk = 'java'
    outfile = 'data\\' + project + '.csv'
    jar = 'SBT.jar'
    cmd = [jdk, '-jar', jar, srcDir, outfile]
    cmd = " ".join(cmd)                                  
    print(cmd)
    e = os.popen(cmd)
    e.close()

times = []
for project in projects:
    t = time.time()
    generate_SBT(project)
    times.append(time.time() - t)

with open('results/time2.txt', 'w') as f:
    for t, project in zip(times, project_names):
        f.write("{}\t{:.2f}\n".format(project, t))
    f.write("Median\t{:.2f}\n".format(np.median(times)))
    f.write("Total\t{:.2f}\n".format(np.sum(times)))
        
print('cost time:', sum(times))
