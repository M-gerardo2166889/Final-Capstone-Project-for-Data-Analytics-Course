"""
create_poverty_2014_2023.py
Author: Mike Gerardo
FINAL VERSION – MATCHES CLEAN FILE EXACTLY

This script:
    • Loads ACS S1701 poverty files (2014–2023)
    • Removes "Geography", "Universe", "Annotations", and other junk rows
    • Keeps ONLY the Maricopa County poverty estimate row
    • Forces schema to match 2014 exactly (master schema)
    • Outputs ACSST5Y2014_2023.csv (clean, identical to your good file)
"""

import pandas as pd
import os

POVERTY_DIR = r"C:\Users\mikeg\OneDrive\Documents\School\CIS 480\Capstone\Data\Poverty Rates Maricopa"
OUTPUT_FILE = os.path.join(POVERTY_DIR, "ACSST5Y2014_2023.csv")

# ------------------------------
# LOAD MASTER (2014)
# ------------------------------
master_path = os.path.join(POVERTY_DIR, "ACSST5Y2014.S1701-Data.csv")
master_df = pd.read_csv(master_path)

# Remove geography header rows
master_df = master_df[master_df["NAME"].str.contains("Maricopa", na=False)]

# Add year column
master_df["Year"] = 2014

# This is our LOCKED schema
master_columns = list(master_df.columns)

combined = [master_df]

# ------------------------------
# PROCESS YEARS 2015–2023
# ------------------------------
for year in range(2015, 2023 + 1):
    file_path = os.path.join(POVERTY_DIR, f"ACSST5Y{year}.S1701-Data.csv")

    if not os.path.exists(file_path):
        print(f"[WARN] Missing: {file_path}")
        continue

    df = pd.read_csv(file_path)

    # REMOVE GEOGRAPHY / ANNOTATION ROWS
    df = df[df["NAME"].str.contains("Maricopa", na=False)]

    # Add Year
    df["Year"] = year

    # Force schema: add missing, remove extras
    for col in master_columns:
        if col not in df.columns:
            df[col] = None

    df = df[master_columns]

    combined.append(df)

# ------------------------------
# CONCAT & SAVE
# ------------------------------
final_df = pd.concat(combined, ignore_index=True)
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"[DONE] Saved → {OUTPUT_FILE}")
