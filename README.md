# Peromyscus-reproductive-convergence

## Phylogenetic inference
```
mafft mitochondrial_genomes.fa > mitochondrial_genomes_msa.fa
qtree -redo -m MFP -s Peromyscus_Mitochondria_msa.fa 
```

## Reconstructing P. polionotus cds

#### Retrieving raw data
```
python downloadJGI.py
```

#### Converting sff to fastq
```
python convertsff.py
```

#### Obtaining reference CDS file
```
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/500/345/GCF_000500345.1_Pman_1.0/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna.gz
```

#### Indexing the reference
```
hisat2-build GCF_000500345.1_Pman_1.0_cds_from_genomic.fna GCF_000500345.1_Pman_1.0_cds
```

#### Aligning to the reference
```
hisat2 -x GCF_000500345.1_Pman_1.0_cds -U reads.fastq -S aln.sam
```

#### Filtering mapped reads
```
samtools view -F 0x04 -b aln.sam > aln.bam
```

#### Sorting bam files
```
samtools sort aln.bam > aln.sorted.bam
```

#### Pileup
```
ln -rs GCF_000500345.1_Pman_1.0_cds_from_genomic.fna temp/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna
samtools mpileup -uf temp/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna *.bam > variants/raw_calls_P_polionotus.bcf
```
#### Variant calls
```
bcftools call -m variants/raw_calls_P_polionotus.bcf > variants/calls_P_polionotus.vcf
```
