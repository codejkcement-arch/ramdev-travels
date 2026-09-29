#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../backend"
python seed.py
