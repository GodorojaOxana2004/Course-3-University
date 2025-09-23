#!/bin/bash

SRC="$1"
DST="${2:-$HOME/backups}"

if [ -z "$SRC" ] || [ ! -d "$SRC" ]; then
    echo "Ошибка: укажите существующий путь"
    exit 1
fi

mkdir -p "$DST" || { echo "Нет доступа для записи в $DST"; exit 1; }

TS=$(date +%Y%m%d_%H%M%S)
BASE=$(basename "$SRC")
ARCHIVE="backup_${BASE}_${TS}.tar.gz"

tar -czf "$DST/$ARCHIVE" -C "$(dirname "$SRC")" "$BASE"
STATUS=$?

SIZE=$(du -h "$DST/$ARCHIVE" | cut -f1)

echo "$(date +%Y-%m-%dT%H:%M:%S) SRC=$SRC DST=$DST FILE=$ARCHIVE SIZE=$SIZE STATUS=$STATUS" >> "$DST/backup.log"

exit $STATUS
