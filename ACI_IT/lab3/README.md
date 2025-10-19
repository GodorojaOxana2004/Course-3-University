# Лабораторная работа N3

В этом репозитории собраны два Ansible-плейбука для базовой настройки серверов: деплой статического сайта на Nginx и создание пользователя с доступом по SSH и правами `sudo`.

---

## 1. Плейбук: Статический сайт через Nginx

**Цель:**  
Установить `nginx` и развернуть мини-сайт из архива `.tar.gz`.

### Шаги:
1. Установить и запустить `nginx`.
2. Создать каталог для сайта:
   ```bash
   /var/www/mysite
   ```
3. Распаковать архив сайта `files/site.tar.gz` в `/var/www/mysite` (используется модуль `unarchive`).
4. Положить минимальный `nginx`-виртуальный хост и активировать его (перезапуск `nginx` через handler).

### Конфигурация виртуального хоста (`mysite.conf`):
```nginx
server {
    listen 80;
    listen [::]:80;

    server_name _;

    root /var/www/mysite;
    index index.html;

    access_log /var/log/nginx/mysite_access.log;
    error_log  /var/log/nginx/mysite_error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Структура проекта:
```
playbooks/
  01_static_site.yml
files/
  site.tar.gz        # заранее упакованный index.html и статика
  mysite.conf        # простой server {} для nginx
```

---

## 2. Плейбук: Пользователь деплоя + SSH-ключ + sudoers drop-in

**Цель:**  
Создать техпользователя `deploy` с доступом по ключу и правами `sudo` через отдельный файл в `/etc/sudoers.d`.

### Шаги:
1. Создать пользователя `deploy` и добавить его в группу `sudo`.
2. Прописать публичный ключ в:
   ```bash
   ~deploy/.ssh/authorized_keys
   ```
   (используется модуль `authorized_key`).
3. Создать файл `/etc/sudoers.d/deploy` с правилом:
   ```
   deploy ALL=(ALL) NOPASSWD:ALL
   ```
4. Проверить синтаксис sudoers:
   ```bash
   visudo -cf /etc/sudoers.d/deploy
   ```
   — только если проверка успешна, оставить файл.

---

## Использование

Запуск плейбуков через Ansible:
```bash
ansible-playbook playbooks/01_static_site.yml
ansible-playbook playbooks/02_deploy_user.yml
```

---

## Требования

- Ansible 2.9+  
- Доступ по SSH к целевым хостам
- Права `sudo` на целевых хостах для установки пакетов и создания пользователей
