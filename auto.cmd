:: @echo off
cd "%~dp0"
uv run dumper.py
uv run cubemapper.py
uv run timestamper.py
uv run lump_checksummer.py
git add entitiesgz filelist ignore_pak.csv ignore.csv original_mapname.csv timestamps.csv lump_checksums.csv vscript_probably.csv
SET GIT_COMMITTER_NAME= "srcwrbot"
SET GIT_COMMITTER_EMAIL="bot@srcwr.com"
git commit --author="srcwrbot <bot@srcwr.com>" -m "%1"
git push originbot
.\purge_venus.bat
