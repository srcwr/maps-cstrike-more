`python -m pip install 'bsp_tool @git+https://github.com/snake-biscuits/bsp_tool.git'`
- this actually won't work oops

## WHAT IS WHAT
- `entities`
	- Extracted entity lump files from each map. You won't have this unless you use `dumper.py` yourself or have extracted all of the files from `entitiesgz`
- `entitiesgz`
	- Compressed (.gz) entity lump files for each map
- `filelist`
	- CSV with the list of packed files in a .bsp
- `auto.cmd`
	- Automatic... processor... thing for this repo. Used by [maps-cstrike](https://github.com/srcwr/maps-cstrike)'s `gamebanana-automatic.py`
- `cubemapper.py`
	- Attempts to deduce a .bsp file's originally compiled map/file name from packed cubemaps, .nav's, and more.
- `dumper.py`
	- Dumps entity lumps and file lists
- `ignore.csv`
	- CSV with the list .bsp's that had errors or warnings from `dumper.py`
- `ignore_pak.csv`
	- CSV with the list .bsp's that had errors or warnings from `dumper.py`'s filelist step
- `lump_checksummer.py`
	- Generates the lump checksum that is used by the Source Engine to verify players are on the correct map. This checksum is also in server logs when changing maps.
- `lump_checksums.csv`
	- Lump checksums...... ^^^^^
- `original_mapname.csv`
	- Potentially original map names from `cubemapper.py`
- `timestamper.py`
	- Something
- `timestamps.csv`
	- Timestamps for .bsp files. May or may not be close to a map's creation.
