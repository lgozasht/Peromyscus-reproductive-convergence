# Peromyscus-reproductive-genetic-differences
I developed a pipeline for detecting shared signatures of selection between two monogomous Peromyscus species, P. eremecus and P. polionotus, relatice two their respective polygamous sister species, P. maniculatus and P. leucopus.

## Phylogenetic inference
I used MAFFT (see https://mafft.cbrc.jp/alignment/software/) to generate a multiple sequence alignment from 15 concatenated orthologous genes of P. eremecus, P. polionotus, P. maniculatus and P. leucopus with the addition of Mus musculus and Rattus norvegicus as outgroups. I used IQ-TREE (see http://www.iqtree.org/) to infer the phylogeny thereafter.

```
mafft concatenated__genes.fa > concatenated__genes_msa.fa
iqtree -redo -m MFP -s concatenated__genes_msa.f
```

## Example scripts used for obtaining sequence data from JGI

#### Retrieving raw data
```
python downloadJGI.py
```

#### Converting sff to fastq
```
python convertsff.py
```

## Example pipeline for reconstructing a variant aware cds 

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
Reconstructs cds and replaces the reference allele at heterozygous sites where the alternate allele exhibits a higher frequency.

```
python reconstruct_variant_cds.py
```

## Finding homologous transcripts between species

#### findOverlaps
Requires silexx (see https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-116) and blastn (see https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) as dependencies.

Performs an all vs all blast between transcripts in each species and clusters sequences with > 80% identity and > 80% alignment block.

First, open findOverlaps.py, scroll to the bottom of the script, and uncomment the blast function call. Then, run the command,
```
python findOverlaps.py
```
You should now have files for each pairwise comparison containing overlaps between homologous transcripts. You'll want to combine all overlaps into one file using the command,
```
cat file1 file2 file3 fileN > all_hits.out
```

Then, go back in the script, comment out the blast function call, and uncomment the other two function calls. Run the command,
```
python findOverlaps.py
```
and you should now have a directory callded "selection_analysis" that harbors directories for each cluster containing its respective codeml input data. 


## Making codeml input data and running codeml

#### makePAMLinput
PAML's codeml requires a multiple sequence alignment corresponding phylogeny as input. However, the functionality and accuracy of codeml is impaired by indels and missing data. Thus, after producing an msa and tree for each transcript using MAFFT and IQ-Tree respectively, I cleaned my alignments using a modified version of Alignment_Refiner_v2 (see https://github.com/dportik/Alignment_Refiner) which also requires trimmal as a dependency (see http://trimal.cgenomics.org/).

```
python makePAMLinput.py
```

#### correctPhylip
Ensures compatability of phylip format with PAML

```
python correctPhylip.py
```

#### makeModel2Files
Adds annotations to phylip and tree input files for compatability with PAML model=2 

```
python makeModel2Files.py
```

#### runPAML
Runs PAML's codeml. To specify which model to use, open the file and edit the "paml_control_model", which can be either "paml_control_model0" or "paml_control_model2". Both control files are available in this repository.

```
python runPAML.py
```

## Reference
* Landen Gozashti, Russell Corbett-Detig and Scott W. Roy. "Evolutionary rates of testes-expressed genes differ in monogamous and promiscuous Peromyscus species", bioRxiv [pre-print](https://www.biorxiv.org/content/10.1101/2021.04.21.440792v7) 2021.
