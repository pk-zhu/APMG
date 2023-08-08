# ULGR: Ultra-Large-Genome-Reductions
A pipeline for optimizing ultra-large genome analysis by removing transposons or other repetitive elements.

大于10GB的基因组在比对时或建立索引时常常占用大量的计算资源，对计算机造成负担，并导致意外的分析失败。而在一些分析中，比如转录组比对（只关注转录本）或GWAS（通常仅关注外显子区比较重要的位点），而这些区域及其少部份基因间区的部分可能仅占基因组整体大小的50%或更低。因此基因组冗余部分的比对造成了大量不必要的占用，这里我提出了一种思路，即通过删除基因组中重复区域来减小基因组大小，以使分析流程轻量化，降低大基因比对的计算资源门槛。

# 首先，需要通过repeatmasker对基因组进行串联区域的注释

# 其次，使用我们提供的perl脚本删除被注释为transponser的区间，得到轻量版的基因组文件

# 接下来，我使用两种方法基于cds序列对轻量基因组进行重新注释

## 方法一：基于haisat2和stringtie

### 然后，将CDS序列比对轻量版参考基因组

### 最后，使用stringtie生成注释文件

## 方法二：基于blast（TBtools）


# 再说一句

有时间的话，接下来我会推出完整的snakemake工作流，并使用两三个物种的转录组数据，分别比对轻量基因组和原始基因组，观察

### 基因组轻量化对比对结果的影响如何

及

### 这种影响是否受物种间不同转座子长度影响

以判断这种方法能否在转录组中应用
