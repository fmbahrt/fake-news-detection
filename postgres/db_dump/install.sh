sed -i.bak 's/wjv316/admin/'.fakenews_100k.db
psql -U admin fakenews_100k < ./fakenews_100k.db
