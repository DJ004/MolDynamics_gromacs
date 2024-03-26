# USAGE: bash count_num_of_lip-sol_in_gro_file.sh FILENAME.gro
# Use case: to update number of solvent and lipid types in topol.top
# Modify lines 13,14 as required to include your solvent/lipid names. Multi-particle molecules must be accompanied with unique particle names. 

#for i in {1..3} # number of repeats
#do
        # Taking gro file as 1st argument
        file=$1 

        # The below returns all lines containing the specified strings separated by |. 
        # Please check the number of spaces in the string (matching those in gro file) to obtain correct results.

        egrep -E '  W| CA| NA| CL' $file > solvent_lines.txt
        egrep -E 'POPC   PO4|POPE   PO4|POPG   PO4|CDL2  PO41|REMP   PO1|RAMP   PO1|OANT   PO1|' $file > lipid_lines.txt
        
        # The below 2 lines return columns 14-15 in new file. syntax: cut -c 1-5,10

        cut -c 6-9 lipid_lines.txt > lipid_lines_resnames.txt
        cut -c 14-15 solvent_lines.txt > solvent_lines_resnames.txt
        
        echo " "
        #echo "r${i}"
        #echo "-----"
        awk '{print $1}' lipid_lines_resnames.txt | uniq -c
        awk '{print $1}' solvent_lines_resnames.txt | uniq -c
        #the above counts number of unique instances in a column
        echo " "

        rm lipid_lines.txt
        rm lipid_lines_resnames.txt
        rm solvent_lines.txt
        rm solvent_lines_resnames.txt
#done
