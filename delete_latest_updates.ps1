# Remove the CAS candidate adder script
Remove-Item -Path add_cas_candidates.py -ErrorAction SilentlyContinue
# Remove the heart-ensc icon if it was added after the rollback point
Remove-Item -Path static/images/heart-ensc.png -ErrorAction SilentlyContinue
# Optionally, remove any other files you know were added after the rollback
