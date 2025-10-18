"""
Redis Helpdesk System - Main Entry Point
Run this to execute the complete lab demonstration
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and handle errors"""
    try:
        print(f"\n{'='*50}")
        print(f"Running {script_name}...")
        print(f"{'='*50}")
        result = subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ {script_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File {script_name} not found!")
        return False

def main():
    print("🚀 Redis Helpdesk System - Lab 3")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your Redis credentials.")
        print("See README.md for setup instructions.")
        return
    
    # Run the lab parts in sequence
    scripts = [
        "config.py",           # Part A: Connection test
        "part-b-model-setup.py",  # Part B: Data model setup
        "part-c-crud-ops.py"   # Part C: CRUD operations
    ]
    
    success_count = 0
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            print(f"\n❌ Stopping execution due to error in {script}")
            break
    
    print(f"\n{'='*50}")
    print(f"Lab execution completed: {success_count}/{len(scripts)} parts successful")
    
    if success_count == len(scripts):
        print("🎉 All parts completed successfully!")
        print("Check the Screenshots/ directory for execution results.")
    else:
        print("⚠️  Some parts failed. Check the error messages above.")
    
    print("\nFor cleanup, run: python delete.py")

if __name__ == "__main__":
    main()
