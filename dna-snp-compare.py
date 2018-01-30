#!/usr/bin/env python
#
# Compares SNPs between DNA service RAW files 
# test with Ancestry.com and 23andMe
#
# * reports total number of SNPs
# * report total number of "custom" SNPs (23andMe i*)
# * reports number of matching SNPs between two files
#

import sys
import re

file1_snps = []
file2_snps = []
matched_snps = []

file1_regular_snps = 0
file2_regular_snps = 0

file1_custom_snps = 0
file2_custom_snps = 0

matches = 0
uniq = 0

file1 = open(sys.argv[1], 'r') 
file2 = open(sys.argv[2], 'r') 

# make sure two file names were provided as arguments
def file_check():
    if ( len(sys.argv) == 3 ):
        pass
    else:
        print(sys.argv[0], "<file1> <file2>")

def data_suck():
    global file1_regular_snps
    global file1_snps
    global file2_regular_snps
    global file2_custom_snps
    global file1_snps_sort
    global file2_snps_sort

    for line in file1:
        if re.match("^r", line):
            file1_regular_snps += 1
            file1_snps.append(line.split()[:1])
        if re.match("^i", line):
            file1_custom_snps += 1

    for line in file2:
        if re.match("^r", line):
            file2_regular_snps += 1
            file2_snps.append(line.split()[:1])
        if re.match("^i", line):
            file2_custom_snps += 1

    file1_snps_sort = sorted(file1_snps)
    file2_snps_sort = sorted(file2_snps)

def print_summary():

    print()
    print("file:\t\t", sys.argv[1])
    print("total_snps:\t", file1_regular_snps + file1_custom_snps)
    print("regular_snps:\t", file1_regular_snps)
    print("custom_snps:\t", file1_custom_snps)
    print()

    print()
    print("file:\t\t", sys.argv[2])
    print("total_snps:\t", file2_regular_snps + file2_custom_snps)
    print("regular_snps:\t", file2_regular_snps)
    print("custom_snps:\t", file2_custom_snps)
    print()

    file1.close()
    file2.close()

# limit max range to search for SNP for faster results
# snp * 2
# +1000 of initial snp
def snp_range_limit(snp):

    if ( snp <= len(file2_snps_sort) ):
        max_range = 0
        max_range = snp * 3
        max_range += 1000
    else:
        max_range = len(file2_snps_sort)
    
    return(max_range)
    
# search for matching SNP between files
def snp_match():
    last_match_idx = 0
    matches = 0

    for snp in range( 0, len(file1_snps_sort) ):

        snp_max = snp_range_limit(snp)

        for snp2 in range( last_match_idx, snp_max ):

            if ( file1_snps_sort[snp] == file2_snps_sort[snp2] ): 
                matched_snps.append(file1_snps_sort[snp])
                matches += 1 
                last_match_idx = snp2

                # print out every 5,000 SNP matches
                if ( matches % 1000 == 0 ):
                    print("snp:", snp, "snp2:", snp2, "matches:", matches)
                break

# main 
file_check()
data_suck()
print_summary()
snp_match()
