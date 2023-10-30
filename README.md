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
1. [Tandem Repeats Finder](https://github.com/Benson-Genomics-Lab/TRF)
2. [RepeatMasker, RepeatModeler](http://www.repeatmasker.org/)
3. [BEDOPS](https://bedops.readthedocs.io/en/latest/index.html)
4. [bedtools2](https://github.com/arq5x/bedtools2)

## 2.Workflow (begin with a fasta file)
### 1.Obtaining repetitive regions from RepeatMasker
#### Obtaining Repetitive Sequences from an Existing Database
```
famdb.py -i RepeatMaskerLib.h5 families \
	-f embl \
	-a \
	-d Viridiplantae \
	> Viridiplantae_ad.embl
util/buildRMLibFromEMBL.pl Viridiplantae_ad.embl > Viridiplantae_ad.fa

# Obtaining Viridiplantae Repetitive Sequences, using the RepBase database
# Alternatively, you can use https://www.dfam.org/releases/Dfam_3.7/families/Dfam.hmm.gz
```
#### Predicting Repetitive Sequences from genome.fa
```
BuildDatabase -name GDB \
	-engine ncbi \
	genome.fa
RepeatModeler -engine ncbi \
	-pa 28 \
	-database GDB \
	-LTRStruct
```
#### RepeatMasker
```
cat GDB-families.fa Viridiplantae_ad.fa > repeat_db.fa
RepeatMasker -xsmall \
	-gff \
	-html \
	-lib repeat_db.fa \
	-pa 28 \
	genome.fa
EDTA.pl --genome female.fa \
	--species others \
	--sensitive 1 --anno 1 --evaluate 1 \
	--threads 30
# The result contains maskedgenome file "masked1.fa"
```
### 2.Obtaining repetitive regions from Tandem Repeats Finder
```
 trf genome.fa 2 7 7 80 10 50 500 -f -d -m
 # The result contains maskedgenome file "masked2.fa"
```
### 3.Generate bedfiles of masked ranges from fasta
```
python fastaN2bed.py masked1.fa > masked1.bed
python fastaN2bed.py masked1.fa > masked2.bed
# The script is in the current repository
```
### 4.merge bedfiles
```
cat masked1.bed masked2.bed > masked.bed
bedtools merge -i masked.bed > mask.bed
```
### 5.Remasked genome.fa
```
bedtools maskfasta -fi genome.fa -bed mask.bed -fo genome.hardmasked.fasta
```

## 3.Workflow (begin with a fasta file and a LTR anotation file)
### 1.Convert gfffile to bedfile
```
gff2bed < LTR.gff3 > LTR.bed
```
### 2.Masked genome.fa
```
bedtools maskfasta -fi genome.fa -bed mask.bed -fo genome.hardmasked.fasta
```
