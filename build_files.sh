# pip install -r requirements.txt
# python3.9 manage.py collectstatic

#!/bin/bash

# Ensure Python and pip are available
which python3.9 || { echo "Python3.9 not found!"; exit 1; }
which pip3 || { echo "pip3 not found! Installing pip..."; curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3.9 get-pip.py; }

# Install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Apply migrations (if needed)
python3.9 manage.py migrate --noinput

# Collect static files
python3.9 manage.py collectstatic --noinput --clear --verbosity 3

# Create the static files directory (needed for Vercel)
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
