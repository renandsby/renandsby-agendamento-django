#!/bin/sh

echo "enabling unaccent on database $POSTGRES_DB"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOF
create extension unaccent;
select * FROM pg_extension;
EOF