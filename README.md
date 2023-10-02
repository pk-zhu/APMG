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

### 首先，需要通过repeatmasker对基因组进行串联区域的注释


### 其次，使用我们提供的python脚本删除被注释为transponser的区间，得到轻量版的基因组文件
```
nohup python -u gigagr.py -g genome.fa -f annotation.gff3 -type Transposon -o clean_genome.fa -n 12 &

#注意这里-n指的是运行脚本的核心数，一个核心处理一条scarfold，不需要太多线程，因为这不能使脚本运行速度加快。
#因大基因组通常包括几十亿条transposons，每处理100000条序列将打印一次报告，使您确认程序在正常运行。若您需要删除的记录较少，可以在脚本中降低报告的记录数量。
```
### 接下来，我基于cds序列对轻量基因组进行重新注释

#### 首先安装gamp
```
./configure --prefix=/home/usr/software/gmap --with-gmapdb=/home/usr/software/gmap
make && make install
```
#### 建立索引
```
gmap_build -d clean_genome clean_genome.fa
```
#### 比对
```
gmap -d clean_genome -f gff3_gene cds.fa -B 4 -t 28 >out1.gff3 &
```
#### 注释结果初步处理
```
python tidy_gff.py -i out1.gff3 -o out2.gff3
```
#### 质控gff3tool
```
mkdir gff_qc
gff3_QC -g out2.gff3 -f clean_genome.fa \
  -o ./gff_qc/sample.qc \
  -s ./gff_qc/stat.txt
gff3_fix -qc_r ./sample.qc -g out2.gff3 -og out3.gff3
```
#### gff3重命名和排序
```
python rename_gff.py -g out3.gff3 -c bed.txt -p out3
gff3_sort -g out3.rename.gff3 -og result.gff3
```
### 最后，使用Busco进行质量检查
```
busco --cpu 10 \
	-l busco_downloads/embryophyta_odb10 \
	-m genome --force -o busco \
	-i genome.fa \
	--offline
```
### 结果还行的话，就把注释后的cds序列提取出来，blast回原cds序列，99%以上的原cds序列应该都能对应新cds序列。

# 再说一句

有时间的话，接下来我会推出完整的snakemake工作流，并使用两三个物种的转录组数据，分别比对轻量基因组和原始基因组，观察**基因组轻量化对比对结果的影响**及**这种影响是否受物种间转座子长度差异作用**，以判断这种方法能否在转录组中应用。
