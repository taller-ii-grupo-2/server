#!/usr/bin/env sh
echo "TESTS RUNNING..."
export DATABASE_URL="sqlite://"
export APP_SETTINGS="config.TestingConfig"
python -m pytest --cov=tests/ --color=yes -s
