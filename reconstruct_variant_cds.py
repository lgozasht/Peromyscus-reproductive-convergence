from Bio import SeqIO
import os

cdsDic = {}
indexDic = {}
with open('temp/variants/calls_P_polionotus.vcf','r') as f:
    for line in f:
        if '#' in line:
            pass
        else:
            sp = line.split('\t')
            refCDS = sp[0].strip()
            if refCDS not in cdsDic:
                indexDic[refCDS] = []
                cdsDic[refCDS] = []
            indexDic[refCDS].append(int(sp[1]))
            if '.' in sp[4]:
                cdsDic[refCDS].append(sp[3].strip())
            else:
       	        cdsDic[refCDS].append(sp[4].strip())

refDic = {}
fasta_sequences = SeqIO.parse(open('temp/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna'),'fasta') 
for fasta in fasta_sequences:
    header, sequence = fasta.id, str(fasta.seq)
    refDic[header.split(' ')[0]] = sequence

count = 0
os.system('rm -r stats_tmp.tsv')
for c in refDic:
    if c in cdsDic:
        count += 1
        with open('stats_tmp.tsv','a') as f:

             f.write('{0}\t{1}\t{2}\t{3}\n'.format(c,len(cdsDic[c]),len(refDic[c]),float(len(cdsDic[c]))/float(len(refDic[c]))))
os.system("sort -t $'\t' -k4 -n stats_tmp.tsv > summary_stats.tsv")

with open('reconstructed_CDS.fa','w') as f:
    for c in cdsDic:
        k = 0
        sequence = ''
        for i in range(len(refDic[c])):
            if i + 1 in indexDic[c]:
                sequence = sequence + cdsDic[c][k]
                k += 1
            else:
                sequence = sequence + refDic[c][i]
                k = 0
        
        f.write('>{0}\n{1}\n'.format(c,sequence))
