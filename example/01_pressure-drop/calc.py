#!/usr/bin/env python3
"""calc.py MU L D Q — the pressure drop of laminar pipe flow by Hagen-Poiseuille, in Pa.
MU viscosity in Pa s, L length in m, D inner diameter in m, Q volume flow in m3/s."""
import math, sys


def pressure_drop(mu, length, diameter, flow):
    """128 mu L Q / (pi D^4), the laminar relation."""
    return 128 * mu * length * flow / (math.pi * diameter ** 4)


if __name__ == '__main__':
    mu, length, diameter, flow = map(float, sys.argv[1:5])
    print(f'{pressure_drop(mu, length, diameter, flow):.3f}')
