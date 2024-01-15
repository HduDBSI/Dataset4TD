import sys
import os
sys.path.append("../") 
from project_Info import projects

# Enviroment: Windows 10 Professional Edition

# pmd-bin-7.0.0-rc1\bin\pmd.bat check -d ..\projects\antlr4-4.11.0 -R PMD_TEDIOUS.xml -r pmdResults\antlr4-4.11.0.csv
def PMD(project):
    pmd = 'pmd-bin-7.0.0-rc1\\bin\\pmd.bat'
    dir = '-d ..\\projects\\' + project
    rule = '-R PMD_TEDIOUS.xml'
    outfile = '-r pmdResults\\' + project + '_pmd.csv'

    cmd = [pmd, 'check', dir, rule, outfile]
    cmd = " ".join(cmd) 
    print(cmd)
    e = os.popen(cmd)
    e.close()

# jdk11\bin\java.exe -jar checkstyle-10.9.3-all.jar -c CS_TEDIOUS.xml -f plain -o csResults\antlr4-4.11.0.csv ..\projects\antlr4-4.11.0
def CheckStyle(project):
    jdk = 'jdk11\\bin\\java.exe'
    jar = "-jar checkstyle-10.9.3-all.jar"
    rule = '-c CS_TEDIOUS.xml'
    format = '-f plain'
    outfile = '-o csResults\\' + project + '_cs.csv'
    dir = '..\\projects\\' + project
    
    cmd = [jdk, jar, rule, format, outfile, dir]
    cmd = " ".join(cmd)                                  
    print(cmd)
    e = os.popen(cmd)
    e.close()


from time import time
t = time()
os.makedirs('csResults', exist_ok=True)
os.makedirs('pmdResults', exist_ok=True)
for project in projects:
    PMD(project)
    CheckStyle(project)

print('cost time:', time()-t)