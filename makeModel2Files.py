import glob

for clusterDir in glob.glob('cluster*'):
    with open('{0}/seqs_msa2_model2.phylip'.format(clusterDir),'w') as outFile:
        with open('{0}/seqs_msa2.phylip'.format(clusterDir),'r') as f:
            for line in f:
                if 'Ppolionotu' in line:                   
       	            PpLine = line.replace('Ppolionotu','Ppolionotu#1')
                    outFile.write(PpLine)
                elif 'Transcript' in line:                   
       	            transLine = line.replace('Transcript','Transcript#1')
                    outFile.write(transLine)
                else:
                    outFile.write(line)
    with open('{0}/seqs_msa.phy_model2.treefile'.format(clusterDir),'w') as outFile:
        with open('{0}/seqs_msa.phy.treefile'.format(clusterDir),'r') as f:
            for line in f:
                outFile.write(line.replace('Ppolionotu','Ppolionotu#1').replace('Transcript','Transcript#1'))

