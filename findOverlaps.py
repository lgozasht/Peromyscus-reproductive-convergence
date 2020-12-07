import os
import glob
from sequenceAnalyzer import FastAreader


def blast():
    stack = []
    for i in ['P_eremicus','P_leucopus','P_polionotus','P_manuclatus']:    
        os.system("makeblastdb -dbtype nucl -in {0}/reconstructed_CDS.fa -title trans -out {0}/transcriptDB".format(i))

    for i in ['P_eremicus','P_leucopus','P_polionotus','P_manuclatus']:
        for k in ['P_eremicus','P_leucopus','P_polionotus','P_manuclatus']:
            comp = [i,k]
            print(comp,sorted(comp),stack)
            if sorted(comp) not in stack and i != k:
                os.system("blastn -db {0}/transcriptDB -query {1}/reconstructed_CDS.fa -outfmt 6 -perc_identity 80 -out {0}_V_{1}.out".format(i,k))
                stack.append(sorted(comp))

    #####cat all blast output to one file called all_hits.out#####

def cluster():
    transcriptDic = {}
    for i in ['P_eremicus','P_leucopus','P_polionotus','P_manuclatus']:
        myReaderInGenes = FastAreader('{0}/reconstructed_CDS.fa'.format(i))
        for header, sequence in myReaderInGenes.readFasta():
            transcriptDic[header] = float(len(sequence))
    with open('all_hits.out.filtered','w') as outf:   
        with open('all_hits.out','r') as f:
       	    for line in f:
       	        sp = line.strip().split('\t')
       	        if float(sp[2]) > 90.0:
                    if float(sp[3]) > transcriptDic[sp[0].strip()]*.8 and float(sp[3]) > transcriptDic[sp[1].strip()]*.8:
                        outf.write(line)
    os.system("awk '{print $1\" \"$2}' all_hits.out.filtered > all_hits_IDs.out")
    # 181276 is the number of sequences upper bound
    os.system('silixx 181276 all_hits_IDs.out > clusters')
    

def findComparisons():
    clusterDic = {}
    with open('clusters','r') as f:
        for line in f:
            try:
                sp = line.strip().split('\t')
                if sp[0] not in clusterDic:
                    clusterDic[sp[0]] = [sp[1]]
                else:
                    clusterDic[sp[0]].append(sp[1])
            except IndexError:
                break
    count = 0
    #print(clusterDic)
    with open('Grouped_clusters.tsv','w') as f:
        for cluster in clusterDic:
            if len(clusterDic[cluster]) >= 4:
                clusterString = '\t'.join(clusterDic[cluster])
                if 'Transcript' in clusterString and 'P_leucopus' in clusterString and 'P_polionotus' in clusterString and 'P_manuclatus' in clusterString:
                    f.write('{0}\t{1}\n'.format(str(cluster),clusterString))
                    count += 1
                
    print(count)

"""

Call functions

"""
#blast()
#cluster()
#findComparisons()

