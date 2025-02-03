# USAGE: bash count_num_of_lip-sol_in_gro_file.sh FILENAME.gro
# AIM: to update number of solvent and lipid types in topol.top
# NOTE: Modify lines 12,13 as required to include specific solvent/lipid names. Lipid names must be accompanied by unique particle names. 


# Taking gro file as 1st argument
file=$1
   
# The below returns all lines containing the specified strings separated by |. 
# Please check the number of spaces in the strings (matching those in gro file).

egrep -E 'SOL     OW|CA      CA|NA      NA|CL      CL' $file > solvent_lines.txt
egrep -E 'POPE    C1|POPG    C1|CDL2    C1|REMP   CB1|PMB1    C1' $file > lipid_lines.txt

#returns columns 14-15 in new file. syntax: cut -c 1-5,10
cut -c 6-9 lipid_lines.txt > lipid_lines_resnames.txt
cut -c 6-9 solvent_lines.txt > solvent_lines_resnames.txt

echo " "
#counts number of unique instances in a column
awk '{print $1}' lipid_lines_resnames.txt | uniq -c
awk '{print $1}' solvent_lines_resnames.txt | uniq -c

rm lipid_lines.txt
rm lipid_lines_resnames.txt
rm solvent_lines.txt
rm solvent_lines_resnames.txt
