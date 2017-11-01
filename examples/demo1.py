# -*- coding: utf-8 -*-

import quantarhei as qr


en = [0.0, 1.0]

M = qr.Molecule(name="My first two-level molecule", elenergies=en)

H = M.get_Hamiltonian()

print(H)

print("version = ", qr.Manager().version)
