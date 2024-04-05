call wrangler r2 object put venus/lump_checksums.csv --file=lump_checksums.csv
set /p PURGETOKEN=<..\secretpurge
curl -X POST "https://api.cloudflare.com/client/v4/zones/1aa75e18589c3649abe7da1eb740bf46/purge_cache" ^
	-H "Authorization: Bearer %PURGETOKEN%" ^
	-H "Content-Type: application/json" ^
	--data "{\"files\":[\"https://venus.fastdl.me/lump_checksums.csv\"]}"
