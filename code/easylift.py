import os
import sys
import time
import argparse
import subprocess
import pandas as pd

start = time.time()
### flags parser
parser = argparse.ArgumentParser(description='easylift')
parser.add_argument('--lift', type=str, default='hg19tohg38')
parser.add_argument('--chr_col', type=str, default='CHR')
parser.add_argument('--pos_col', type=str, default='POS')
parser.add_argument('--file_in', type=str, default='./example/df_hg19.txt')
parser.add_argument('--file_out', type=str, default='./example/df_hg19_lifted_to_hg38.txt')
args = parser.parse_args()

lift = args.lift
chr_col = args.chr_col; pos_col = args.pos_col
file_in = args.file_in; file_out = args.file_out

# # default setting
# lift = 'hg19tohg38'
# chr_col = 'CHR'
# pos_col = 'POS'
# file_in = './example/df_hg19.txt'
# file_out = './example/df_hg19_lifted_to_hg38.txt'

print('setting:')
print('lift: '+ lift)
print('chr_col: '+ chr_col); print('pos_col: '+ pos_col)
print('file_in: '+ file_in); print('file_out: '+ file_out)
print('')

# liftover dict
file_map = {'hg19tohg38': './liftover/hg19ToHg38.over.chain.gz', 'hg38tohg19': './liftover/hg38ToHg19.over.chain.gz'}
# id for temp files
temp_id = hash(file_in)
temp_id = str(temp_id+sys.maxsize) if temp_id<0 else str(temp_id)
# read input
if file_in.endswith('.gz'): df = pd.read_csv(file_in, compression='gzip', sep='\t', low_memory=False)
else: df = pd.read_csv(file_in, sep='\t')

df.replace(23, 'X', inplace=True) # chr23 to chrX
df.replace(24, 'Y', inplace=True)
df = df.astype({pos_col: 'Int64'}, errors='ignore') # value not int would convert to NA 
df['id'] = df.index

# a option for me to test: when not snp are lifted, if break work.
# df[chr_col] = 23

# make bed
bed = df[[chr_col, pos_col, 'id']].copy()
bed['end'] = bed[pos_col] + 1
bed[chr_col] = 'chr' + bed[chr_col].astype('string')
bed = bed[[chr_col, pos_col, 'end', 'id']]
bed.to_csv('temp/'+temp_id+'.bed', sep='\t', index=False, header = False)

# liftover
liftover_command = f'code/liftOver temp/{temp_id}.bed {file_map[lift]} temp/{temp_id}.map temp/{temp_id}.unmap'
subprocess.Popen(liftover_command, shell=True).wait()

# add new pos
try:
    df_map = pd.read_csv(f'temp/{temp_id}.map', sep='\t', header=None)[[1,3]]
except pd.errors.EmptyDataError:
    print("Error: No SNP can be lifted. Please check your input.")
    sys.exit()

df_map.rename(columns = {1:pos_col, 3:'id'}, inplace = True)
df.rename(columns = {pos_col:pos_col+'_old'}, inplace = True)
res = df.merge(df_map, how='left').drop('id', axis=1) 
res = res.astype({pos_col: 'Int64'}, errors='ignore')

# save
res.to_csv(file_out, sep='\t', index=False)
print(f'deleting temporary files...')
rm_command = f'rm -rf temp/{temp_id}*'
subprocess.Popen(rm_command, shell=True).wait()
print(f'{df_map.shape[0]} snp are lifted successfully')
print(f'done!')
end = time.time()
print (f'spend {round(end-start, 2)} sec')