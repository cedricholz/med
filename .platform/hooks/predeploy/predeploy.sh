#!/bin/bash
sudo mkdir -p /var/app/staging/frontend/build
sudo aws s3 sync s3://marlinsurf-artifacts/ /var/app/staging/frontend/build/