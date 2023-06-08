
# About easylift
`easylift` is a tool to convert genomic position of a gwas summary from one build to another (hg19 and hg38).

# Why easylift
I make minor efforts to omit some laborious steps (i.e., prepare bed input, lift, and then map back to your files) in the use of `LiftOver`.
With `easylift`, you can use a (tab separated) file (e.g., gwas summary) as input and obtain an output with a position field. 

# Requirements 
- `Linux` 
- `LiftOver`
- `Python3` (>=3.8) with `pandas`, `argparse`, `os`, `sys`, `time`, `subprocess`  
  
Versions I used are in bracket.

# Getting Started
Clone this repository via the commands:
```  
git clone https://github.com/zhanghaoyang0/easylift.git
cd easylift
```

Once the above has completed, you can try to lift to new pos field by specifying: 
`--lift` hg19tohg38 or hg38tohg19, default is hg19tohg38   
`--chr_col` field name of CHR, default is CHR   
`--pos_col` field name of POS, default is POS   
`--file_in` tab[\t] separated input file, gzip (file_in end with '.gz') input can also be recognized  
`--file_out` output file  

Two examples (hg19tohg38 and hg38tohg19):

```
python ./code/easylift.py \
--lift hg19tohg38 \
--chr_col CHR --pos_col POS \
--file_in ./example/df_hg19.txt \
--file_out ./example/df_hg19_lifted_to_hg38.txt

python ./code/easylift.py \
--lift hg38tohg19 \
--chr_col chrom --pos_col pos \
--file_in ./example/df_hg38.txt \
--file_out ./example/df_hg38_lifted_to_hg19.txt
```

gzip (file_in end with '.gz') input can be recognized: 
```
python ./code/easylift.py \
--lift hg19tohg38 \
--chr_col CHR --pos_col POS \
--file_in ./example/df_hg19.txt.gz \
--file_out ./example/df_hg19_lifted_to_hg38.txt
```

The input file is like:
```
CHR     POS     A1      A2      FRQ     BETA    SE      P
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035
12      104289454       T       C       0.534   0.0085  0.0088  0.3322
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256
4       163471758       T       C       0.612   0.0119  0.0094  0.2057
```

If `easylift` is running, you will see:
```
setting:
lift: hg19tohg38
chr_col: CHR
pos_col: POS
file_in: ./example/df_hg19.txt
file_out: ./example/df_hg19_lifted_to_hg38.txt

Reading liftover chains
Mapping coordinates
deleting temporary files...
2000 snp are lifted successfully
done!
spend 0.13 sec
```

The output file is like:
```
CHR     POS_old A1      A2      FRQ     BETA    SE      P       POS
2       48543917        A       G       0.4673  0.0045  0.0088  0.6101  48316778
5       87461867        A       G       0.7151  0.0166  0.0096  0.08397 88166050
14      98165673        T       C       0.1222  -0.0325 0.014   0.02035 97699336
12      104289454       T       C       0.534   0.0085  0.0088  0.3322  103895676
11      26254654        T       C       0.0765  0.0338  0.0167  0.04256 26233107
4       163471758       T       C       0.612   0.0119  0.0094  0.2057  162550606
```

# Feedback and comments
Add an issue or send email to zhanghaoyang0@hotmail.com