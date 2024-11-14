# SPDX-License-Identifier: WTFPL

import os
import glob
import gzip
from pathlib import Path

os.system("git pull")

if not os.path.exists("entities"):
    os.makedirs("entities")

existing_compressed_entities = [Path(f).stem.replace(".cfg", "") for f in glob.glob("entitiesgz/*.cfg.gz")]
existing_uncompressed_entities = [Path(f).stem for f in glob.glob("entities/*.cfg")]

decompress_these = sorted(set(existing_compressed_entities) - set(existing_uncompressed_entities))

print(f"need to decompress {len(decompress_these)} items")

for hash in decompress_these:
    print(f"decompressing {hash}.cfg.gz")
    with open(f"entities/{hash}.cfg", "wb") as uncompressed, gzip.open(f"entitiesgz/{hash}.cfg.gz", "rb") as compressed:
        uncompressed.write(compressed.read())
