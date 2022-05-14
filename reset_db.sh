#!/bin/sh

if [ "$#" -gt 0 ]; then
    echo Unknown arguments: "$@"
    echo Usage: /bin/sh reset_db.sh
    exit 1
fi

if ! echo '' "$0" | grep 'reset_db\.sh$'; then
    echo Something bad happened. Refuse to operate.
    echo Did you move this script?
    echo hint: this may accidentally delete another database
    exit 1

fi

cd -- "$(dirname -- "$0")"

rm -f data.db
sqlite3 data.db <<'EOF'
.read schema.sql
.read initial_data.sql
EOF

echo Database is now reset.