import glob
import os
for name in glob.glob('*'):
    if 'sff' in name:
        os.system('bzip2 -d {0}'.format(name))
        os.system('./sff2fastq/sff2fastq {0} -o {1}'.format(name.strip('.bz2'),name.replace('sff','fastq')))
                
