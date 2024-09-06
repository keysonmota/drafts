pg_restore \
--host "127.0.0.1" \
--port "5432" \
--username "postgres" \
--no-password \
--dbname "integratto2" \
--verbose \
"/docker-entrypoint-initdb.d/integratto2.backup"