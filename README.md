# GigaGR (GigaGenomeReduction)
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

大基因组在比对或建立索引时常常占用大量的计算资源，对计算机造成负担，并导致意外的分析失败。而在一些分析中并不关注基因组所有的区域，比如转录组比对（只关注转录本）或GWAS、eQTL（在大量的SNP/INDEL中，通常仅关注外显子区比较重要的位点），而关键的区域（外显子、内含子、UTR等）及其少部份基因间区的部分可能仅占基因组整体大小的50%或更低。因此基因组冗余部分的比对造成了大量不必要的占用，这里我提出了一种思路，即通过删除基因组中重复区域来减小参考基因组大小，以使分析流程轻量化，降低大基因组比对的计算资源门槛。

### 首先，需要通过repeatmasker对基因组进行串联区域的注释


### 其次，使用我们提供的python脚本删除被注释为transponser的区间，得到轻量版的基因组文件
```
nohup python -u gigagr.py -g genome.fa -f annotation.gff3 -type Transposon -o clean_genome.fa -n 12 &

#注意这里-n指的是运行脚本的核心数，一个核心处理一条scarfold，不需要太多线程，因为这不能使脚本运行速度加快。
#因大基因组通常包括几十亿条transposons，每处理100000条序列将打印一次报告，使您确认程序在正常运行。若您需要删除的记录较少，可以在脚本中降低报告的记录数量。
```
### 接下来，我基于cds序列对轻量基因组进行重新注释
```
#首先安装gamp
./configure --prefix=/home/usr/software/gmap --with-gmapdb=/home/usr/software/gmap
make
make install
#建立索引
gmap_build -d clean_genome clean_genome.fa
#比对
gmap -d clean_genome -f gff3_gene cds.fa -B 4 -t 28 >out1.gff3 &
#注释结果初步处理
python tidy_gff.py -i out1.gff3 -o out2.gff3
#质控gff3tool
mkdir gff_qc
gff3_QC -g out2.gff3 -f clean_genome.fa -o ./gff_qc/sample.qc -s ./gff_qc/stat.txt
gff3_fix -qc_r ./sample.qc -g out2.gff3 -og out3.gff3
#重命名和排序
python rename_gff.py -g out3.gff3 -c bed.txt -p out3
gff3_sort -g out3.rename.gff3 -og result.gff3
```
### 最后，一般把注释后的cds序列提取出来，blast回原cds序列，99%以上的原cds序列应该都能对应新cds序列。

# 再说一句

有时间的话，接下来我会推出完整的snakemake工作流，并使用两三个物种的转录组数据，分别比对轻量基因组和原始基因组，观察**基因组轻量化对比对结果的影响**及**这种影响是否受物种间转座子长度差异作用**，以判断这种方法能否在转录组中应用。
