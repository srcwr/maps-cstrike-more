@echo off
python dumper.py
python cubemapper.py
python timestamper.py
python lump_checksummer.py
git add entitiesgz filelist ignore_pak.csv ignore.csv original_mapname.csv timestamps.csv lump_checksums.csv
SET GIT_COMMITTER_NAME= "srcwrbot"
SET GIT_COMMITTER_EMAIL="bot@srcwr.com"
git commit --author="srcwrbot <bot@srcwr.com>" -m "%1"
git push originbot
