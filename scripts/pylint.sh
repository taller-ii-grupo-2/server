#!/usr/bin/env sh
echo "PYINT LINT CHECKING..."
pylint --load-plugins pylint_flask app/
