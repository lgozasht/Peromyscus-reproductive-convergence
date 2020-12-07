import glob

for clustDir in glob.glob('cluster*'):
    print(clustDir)
    with open('{0}/seqs_msa2.phylip'.format(clustDir),'w') as outFile:
        with open('{0}/seqs_msa.phy'.format(clustDir),'r') as f:
            for line in f:
                try:
                   myInt = int(line.strip().split(' ')[-1]) 
                   print(myInt)
                   myInt += 1
                   print(myInt)
                   firstLine = line.strip() + 'I\n'
                   outFile.write(firstLine)
                   continue
                except TypeError and ValueError:
                    pass
                if 'Pleucopus' in line:
                    PlLine = line.replace('Pleucopus','Pleucopus  ')
       	       	    outFile.write(PlLine)
                elif 'Pmanuclatu' in line:                   
       	            PmLine = line.replace('Pmanuclatu','Pmanuclatu  ')
                    outFile.write(PmLine)
       	        elif 'Ppolionotu' in line:                   
       	       	    PpLine = line.replace('Ppolionotu','Ppolionotu  ')
                    outFile.write(PpLine)
       	        elif 'Transcript' in line:                   
       	            transLine = line.replace('Transcript','Transcript  ')
                    outFile.write(transLine)
                
                else:
                    outFile.write(line)
