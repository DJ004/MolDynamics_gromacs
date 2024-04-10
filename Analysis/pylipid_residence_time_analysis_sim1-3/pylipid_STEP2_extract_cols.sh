#!/bin/bash

# Goal: Extract 10th column i.e. residence times from 3 simulation replicate files 
#       and provide a file in the following format:
#
# res_num  residence_time_r1  residence_time_r2  residence_time_r3 (µs)
#    1          0.5                 0.35                0.6
#    2          0.0                 0.1                 0.05
#    .           .                   .                   .
#    .           .                   .                   .

# Script usage:
# bash pylipid_extract_cols.sh

# Repeat for each lipid
# cd into parent dir containing pylipid_r1, .._r2, .._r3, .._avg

RESTIME_XVG_FILENAME="pylipid_chol.xvg"
LIPID="chol"

mkdir pylipid_avg

# Specify number of simulation replicates in the for loop
# NUM_OF_REPS=3 by default
for i in {1..3};
do
	awk '{print $10}'  pylipid_r${i}/$RESTIME_XVG_FILENAME > pylipid_avg/${LIPID}_restime_r${i}_col2.xvg
	awk '{print $2+1}' pylipid_r${i}/$RESTIME_XVG_FILENAME > pylipid_avg/${LIPID}_restime_r${i}_col1.xvg
	paste -d'\t' pylipid_avg/${LIPID}_restime_r${i}_col1.xvg pylipid_avg/${LIPID}_restime_r${i}_col2.xvg > pylipid_avg/${LIPID}_restime_${i}.xvg
done
paste -d'\t' pylipid_avg/${LIPID}_restime_r{1..3}_col2.xvg > pylipid_avg/${LIPID}_restime_all_col2.xvg
paste -d'\t' pylipid_avg/${LIPID}_restime_r1_col1.xvg pylipid_avg/${LIPID}_restime_all_col2.xvg > pylipid_avg/${LIPID}_resnum_restime_allreps.xvg

cd pylipid_avg/

# Remove intermediate files
rm ${LIPID}_restime_r{1..3}_col*.xvg ${LIPID}_restime_all_col2.xvg
