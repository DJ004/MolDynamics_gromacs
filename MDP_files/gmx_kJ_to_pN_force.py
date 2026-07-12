# Given value in kJ/mol/nm
gromacs_force = 12

# Avogadro's number
N_A = 6.02214076e23

# Unit conversion logic:
# 1 kJ = 10^3 J
# 1 mol = 6.02214076e23 particles
# 1 nm = 10^-9 m
# So, 1 kJ/mol/nm = (10^3 J) / (6.02214076e23 * 10^-9 m) = 10^12 / N_A  J/m (or N)
# 1 pN = 10^-12 N, so 1 N = 10^12 pN
# Therefore:
# 1 kJ/mol/nm = (10^12 / N_A) * 10^12 pN = 10^24 / N_A pN

factor = (10**3) / (N_A * 10**-9) # in Newtons
factor_pN = factor * 10**12 # in pN

result_pN = gromacs_force * factor_pN
print(f"Factor: {factor_pN}")
print(f"Result: {result_pN}")

# --------------------------------------------------
# ref: https://share.google/aimode/mwEv2U2UFAJXlcJnD
# A force of 12 kJ/mol/nm in GROMACS corresponds to an acting single-molecule force of 19.93 pN
