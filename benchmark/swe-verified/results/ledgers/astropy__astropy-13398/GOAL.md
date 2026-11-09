# GOAL — 01_task

## Question
Owner, 2026-11-09: «Fix the issue in TASK.md in this repository».

## Stance
the issue in TASK.md is fixed in this repository. This room follows RULE.md of hectoline by its link.

## Audience
The owner. The terminal of this room. The 00 session that watches it.

## Goals
Progress = leaves at target ÷ leaves, RULE §5. Done steps ÷ all steps is the work count. Each goal leaf has one measure in this room's measures.py.

| G | goal | parent | measure | target | baseline |
|---|---|---|---|---|---|
| G0 | the issue in TASK.md is fixed in this repository | — | leaves at target | 1 of 1 | 0 of 1 |
| G1 | a direct ITRS to Observed path, the one the issue of TASK.md asks for, serves the frame graph of astropy | G0 | acceptance checks of the direct path that pass, measures.py g1 | 4 of 4 | 0 of 4 |

## Acceptance checks of G1
Four checks, one number each, run by accept.py in the room, counted by measures.py g1.
1. overhead-altaz: an ITRS position 10 km over the observer reads alt 90 deg to 1 µas in AltAz.
2. overhead-hadec: that same position reads ha 0 h to 1 µas, dec the geodetic latitude of the observer to 1 µas, in HADec.
3. round-trip: AltAz to ITRS, HADec to ITRS return 1000 satellite positions to 1 mm, no pressure in the frame.
4. refraction: under 1000 hPa the azimuth holds to 1 µas, the distance holds the topocentric range to 1 mm, the elevation shift matches the CIRS route to 20 mas over 20 deg altitude, HADec agrees with AltAz to 1 mas. The 20 mas is the second order effect of the 0.32 arcsec diurnal aberration that the CIRS route carries, measured in the room.
At the base commit 6d44ad4 of this room no tool runs them, so g1 counts 0 of 4. Once the tool stands, the round trip alone holds, 1 of 4: the old path through ICRS inverts itself, yet it reads a geocentric direction, so it misses the zenith by 3.7 deg and the range by 594 m, both measured in the room.

## Layers and flow
inputs → rules → state → result → view. Rules: RULE.md of hectoline by its link. State: the six ledgers and the log.
