#!/usr/bin/env python3
"""measures.py — the measure of 01_pressure-drop, RULE §5. g1 = reference cases the calculator misses by over 1 percent.
The reference: water at 20 degrees C, viscosity 1.0e-3 Pa s, pipe length 2 m, diameter 0.01 m, flow 1.0e-5 m3/s.
Hagen-Poiseuille gives 81.487 Pa. Reynolds number 1273, laminar. Usage: measures.py g1 [ROOM]."""
import os, subprocess, sys

CASES = [((1.0e-3, 2.0, 0.01, 1.0e-5), 81.487)]


def g1(room=None, bl=None):
    """Reference cases the calculator misses by over 1 percent. A missing calculator misses every case."""
    room = room or os.path.dirname(os.path.abspath(__file__))
    calc = os.path.join(room, 'calc.py')
    if not os.path.isfile(calc):
        return len(CASES)
    missed = 0
    for args, want in CASES:
        run = subprocess.run([sys.executable, '-I', '-B', calc, *map(str, args)], capture_output=True, text=True)
        try:
            got = float(run.stdout.strip())
        except ValueError:
            missed += 1
            continue
        missed += abs(got - want) / want > 0.01
    return missed


if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'g1'
    print(name, globals()[name](sys.argv[2] if len(sys.argv) > 2 else None))
