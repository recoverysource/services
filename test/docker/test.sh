#!/bin/sh
##
# This script is the primary entry point for testing within containers.
#
# The entire local repository is mounted at /srv/services and then testing
# invokes Dockertest.sh from within the container, returning exit status.
##
# Fail on first error
set -e

# Root Directory
cd /srv/services/test

# Initial Configuration
echo 'NOTICE :: Running initial config sync ...'
ansible-playbook maintenance.yml

# Ensure Idempotency
echo 'NOTICE :: Running again (expect zero changes) ...'
ansible-playbook maintenance.yml | grep -E 'changed=0\s+unreachable=0\s+failed=0\s'

# Validation Tests
echo 'NOTICE :: Running automated tests ...'
python3 -m pytest --type container
