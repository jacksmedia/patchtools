#!/bin/bash

BASE_DIR="C:/Users/J4cks/Documents/patchwork"

# Run scripts for Plus patches & manifests
echo "Running stylepacks-maker.py..."
python "$BASE_DIR/tools/_style-packs/stylepacks-maker.py"

echo "Running sfc-exfiltrator.py..."
python "$BASE_DIR/tools/_style-packs/sfc-exfiltrator.py"

echo "Running manifest-exporter.py..."
python "$BASE_DIR/tools/_style-packs/manifest-exporter.py"

echo "Running stylepack-maker.py from $BASE_DIR..."
cd $BASE_DIR
python stylepack-maker.py

# Run scripts for Classic patches

echo "Running classic-stylepacks-maker.py..."
python "$BASE_DIR/tools/_style-packs/classic-stylepacks-maker.py"

echo "Running sfc-exfiltrator2.py..."
python "$BASE_DIR/tools/_style-packs/sfc-exfiltrator2.py"

echo "Running classic-stylepack-maker.py from $BASE_DIR..."
cd $BASE_DIR
python classic-stylepack-maker.py

# Pause for user input to prevent the window from closing
echo "Press Enter to exit..."
read