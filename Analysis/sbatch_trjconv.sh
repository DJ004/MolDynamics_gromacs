#!/bin/bash
#SBATCH --account=________
#SBATCH --partition=______
#SBATCH --qos=____________
#SBATCH --cpus-per-task=1
#SBATCH --time=00:08:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --array=1-3%3
#SBATCH --mem=4G
#SBATCH -o out.%x_%j.out
#SBATCH -e out.%x_%j.err
#SBATCH -J _______________

module --force purge
module load gcc/11.2.0-gpu openmpi/5.0.3-gpu gromacs/2024.3-gpu

R=$SLURM_ARRAY_TASK_ID
echo "ARRAY TASK = $SLURM_ARRAY_TASK_ID"
echo "R = $R"

NAME="PR_wt00pN"

printf "c\nc\nc\nc\nc\nc\nc\nc\nc\nc\nc\nc\n" | srun --exclusive -N1 -n1 gmx_mpi trjcat -f ${NAME}_r${R}*part*xtc -o ${NAME}_r${R}_cat.xtc -settime
# include as many "c\n" as the max num of *part*xtc across all sim reps.
wait
echo "trjcat for rep_$R finished."

mkdir part_XTCs pull_XVGs
mv ${NAME}_r${R}*part*xtc part_XTCs/
mv ${NAME}_r${R}*pull*xvg pull_XVGs/ # if any

printf "q\n" | srun --exclusive -N1 -n1 gmx_mpi make_ndx -f ${NAME}_r1.tpr -o index.ndx

echo Protein Protein | srun --exclusive -N1 -n1 gmx_mpi trjconv -f ${NAME}_r${R}_cat.xtc -s ${NAME}_r${R}.tpr -o ${NAME}_r${R}_prot_dt2.5ns.xtc -n index.ndx -dt 2500 -pbc mol -ur compact -center
wait
echo "trjconv for rep_$R finished."
