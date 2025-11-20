"""
create_pm_2014_2023.py
Author: Mike Gerardo

FINAL VERSION – MATCHES CLEAN PM FILE EXACTLY

This script:
    • Loads PM2.5 EPA files (2014–2023)
    • Keeps ONLY Maricopa County rows
    • Forces each year to match 2014's schema exactly
    • Adds a Year column
    • Outputs ad_viz_plotval_data_2014_2023.csv cleanly
"""

import pandas as pd
import os

# ------------------------------
# PATH WHERE YOUR PM FILES LIVE
# ------------------------------
PM_DIR = r"C:\Users\mikeg\OneDrive\Documents\School\CIS 480\Capstone\Data\PM_index"

OUTPUT_FILE = os.path.join(PM_DIR, "ad_viz_plotval_data_2014_2023.csv")

# ------------------------------
# LOAD MASTER (2014)
# ------------------------------
master_path = os.path.join(PM_DIR, "ad_viz_plotval_data_2014.csv")

if not os.path.exists(master_path):
    raise FileNotFoundError("2014 PM file missing — cannot build master schema.")

print(f"[MASTER] Loading schema from: {master_path}")

master_df = pd.read_csv(master_path)

# Keep ONLY Maricopa County
master_df = master_df[master_df["County"].str.contains("Maricopa", na=False)]

master_df["Year"] = 2014

# Lock in schema
master_columns = list(master_df.columns)

combined_frames = [master_df]

# ------------------------------
# PROCESS YEARS 2015–2023
# ------------------------------
for year in range(2015, 2023 + 1):
    file_path = os.path.join(PM_DIR, f"ad_viz_plotval_data_{year}.csv")

    if not os.path.exists(file_path):
        print(f"[WARN] Missing: {file_path}")
        continue

    print(f"[INFO] Loading: {file_path}")

    df = pd.read_csv(file_path)

    # KEEP ONLY MARICOPA COUNTY
    df = df[df["County"].str.contains("Maricopa", na=False)]

    # Add year
    df["Year"] = year

    # FORCE SCHEMA MATCH
    # 1. Add missing columns
    for col in master_columns:
        if col not in df.columns:
            df[col] = None

    # 2. Drop extra columns
    df = df[master_columns]

    combined_frames.append(df)

# ------------------------------
# CONCAT & SAVE OUTPUT
# ------------------------------
final_df = pd.concat(combined_frames, ignore_index=True)
final_df.to_csv(OUTPUT_FILE, index=False)

print("\n[OK] PM dataset successfully created.")
print(f"[DONE] Saved → {OUTPUT_FILE}")
