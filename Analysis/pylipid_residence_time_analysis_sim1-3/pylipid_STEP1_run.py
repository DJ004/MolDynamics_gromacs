#!/usr/bin/python

# ------------------------------

# Based on documentation provided by Wanling Song et al.
# Original documentation: https://pylipid.readthedocs.io/en/master/tutorials/0-application-walk-through.html

# Paper:   PyLipID: A Python Package for Analysis of Protein-Lipid Interactions from Molecular Dynamics Simulations.
# Authors: Wanling Song*, Robin A. Corey, T. Bertie Ansell, C. Keith Cassidy, Michael R. Horrell, Anna L. Duncan, Phillip J. Stansfeld, and Mark S. P. Sansom*
# Journal: J. Chem. Theory Comput. 2022, 18, 2, 1188-1201
# DOI:     https://doi.org/10.1021/acs.jctc.1c00708
# Github:  https://github.com/wlsong/PyLipID

# Script requires:
# pylipid 
# numpy 
# Regarding numpy: either numpy version <1.24, or change dtype=np.int to dtype=np.int64
#                  source: https://github.com/wlsong/PyLipID/issues/28

# Script USAGE: 
# python pylipid_STEP1_run.py

# ------------------------------

import pylipid
from pylipid.api import LipidInteraction


# ------ SIMULATION REPLICATE r1 ------


trajfile_list = ["protein_lipid_r1.xtc"] #edit
topfile_list = ["protein_lipid_r1.gro"]  #edit
cutoffs = [0.475, 0.8]                   #default
nprot = 1                                #number of prot
timeunit = 'us'                          #default
save_dir = "./pylipid_r1"                #edit here and in the li.dataset.to_csv... command for each lipid


lipid = "CHOL"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r1/pylipid_chol.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPG"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r1/pylipid_popg.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPS"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r1/pylipid_pops.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPE"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r1/pylipid_pope.xvg', header=None, index=None, sep='\t', mode='a')


# ------ SIMULATION REPLICATE r2 ------

trajfile_list = ["protein_lipid_r2.xtc"] #edit
topfile_list = ["protein_lipid_r2.gro"]  #edit
cutoffs = [0.475, 0.8]                   #default
nprot = 1                                #number of prot
timeunit = 'us'                          #default
save_dir = "./pylipid_r2"                #edit here and in the li.dataset.to_csv... command for each lipid


lipid = "CHOL"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r2/pylipid_chol.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPG"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r2/pylipid_popg.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPS"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r2/pylipid_pops.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPE"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r2/pylipid_pope.xvg', header=None, index=None, sep='\t', mode='a')


# ------ SIMULATION REPLICATE r3 ------

trajfile_list = ["protein_lipid_r3.xtc"] #edit
topfile_list = ["protein_lipid_r3.gro"]  #edit
cutoffs = [0.475, 0.8]                   #default
nprot = 1                                #number of prot
timeunit = 'us'                          #default
save_dir = "./pylipid_r3"                #edit here and in the li.dataset.to_csv... command for each lipid


lipid = "CHOL"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r3/pylipid_chol.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPG"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r3/pylipid_popg.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPS"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r3/pylipid_pops.xvg', header=None, index=None, sep='\t', mode='a')


lipid = "POPE"
li = LipidInteraction(trajfile_list, topfile_list=topfile_list, cutoffs=cutoffs, lipid=lipid, nprot=nprot, save_dir=save_dir)
durations = li.compute_residue_duration()
occupancies = li.compute_residue_occupancy()
lipidcounts = li.compute_residue_lipidcount()
koffs, res_times = li.compute_residue_koff(plot_data=True, fig_close=True)
li.dataset.to_csv(r'./pylipid_r3/pylipid_pope.xvg', header=None, index=None, sep='\t', mode='a')

