
import subprocess
import os

import subprocess
import os

def run_script(script_name):
    path = os.path.join("scripts", script_name)
    if not os.path.exists(path):
        print(f"❌ Script not found: {path}")
        exit(1)

    print(f"\n--- Running {script_name} ---")
    result = subprocess.run(["python", script_name], cwd="scripts")
    if result.returncode != 0:
        print(f"❌ {script_name} failed.\n")
        exit(1)
    else:
        print(f"✅ {script_name} completed.\n")

def ensure_folders():
    for folder in ["data", "viz"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created folder: {folder}")

if __name__ == "__main__":
    ensure_folders()

    run_script("download_data.py")
    run_script("preprocess_data.py")
    run_script("regression_handicap.py")
    run_script("rolling_optimize_ratings.py")
    run_script("plot_rolling_ratings.py")

    print("🎉 All steps completed successfully.")

