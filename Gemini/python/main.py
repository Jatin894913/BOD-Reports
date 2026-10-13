import sys
import os
from config import config
from folder_manager import FolderManager
from reports import W2WPRODReport, W2WUATReport, FTUATReport, BigulUATReport, BigulPRODReport, TTSQAReport

def main():
    # 1. Determine project root
    # If we are in 'python' folder, root is parent. Otherwise, it's current.
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "python":
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir
    
    # Change directory to project root to ensure all paths are consistent
    os.chdir(project_root)

    # 2. Load configuration
    config.load("common.env")
    config.load(".env")

    # Debug: Print the loaded values
    print(f"Debug: INFO_PATH = {config.get('INFO_PATH')}")
    print(f"Debug: SCRIP_PATH = {config.get('SCRIP_PATH')}")
    print(f"Debug: PATTERN = {config.get('PATTERN')}")

    # 3. Create folders
    FolderManager.create_daily_folders()

    # 4. Main Menu Loop
    try:
        while True:
            print("\n===== BOD REPORT GENERATOR (PYTHON) =====")
            print("1) W2W PROD Report")
            print("2) W2W UAT Report")
            print("3) FTUAT Report")
            print("4) BIGUL UAT Report")
            print("5) BIGUL PROD Report")
            print("6) TTS QA Report")
            print("7) Exit")
            
            choice = input("\nSelect report to run (1-7): ").strip()
            
            report = None
            if choice == "1": report = W2WPRODReport()
            elif choice == "2": report = W2WUATReport()
            elif choice == "3": report = FTUATReport()
            elif choice == "4": report = BigulUATReport()
            elif choice == "5": report = BigulPRODReport()
            elif choice == "6": report = TTSQAReport()
            elif choice == "7":
                print("Exiting BOD Report Generator. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            if report:
                try:
                    report.execute()
                except KeyboardInterrupt:
                    print("\n\n[!] Report generation interrupted by user.")
                except Exception as e:
                    print(f"\nAn error occurred while running the report: {e}")

                try:
                    again = input("\nWould you like to generate another report? (yes/no): ").strip().lower()
                    if again not in ['yes', 'y']:
                        print("Exiting BOD Report Generator. Goodbye!")
                        break
                except KeyboardInterrupt:
                    print("\nExiting BOD Report Generator. Goodbye!")
                    break

    except KeyboardInterrupt:
        print("\n\nExiting BOD Report Generator. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
