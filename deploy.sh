#!/bin/sh

USERNAME="$1"
PASSWORD="$2"
if [ "$USERNAME" == "" ] || [ "$PASSWORD" == "" ];
then
  echo "ERROR: expected arguments: <USERNAME> <PASSWORD>"
  exit
fi


# build the distribution archives
rm -rf build/ dist/
python3 setup.py sdist bdist_wheel

# upload to pypi
python3 -m twine upload --repository testpypi dist/* -u $USERNAME -p $PASSWORD
