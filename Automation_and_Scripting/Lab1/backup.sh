#!/usr/bin/env bash 
set -euo pipefail

usage(){
echo " $0 Using this directory: /home/oxana/Documents/All_Labs_University"
echo "$0 Copy in this Directory: /home/oxana/backups"
exit 1
}

if [ $# -lt 1]; then usge;fi

SRC="$1"
DEST="${2:-/backup}"

if [! -d "$SRC"]; then 
echo "Mistake: directory '$SRC'  not found." >&2
exit2
fi

if[ ! -d "$DEST"]; then
echo "Copy-Directory  '$DEST' not found - create..."
mkdir -p "$DEST"
fi 

DATE_STR="$(date +%F_%H-%M-%S)"
BASE="$(basename "$SRC")"
ARCHIVE="${DEST}/${BASE}_backup_${DATE_STR}.tar.gz"

tar -czf "$ARCHIVE" -C "$(dirname "$SRC")" "$BASE"

echo "Rezerv oopy is create: $ARCHIVE"