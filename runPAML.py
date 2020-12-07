import glob
import os

for clustDir in glob.glob('cluster*'):
    print(clustDir)
    os.system('cp paml_control_model2 {0}'.format(clustDir))
    os.chdir(clustDir)
    os.system('codeml paml_control_model2')
    os.chdir('..')

 
 
