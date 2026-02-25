import MDAnalysis as mda
import numpy as np
import pandas as pd

def calculate_order_parameter(universe, selection_string, ref_axis='z'):
    """
    Calculate the lipid order parameter S_CD.

    Parameters:
    universe : MDAnalysis Universe object
        The Universe object containing the trajectory data.
    selection_string : str
        The selection string to select the lipid atoms (e.g., 'name C2 H2').
    ref_axis : str
        The reference axis for the bilayer normal ('x', 'y', or 'z').

    Returns:
    order_parameters : dict
        A dictionary with residue names as keys and their corresponding order parameters as values.
    """

    # Get the reference axis index
    axis_dict = {'x': 0, 'y': 1, 'z': 2}
    ref_axis_index = axis_dict[ref_axis]

    # Select the atoms
    atom_group = universe.select_atoms(selection_string)

    order_parameters = {}
    
    for res in atom_group.residues:
        # Initialize the cos^2(theta) accumulator
        cos2_theta_sum = 0.0
        n_bonds = 0

        for atom in res.atoms:
            if atom.name.startswith('C') and len(atom.bonded_atoms) > 0:
                for bonded_atom in atom.bonded_atoms:
                    if bonded_atom.name.startswith('H'):
                        bond_vector = bonded_atom.position - atom.position
                        bond_vector /= np.linalg.norm(bond_vector)
                        cos_theta = bond_vector[ref_axis_index]
                        cos2_theta_sum += cos_theta ** 2
                        n_bonds += 1

        if n_bonds > 0:
            S_CD = 0.5 * (3.0 * (cos2_theta_sum / n_bonds) - 1.0)
            order_parameters[res.resname] = S_CD

    return order_parameters

# Load the GROMACS trajectory
universe = mda.Universe('topology.top', 'trajectory.xtc')

# Define the selection string for the lipid atoms
selection_string = 'name C2 H2'  # Adjust this based on your system

# Calculate the order parameters
order_parameters = calculate_order_parameter(universe, selection_string)

# Print the results
for resname, S_CD in order_parameters.items():
    print(f'Residue: {resname}, S_CD: {S_CD}')

# Optionally, save the results to a CSV file
df = pd.DataFrame(order_parameters.items(), columns=['Residue', 'Order Parameter'])
df.to_csv('order_parameters.csv', index=False)
