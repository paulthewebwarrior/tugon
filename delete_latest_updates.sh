#!/bin/bash
# Remove the CAS candidate adder script
rm -f add_cas_candidates.py
# Remove the heart-ensc icon if it was added after the rollback point
rm -f static/images/heart-ensc.png
# Optionally, remove any other files you know were added after the rollback
