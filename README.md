## A pipeline for masking a genome, starting from a fasta file or a gff file.

> ***By Pengkai Zhu***
> 
> ***Institution: Fujian Agriculture and Forestry University***
> 
>  ***Email: pkzhu222@gmail.com***
> 
>  ***Cite:***
>  
>


------

Ultra-Large genomes often strain computational resources during alignment or indexing, leading to analysis issues. However, some analyses focus on specific genome regions, like exons, introns, UTRs, and key loci, which may represent only 50% or less of the total genome size. Aligning the entire genome results in unnecessary resource usage. Therefore, I propose masking repetitive regions to shrink the reference genome, making the analysis more efficient and lowering resource demands for large genome alignments.
## 1.Software
1. [Red](https://anaconda.org/bioconda/red/files)
2. [BEDOPS](https://bedops.readthedocs.io/en/latest/index.html)
3. [bedtools2](https://github.com/arq5x/bedtools2)

## 2. Workflow (begin with a fasta file)
### 1. Obtaining repetitive regions from Red
#### 1. Creating Directory to Store Output
```
mkdir -p OUTPUT
```
#### 2. Predicting Repetitive Sequences from genome
```
Red -gnm /path/to/genome/dir/ -msk ./OUTPUT -rpt ./OUTPUT
```
#### 3. Converting Soft-Masked Genome to Hard-Masked Genome
```
awk '!/>/ {gsub(/[atcg]/,"N")} 1' ./OUTPUT/genome.msk > ./OUTPUT/genome.hardmasked.fa
```

## 3. Workflow (begin with a fasta file and a repeats anotation file)
### 1. Convert gfffile to bedfile
```
gff2bed < LTR.gff3 > LTR.bed
```
### 2. Masked genome.fa
```
bedtools maskfasta -fi genome.fa -bed mask.bed -fo genome.hardmasked.fasta
```
