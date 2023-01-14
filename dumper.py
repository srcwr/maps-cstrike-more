
import os
import glob
import bsp_tool
from pathlib import Path

ignored = {}
with open("ignore.txt") as f:
    for line in f:
        ignored[line.split(",")[0]] = True

for filename in glob.iglob("../hashed/*.bsp"):
    maphash = Path(filename).stem
    if maphash in ignored:
        continue
    newents = "entities/" + maphash + ".cfg"
    if os.path.exists(newents): # should read dir once & check the dict tbh... don't care... i'd rather leave this comment instead...
        continue
    print(maphash)
    bsp = bsp_tool.load_bsp(filename)
    if "ENTITIES" in bsp.headers:
        ents = bsp.ENTITIES.as_bytes()[:-1] # -1 to remove trailing null byte
        with open(newents, "wb") as f:
            f.write(ents)
    #break