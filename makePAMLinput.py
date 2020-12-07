import os
from sequenceAnalyzer import FastAreader


clusterDic = {}
transcriptDic = {}
with open('Grouped_clusters.tsv','r') as f:
    for line in f:
        sp = line.strip().split('\t')
        clusterDic[sp[0]] = []
        for i in sp[1:]:
            clusterDic[sp[0]].append(i)
            transcriptDic[i] = ''

for i in ['P_eremicus','P_leucopus','P_polionotus','P_manuclatus']:
    myReaderInGenes = FastAreader('{0}/reconstructed_CDS.fa'.format(i))
    for header, sequence in myReaderInGenes.readFasta():
        if header in transcriptDic:
            if len(sequence) % 3 != 0:
                remainder = len(sequence) % 3
                addString = 'N'*(3-remainder)
                transcriptDic[header] = sequence + addString
            else:
                transcriptDic[header] = sequence
            if len(transcriptDic[header]) % 3 != 0:
                print(len(transcriptDic[header]),header)

os.system('mkdir selection_analysis')   
for cluster in clusterDic:
    if str(cluster) == '2':
        continue 
    os.system('mkdir selection_analysis/cluster_{0}'.format(str(cluster)))
    PATH = 'selection_analysis/cluster_{0}'.format(str(cluster))
    print(len(clusterDic[cluster]))
    stackDic = {'Transcript':False,'Pleucopus':False,'Ppolionotus':False,'Pmanuclatus':False}
    with open('{0}/seqs.fa'.format(PATH),'w') as f:
       	with open('{0}/cluster_log.txt'.format(PATH),'w') as f2:

            for header in clusterDic[cluster]:
                if 'Transcript' not in header:
                    species = header.split('_')[0] +  header.split('_')[1]
                else:
                    species = header.split('_')[0]
                if stackDic[species] == False:
                    f.write('>{0}\n{1}\n'.format(species,transcriptDic[header]))
                    stackDic[species] = True
                f2.write('{0}\t'.format(header))
    os.system('mkdir {0}/prePHY'.format(PATH))
    #os.system('rm -e  {0}/prePHY/*.phy'.format(PATH))
        
    os.system('mafft --phylipout {0}/seqs.fa > {0}/prePHY/seqs_msa.phylip'.format(PATH))
    print('cleaning phylip')
    currentPath = os.getcwd()
    os.system('rm -r {0}/{1}/prePHY/Alignment_Assessment'.format(currentPath,PATH))
   # os.system('rm -r {0}/{1}/prePHY/Output_Refinement'.format(currentPath,PATH))

    os.system('python2.7 Alignment_Assessment_v2.py {0}/prePHY {0}/prePHY'.format(PATH))
    os.system('python2.7 Alignment_Refiner_v2.py {0}/{1}/prePHY {0}/{1}/prePHY/Alignment_Assessment/Master_Alignment_Assessment.txt'.format(currentPath,PATH))
    os.system('cp {1}/prePHY/Output_Refinement/seqs_msa.phy {1}/'.format(currentPath,PATH))
    os.chdir(PATH)
    os.system('iqtree -redo -m MFP -s seqs_msa.phy')
    os.chdir('../..')
      

