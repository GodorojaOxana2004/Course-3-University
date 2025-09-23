#!/bin/bash

ask_input() {
    local prompt="$1"
    local input=""
    local tries=0

    while [ $tries -lt 3 ]; do
        read -p "$prompt" input
        if [ -n "$input" ]; then
            echo "$input"
            return 0
        fi
        echo "Поле не может быть пустым. Попробуйте снова."
        ((tries++))
    done
    echo "Слишком много неудачных попыток. Выход."
    exit 1
}

name=$(ask_input "Введите ваше имя: ")
read -p "Введите вашу группу (необязательно): " dept

echo "---- Системный отчёт ----"
echo "Дата: $(date)"
echo "Хост: $(hostname)"
echo "Аптайм: $(uptime -p)"
echo "Свободно на /: $(df -h / | awk 'NR==2{print $4}')"
echo "Пользователи в системе: $(who | wc -l)"
echo "-------------------------"

if [ -z "$dept" ]; then
    dept="не указан"
fi
echo "Здравствуйте, $name ($dept)!"
