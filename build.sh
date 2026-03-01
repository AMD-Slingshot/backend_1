#!/usr/bin/env bash
# build.sh - Render build script

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install packages with pre-built wheels
pip install --no-cache-dir -r requirements.txt
