#!/bin/bash
#SBATCH --account=
#SBATCH --partition= 
#SBATCH --qos=
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --array=1-3%3
#SBATCH --mem=8G       
#SBATCH -o out.%x_%j.out
#SBATCH -e out.%x_%j.err
#SBATCH -J 

module --force purge
module load gcc/11.2.0-gpu openmpi/5.0.3-gpu gromacs/2024.3-gpu

R=$SLURM_ARRAY_TASK_ID
echo "ARRAY TASK = $SLURM_ARRAY_TASK_ID"
echo "R = $R"

CONC=40

printf "c\nc\nc\nc\nc\nc\nc\nc\n" | srun --exclusive -N1 -n1 gmx_mpi trjcat -f PR_wt_chol${CONC}_00pN_r${R}*part*xtc -o PR_wt_chol${CONC}_00pN_r${R}_cat.xtc -settime
# include as many "c\n" as the max num of *part*xtc across all sim reps.
wait
echo "trjcat for rep_$R finished."

echo 23 | srun --exclusive -N1 -n1 gmx_mpi trjconv -f PR_wt_chol${CONC}_00pN_r${R}_cat.xtc -s PR_wt_chol${CONC}_00pN_r${R}.tpr -o PR_wt_chol${CONC}_00pN_r${R}_protCHOL_dt2.5ns.xtc -n index.ndx -dt 2500
wait
echo "trjconv for rep_$R finished."

