#!/bin/bash

PATH_FS="$1"
THRESHOLD="${2:-80}"

if [ -z "$PATH_FS" ] || [ ! -d "$PATH_FS" ]; then
    echo "Ошибка: путь не найден"
    exit 2
fi

USAGE=$(df -h "$PATH_FS" | awk 'NR==2{print $5}' | tr -d '%')

echo "$(date '+%Y-%m-%d %H:%M:%S')"
echo "Путь: $PATH_FS"
echo "Использовано: ${USAGE}%"

if [ "$USAGE" -lt "$THRESHOLD" ]; then
    echo "Статус: OK"
    exit 0
else
    echo "WARNING: диск почти заполнен!"
    exit 1
fi
