sed -i.bak 's/wjv316/admin/'.fakenews_1m.db
psql -U admin fakenews_1m < ./fakenews_1m.db
