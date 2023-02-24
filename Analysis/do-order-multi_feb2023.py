#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script to calculate lipid order parameter for coarse-grained Martini2 lipids
# Original script 'do-order-multi.py' is available here: http://www.cgmartini.nl/index.php/downloads/tools/229-do-order
#
# Update: 23 Feb 2023 - Abigail Ormrod & Dheeraj Prakaash (Univ of Oxford)
#   - Corrected PC & PE lipids according to martini_v2.0_lipids.itp
#   - Updated script according to gromacs 2020 
#   - Added POPG, DOPG, DLPG, CDL2
#
# Update: 27 Nov 2011 - Helgi I. Ingolfsson               
#   - Fixed POPC and POPE (tail order is flipped in regular Martini 2.1 itp)
#

from math import sqrt
from os import remove, system, path
from sys import argv, stdout
import subprocess


### SOME TOOLS

# parse a .gro file
# return a list of coordinates
def read_gro(file, atoms):
  line_counter = 0
  number_of_particles = 0
  first, second = [], []
  for line in open(file):
    if line_counter == 1:
      number_of_particles = int(line)
    elif line_counter > 1 and line_counter < number_of_particles + 2:
      if line[10:15].strip() == atoms[0]:
        first.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
      elif line[10:15].strip() == atoms[1]:
        second.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
    line_counter += 1
  return [first, second]



### REAL STUFF

if len(argv) != 11:
  # coments/usage
  print '''
  Compute (second rank) order parameter, defined as:

    P2 = 0.5*(3*<cosÂ²(theta)> - 1)

  where "theta" is the angle between the bond and the bilayer normal.
  P2 = 1      perfect alignement with the bilayer normal
  P2 = -0.5   anti-alignement
  P2 = 0      random orientation

  All lipids defined in the "martini_v2.0_lipids.itp" file can be analyzed
  with this script.
  Usage: python2 do-order-multi_feb2023.py <xtc/trr> <tpr> <initial time> <final time> <skip frames> <bilayer normal - [x] [y] [z]> <# of lipids of that type> <lipid type>

    > python2 do-order-multi_feb2023.py FILE.xtc FILE.tpr 0 5000000 5 0 0 1 755 POPE

  will for example read a 5000 ns trajectory of 755 POPE lipids, calculating the order parameter for 
  every 5th frame and averaging the results. P2 will be calculated relative to the z-axis.

  WARNING script will output all frames in one go, into files called frame_dump_XXX.gro and 
  then remove them so don't have any other files with this name in the current directory.
  ''' % (argv[0], argv[0])
  exit(0)

