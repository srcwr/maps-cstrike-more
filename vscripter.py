# SPDX-License-Identifier: WTFPL

# Only used for the initial filling of vscript_probably.csv

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "bsp_tool @ git+https://github.com/srcwr/bsp_tool@dc486011ab5bfee6f68f32367c1127e8b972b3a5",
# ]
# ///

import glob
import csv
import re
from pathlib import Path

vscript_filelist_probably = set()
vscript_entities_probably = set()

for filename in glob.iglob("entities/*.cfg"):
    maphash = Path(filename).stem
    with open(filename, "rb") as f:
        ents = f.read()
    if re.search(b"(script |script_execute|RunScriptCode|RunScriptFile|CallScriptFunction)", ents, re.I):
        print(f"entities {maphash}")
        vscript_entities_probably.add(maphash)

for filename in glob.iglob("filelist/*.csv"):
    maphash = Path(filename).stem
    with open(filename, newline="", encoding="utf-8") as f:
        cr = csv.reader(f)
        for line in cr:
            if line[0] == "sha1":
                continue
            if ("vscripts" in line[0].lower()) or line[0].endswith(".nut"):
                vscript_filelist_probably.add(maphash)
                print(f"filelist {maphash}")


if len(vscript_filelist_probably) > 0 or len(vscript_entities_probably) > 0:
    print("vscript probably exists, so doing csv stuff")
    vscript_csv = {}
    with open("vscript_probably.csv", newline="", encoding="utf-8") as f:
        cr = csv.reader(f)
        for line in cr:
            if line[0] == "sha1":
                continue
            vscript_csv[line[0]] = line[1]
    for maphash in (vscript_filelist_probably&vscript_entities_probably):
        vscript_csv[maphash] = "filelist & entities"
    for maphash in (vscript_filelist_probably-vscript_entities_probably):
        vscript_csv[maphash] = "filelist"
    for maphash in (vscript_entities_probably-vscript_filelist_probably):
        vscript_csv[maphash] = "entities"

    with open("vscript_probably.csv", "w", newline="", encoding="utf-8") as csvfile:
        mycsv = csv.writer(csvfile)
        mycsv.writerow(["sha1","reason"])
        xxx = dict(sorted(vscript_csv.items()))
        for k,v in xxx.items():
            mycsv.writerow([k, v])
