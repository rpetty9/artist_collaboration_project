#!/bin/bash

echo "Creating Python 3.10 virtual environment in ./venv"
python3.10 -m venv venv

echo "Activating virtual environment"
source venv/bin/activate

echo "Installing required packages"
pip install --upgrade pip
pip install pandas plotly dash networkx pyvis numpy scikit-learn

echo "Installing done! Your environment is ready and activated."
echo "To activate again later, run: source venv/bin/activate"
