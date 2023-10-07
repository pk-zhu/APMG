# ULGGR (Ultra-Large Gymnosperm Genomes Reduction)
## A pipeline for optimizing large genome analysis by removing transposons or other repetitive elements.

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

Large genomes often strain computational resources during alignment or indexing, leading to analysis issues. However, some analyses focus on specific genome regions, like exons, introns, UTRs, and key loci, which may represent only 50% or less of the total genome size. Aligning the entire genome results in unnecessary resource usage. Therefore, I propose removing repetitive regions to shrink the reference genome, making the analysis more efficient and lowering resource demands for large genome alignments.
## 1.Software
1. [BUSCO](https://busco.ezlab.org/)
2. [RepeatMasker, RepeatModeler](http://www.repeatmasker.org/)
3. [Gmap](http://research-pub.gene.com/gmap/src/)
4. [gff3tool](https://github.com/NAL-i5K/GFF3toolkit)
5. [GFFUtils](https://github.com/fls-bioinformatics-core/GFFUtils)
6. [TransDecoder](https://github.com/TransDecoder/TransDecoder)
7. [NCBI BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi)
## 2.Workflow
### 1.Obtaining repetitive regions
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
# The output file contains duplicate region annotations, and it is referred to as 'anntation.gff3' below.
```

### 2.Using the Python script we provide, remove intervals annotated as "Transposon" to obtain a lightweight version of the genome file.
```
nohup python -u ulggr.py -g genome.fa -f annotation.gff3 -type Transposon -o lw_genome.fa -n 12 &

# -n refers to the number of threads to run the script. One core per scaffold is sufficient. you don't need many threads as it won't significantly speed up the script.
# Since large genomes typically contain billions of transposons, a report will be printed every 100,000 sequences processed to confirm that the program is running smoothly. If you need to remove fewer records, you can increase the number of records reported in the ulggr.py.
```
### 3.Re-annotate the Lightweight Genome Based on CDS Sequences

#### install gamp (If already installed, please skip)
```
cd /home/usr/software/
wget -c http://research-pub.gene.com/gmap/src/gmap-gsnap-2023-07-20.tar.gz
tar -zxvfp gmap-gsnap-2023-07-20.tar.gz
./configure --prefix=/home/usr/software/gmap --with-gmapdb=/home/usr/software/gmap
make && make install
```
#### build index
```
gmap_build -d clean_genome lw_genome.fa
```
#### mapping
```
gmap -d clean_genome -f gff3_gene cds.fa -B 4 -t 28 >out1.gff3 &
```
### 3.Processing the Annotation Results

#### Quality Control
```
gff3_QC -g out2.gff3 -f lw_genome.fa \
  -o sample.qc \
  -s stat.txt
gff3_fix -qc_r sample.qc -g out2.gff3 -og out3.gff3
```
#### Renaming and Sorting
```
python rename_gff.py -g out3.gff3 -c bed.txt -p out3
# The script used here is from GFFUtils. For convenience, i copy this script separately here. When using it, please cite orginal site.

gff3_sort -g out3.rename.gff3 -og result.gff3
```
#### Refine the annotation
```
python tidy_gff.py -i out1.gff3 -o out2.gff3
```
### 4.Homology Assessment
```
busco --cpu 10 \
	-l busco_downloads/embryophyta_odb10 \
	-m genome --force -o busco \
	-i lw_genome.fa \
	--offline

# lw_genome.fa should have a higher BUSCO value.
```
### If the results are satisfactory, extract the annotated CDS sequences, and then perform a BLAST search against the original CDS sequences (Undemonstrated).
### More than 99% of the original CDS sequences should correspond to the new CDS sequences.
