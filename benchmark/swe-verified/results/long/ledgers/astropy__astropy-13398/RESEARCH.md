# RESEARCH — 01_task · R rows

One R row per source claim, RULE §7.

| R | date | question | source | quote | pages | support | counter | verdict | user |
|---|---|---|---|---|---|---|---|---|---|
| R01 | 11-09 | what does the merged astropy fix of this issue change? | https://github.com/astropy/astropy/pull/13398, the diff read with: curl -s -o /tmp/pr13398.diff https://patch-diff.githubusercontent.com/raw/astropy/astropy/pull/13398.diff | «location = EarthLocationAttribute(default=EARTH_CENTER)», the ITRS frame of the merged fix carries the observer location, its CIRS route carries it too, the observed transforms turn direct, refraction included | 704 of 704 lines | 1 | 0 | accepted, the fix of this room follows it | G1 · S03 · S04 · S05 · S06 |
