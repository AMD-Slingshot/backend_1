#!/usr/bin/env bash
# build.sh - Render build script

set -o errexit

# Install system dependencies for Pillow (image processing)
apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev

# Upgrade pip
pip install --upgrade pip

# Install Python packages
pip install --no-cache-dir -r requirements.txt
