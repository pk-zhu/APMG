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
nohup python -u gigagr.py -g genome.fa -f annotation.gff3 -type Transposon -o output.fa -n 40
```
### 接下来，我使用两种方法基于cds序列对轻量基因组进行重新注释

##### 方法一：基于haisat2和stringtie
```shell
#建立基因组索引
hisat2-build -p 28 genome.fa genome
#将CDS序列比对轻量版参考基因组
hisat2 -p 28 -x genome --dta -U reads.fq | samtools sort -@ 28 > reads.bam
#stringtie注释
stringtie -p 28 -o stringtie.gtf reads.bam
```

##### 方法二：基于blast（TBtools）


# 再说一句

有时间的话，接下来我会推出完整的snakemake工作流，并使用两三个物种的转录组数据，分别比对轻量基因组和原始基因组，观察**基因组轻量化对比对结果的影响**及**这种影响是否受物种间转座子长度差异作用**，以判断这种方法能否在转录组中应用。
