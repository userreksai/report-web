#!/usr/bin/env bash
set -euo pipefail

APP_DIR=/opt/report-web
REPOSITORY=https://github.com/userreksai/report-web.git

if [[ ! -d "$APP_DIR/.git" ]]; then
  sudo git clone "$REPOSITORY" "$APP_DIR"
else
  sudo git -C "$APP_DIR" pull --ff-only
fi

sudo chown -R www-data:www-data "$APP_DIR"
cd "$APP_DIR"
if command -v pnpm >/dev/null 2>&1; then
  sudo -u www-data pnpm install --frozen-lockfile
else
  sudo -u www-data npm install --no-audit --no-fund
fi
sudo -u www-data npm run build

sudo install -m 0644 "$APP_DIR/deploy/report-web.service" /etc/systemd/system/report-web.service
sudo systemctl daemon-reload
sudo systemctl enable report-web
sudo systemctl restart report-web
sudo systemctl status report-web --no-pager
