#!/usr/bin/env bash

sudo curl -L https://github.com/bct-sales/frontend/releases/latest/download/index.html -o /var/www/html/bct.html
sudo chown www-data:www-data /var/www/html/bct.html
