#!/bin/bash
# Скрипт начальной настройки сервера Ubuntu 22.04
# Запускать: bash server_setup.sh <your-github-repo-url>
# Пример:    bash server_setup.sh https://github.com/username/lms-project.git

set -e

REPO_URL=${1:-"https://github.com/YOUR_USERNAME/lms-project.git"}
DEPLOY_USER="deploy"
APP_DIR="/home/$DEPLOY_USER/lms-project"

echo "════════════════════════════════════════"
echo " LMS Project — Настройка сервера"
echo "════════════════════════════════════════"

# ── 1. Обновление системы ──────────────────
echo "▶ Обновление пакетов..."
apt-get update -qq && apt-get upgrade -y -qq

# ── 2. Установка Docker ────────────────────
echo "▶ Установка Docker..."
apt-get install -y -qq ca-certificates curl gnupg git ufw

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update -qq
apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin

# ── 3. Создание пользователя deploy ───────
echo "▶ Создание пользователя $DEPLOY_USER..."
if ! id "$DEPLOY_USER" &>/dev/null; then
  useradd -m -s /bin/bash "$DEPLOY_USER"
fi
usermod -aG docker "$DEPLOY_USER"

# ── 4. SSH-ключ для GitHub Actions ─────────
echo "▶ Генерация SSH-ключа для CI/CD..."
SSH_DIR="/home/$DEPLOY_USER/.ssh"
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

ssh-keygen -t ed25519 -C "github-actions@lms" \
  -f "$SSH_DIR/github_actions" -N "" -q

cat "$SSH_DIR/github_actions.pub" >> "$SSH_DIR/authorized_keys"
chmod 600 "$SSH_DIR/authorized_keys"
chown -R "$DEPLOY_USER:$DEPLOY_USER" "$SSH_DIR"

# ── 5. Клонирование репозитория ─────────────
echo "▶ Клонирование репозитория..."
sudo -u "$DEPLOY_USER" git clone "$REPO_URL" "$APP_DIR"

echo "▶ Создание .env из шаблона..."
sudo -u "$DEPLOY_USER" cp "$APP_DIR/.env.template" "$APP_DIR/.env"

# ── 6. Настройка файрвола ──────────────────
echo "▶ Настройка UFW..."
ufw --force reset > /dev/null
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH    # порт 22 — SSH
ufw allow 80/tcp     # HTTP → Nginx
# Порт 8000 НЕ открываем — приложение доступно только через Nginx
ufw --force enable

echo ""
echo "════════════════════════════════════════"
echo " ✅ Сервер настроен!"
echo "════════════════════════════════════════"
echo ""
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo ""
echo "1️⃣  Добавьте этот приватный ключ в GitHub Secrets (SERVER_SSH_KEY):"
echo "────────────────────────────────────────"
cat "$SSH_DIR/github_actions"
echo "────────────────────────────────────────"
echo ""
echo "2️⃣  Заполните .env на сервере:"
echo "    nano $APP_DIR/.env"
echo ""
echo "3️⃣  Первый запуск:"
echo "    su - $DEPLOY_USER"
echo "    cd lms-project"
echo "    docker compose up -d --build"
echo ""
echo "4️⃣  Создайте суперпользователя:"
echo "    docker compose exec web python manage.py createsuperuser"
echo ""
echo "🌐 Приложение будет доступно по: http://$(curl -s ifconfig.me)"
