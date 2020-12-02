# Peromyscus-reproductive-convergence

## Phylogenetic inference
```
mafft mitochondrial_genomes.fa > mitochondrial_genomes_msa.fa
iqtree -redo -m MFP -s Peromyscus_Mitochondria_msa.fa 
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
mkdir temp
ln -rs GCF_000500345.1_Pman_1.0_cds_from_genomic.fna temp/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna
mkdir variants
samtools mpileup -uf temp/GCF_000500345.1_Pman_1.0_cds_from_genomic.fna *.bam > variants/raw_calls_P_polionotus.bcf
```
#### Variant calls
```
bcftools call -m variants/raw_calls_P_polionotus.bcf > variants/calls_P_polionotus.vcf
```

#### Constructing variant aware transcripts
```
python reconstruct_variant_cds.py
```

## Finding homologous transcripts between species

#### findOverlaps
Requires silexx (see https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-116) and blastn (see https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) as dependencies.


Performs an all vs all blast between transcripts in each species and clusters sequences with > 80% identity and > 80% alignment block.

```
python findOverlaps.py
```

## Making PAML input data


