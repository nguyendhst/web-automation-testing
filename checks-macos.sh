#!/bin/zsh

# verify if python >= 3.10 is installed
PYTHON_VERSION=$(python3 -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))')

if [ -z "$PYTHON_VERSION" ]; then
  echo "Python is not installed."
  exit 1
fi

REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
  echo -e "\u2705 Python version is greater than or equal to 3.10: $PYTHON_VERSION"
else
  echo -e "\u274C Python version is less than 3.10: $PYTHON_VERSION"
  exit 1
fi

# verify if pip is installed
PIP_VERSION=$(pip3 --version)

if [ -z "$PIP_VERSION" ]; then
  echo "Pip is not installed."
  exit 1
fi

echo -e "\u2705 Pip is installed: $PIP_VERSION"


# verify if homebrew is installed
BREW_VERSION=$(brew --version)

if [ -z "$BREW_VERSION" ]; then
  echo -e "\u274C Homebrew is not installed."
  exit 1
fi

echo -e "\u2705 Homebrew is installed: $BREW_VERSION"


