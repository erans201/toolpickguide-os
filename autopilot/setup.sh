#!/bin/sh
# Cloud robot setup (2026-10-23). Plain `pip` in the cloud image installs into a different Python than
# `python3`, so always go through `python3 -m pip`. A key-check run also hit a cryptography import panic
# (Debian's system copy); reinstalling it into python3's own site-packages fixes that.
python3 -m pip install -q requests python-dotenv markdown html2text google-api-python-client google-auth google-analytics-data pillow 2>&1 | grep -v "Running pip as the 'root'" | tail -2
if ! python3 -c "import google.oauth2.service_account" >/dev/null 2>&1; then
  python3 -m pip install -q --ignore-installed cryptography 2>&1 | grep -v "Running pip as the 'root'" | tail -1
fi
python3 -c "import requests, dotenv, markdown, html2text, googleapiclient, google.oauth2.service_account, google.analytics.data, PIL" \
  && echo "setup OK" || echo "setup FAILED: report under ALERTS"