else:

  # snapshots
  trajfile = argv[1]
  tpr_file = argv[2]
  initial_time = int(argv[3])
  final_time = int(argv[4])
  traj_skip = int(argv[5])
  # (normalized) orientation of bilayer normal
  orientation_of_bilayer_normal = [float(argv[6]), float(argv[7]), float(argv[8])]
  norm = sqrt(orientation_of_bilayer_normal[0]**2 + orientation_of_bilayer_normal[1]**2 + orientation_of_bilayer_normal[2]**2)
  for i in range(3):
    orientation_of_bilayer_normal[i] /= norm
  stdout.write("(Normalized) orientation of bilayer normal: ( %.3f | %.3f | %.3f ).\n" % (
    orientation_of_bilayer_normal[0], \
    orientation_of_bilayer_normal[1], \
    orientation_of_bilayer_normal[2]  \
  ))
  # number of lipids
  number_of_lipids = int(argv[9])
  # lipid type
  lipid_type = argv[10]

  # output legend
  phosphatidylcholine_bond_names = " NC3-PO4 PO4-GL1 GL1-GL2 "
  phosphatidylethanolamine_bond_names = " NH3-PO4 PO4-GL1 GL1-GL2 "
  phosphatidylglycerol_bond_names = " GL0-PO4 PO4-GL1 GL1-GL2 "
  cardiolipin_bond_names = " GL0-PO41 GL0-PO42 PO41-GL11 GL11-GL21 PO42-GL12 GL12-GL22 "
  # PCs
  if   lipid_type == "DAPC": bond_names = phosphatidylcholine_bond_names + "GL1-D1A D1A-D2A D2A-D3A D3A-D4A D4A-C5A GL2-D1B D1B-D2B D2B-D3B D3B-D4B D4B-C5B\n"
  elif lipid_type == "DLPC": bond_names = phosphatidylcholine_bond_names + "GL1-C1A C1A-C2A C2A-C3A GL2-C1B C1B-C2B C2B-C3B\n"
  elif lipid_type == "DOPC": bond_names = phosphatidylcholine_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-D2B D2B-C3B C3B-C4B\n"
  elif lipid_type == "DPPC": bond_names = phosphatidylcholine_bond_names + "GL1-C1A C1A-C2A C2A-C3A C3A-C4A GL2-C1B C1B-C2B C2B-C3B C3B-C4B\n"
  elif lipid_type == "POPC": bond_names = phosphatidylcholine_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-C2B C2B-C3B C3B-C4B\n"
  # PEs
  elif lipid_type == "DAPE": bond_names = phosphatidylethanolamine_bond_names + "GL1-D1A D1A-D2A D2A-D3A D3A-D4A D4A-C5A GL2-D1B D1B-D2B D2B-D3B D3B-D4B D4B-C5B\n"
  elif lipid_type == "DLPE": bond_names = phosphatidylethanolamine_bond_names + "GL1-C1A C1A-C2A C2A-C3A GL2-C1B C1B-C2B C2B-C3B\n"
  elif lipid_type == "DOPE": bond_names = phosphatidylethanolamine_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-D2B D2B-C3B C3B-C4B\n"
  elif lipid_type == "DPPE": bond_names = phosphatidylethanolamine_bond_names + "GL1-C1A C1A-C2A C2A-C3A C3A-C4A GL2-C1B C1B-C2B C2B-C3B C3B-C4B\n"
  elif lipid_type == "POPE": bond_names = phosphatidylethanolamine_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-C2B C2B-C3B C3B-C4B\n"
  # PGs
  elif lipid_type == "POPG": bond_names = phosphatidylglycerol_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-C2B C2B-C3B C3B-C4B\n"
  elif lipid_type == "DOPG": bond_names = phosphatidylglycerol_bond_names + "GL1-C1A C1A-D2A D2A-C3A C3A-C4A GL2-C1B C1B-D2B D2B-C3B C3B-C4B\n"
  elif lipid_type == "DLPG": bond_names = phosphatidylglycerol_bond_names + "GL1-C1A C1A-C2A C2A-C3A GL2-C1B C1B-C2B C2B-C3B \n"
  # CDL
  elif lipid_type == "CDL2": bond_names = cardiolipin_bond_names + "GL11-C1A1 C1A1-C2A1 C2A1-D3A1 D3A1-C4A1 C4A1-C5A1 GL21-C1B1 C2B1-D3B1 D3B1-C4B1 C4B1-C5B1 GL12-C1A2 C1A2-C2A2 C2A2-D3A2 D3A2-C4A2 C4A2-C5A2 GL22-C1B2 C1B2-C2B2 C2B2-D3B2 D3B2-C4B2 C2B2-C5B2\n"

  # output legend
  output_legend = "  Frame" + bond_names 

  # write the stuff
  stdout.write("\n " + output_legend)
  stdout.write(" " + ("-"*(len(output_legend) - 1)) + "\n")
  output = open('order.dat', 'w')
  output.write(output_legend)
  output.write(("-"*(len(output_legend) - 1)) + "\n")

  # Output all frame using trjconv 
  stdout.write("Output all coordinate files \n")
  command = "echo %s | gmx trjconv -f %s -s %s -b %i -e %i -sep -skip %i -pbc whole -o frame_dump_.gro > /dev/null" % (lipid_type, trajfile, tpr_file, initial_time, final_time, traj_skip)
  print command
  subprocess.call(command, shell=True)

  # For each dumped frame
  stdout.write("Starting P2 calculation")
  order_parameters = []
  file_count = 0
  bonds = []
  while True:
    filename = "frame_dump_" + str(file_count) + ".gro"
    if not path.isfile(filename) or path.getsize(filename) == 0:
        break
    
    stdout.write("Taking care of snapshot %s \n" % filename)

    # compute order parameter for each bond, for each snapshot
    current_order_parameters = []
    # bonds respectively involved in the head,
    #                             in the junction head-tail,
    #                             in each tail
    bonds = []

    for bond_name in bond_names.split():
      bonds.append(bond_name.split("-"))

    for bond in bonds:

      # parse .gro file, grep bead coordinates
      first, second = read_gro(filename, bond)

      # compute order parameter for each lipid
      order_parameter = 0.0
      for i in range(number_of_lipids):
        # vector between the two previous beads (orientation doesn't matter)
        vector = [0.0, 0.0, 0.0]
        for j in range(3):
          vector[j] = first[i][j] - second[i][j]
        norm2 = vector[0]**2 + vector[1]**2 + vector[2]**2
        # compute projection on the bilayer normal
        projection = vector[0]*orientation_of_bilayer_normal[0] + vector[1]*orientation_of_bilayer_normal[1] + vector[2]*orientation_of_bilayer_normal[2]
        # order parameter
        order_parameter += projection**2/norm2

      # compute final averaged order parameter
      # store everything in lists
      current_order_parameters.append(0.5*(3.0*(order_parameter/number_of_lipids) - 1.0))
    order_parameters.append(current_order_parameters)

    # write results
    results = "%7i" % file_count
    for order_parameter in current_order_parameters:
      results += "%8.3f" % order_parameter
    stdout.write(" " + results + "\n")
    output.write(results + "\n")

    remove(filename)
    file_count += 1
  # End while loop

  stdout.write(" " + ("-"*(len(output_legend) - 1)) + "\n\n")
  stdout.write("Snapshots analysis done.%s\n" % (" "*56))
  stdout.write("Computing averages...\n")

  # average order parameter
  averaged_order_parameters = []
  for i in range(len(bonds)):
    sum = 0.0
    for j in range(len(order_parameters)):
      sum += order_parameters[j][i]
    averaged_order_parameters.append(sum/len(order_parameters))
 
  # write results
  stdout.write("\n         " + bond_names)
  stdout.write(("-"*(len(output_legend) - 1)) + "\n")
  output.write(("-"*(len(output_legend) - 1)) + "\n")
  results = "average"
  for order_parameter in averaged_order_parameters:
    results += "%8.3f" % order_parameter
  stdout.write(" " + results + "\n")
  output.write(results + "\n")
  stdout.write(" " + ("-"*(len(output_legend) - 1)) + "\n\n")

  # Write abs average order parameters <Sn> (for carbon chains only)
  # WARNING this works with currenct lipids (all have defined x5 none carbon bonds) but for manually added lipids this might not be true
  ave_chain_s = 0
  for i in averaged_order_parameters[3:]: 
     ave_chain_s += abs(i)
  average_txt = "Abs average order parameters for carbon chains <Sn> = %8.3f \n\n" % (ave_chain_s / (len(averaged_order_parameters)-3))
  stdout.write(average_txt)
  output.write(average_txt)
  stdout.write("Results written in \"order.dat\".\n")

  output.close()
