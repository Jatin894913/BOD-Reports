import os
from datetime import datetime
from config import config

class FolderManager:
    @staticmethod
    def create_daily_folders():
        if not config.ENABLE_FOLDER_CREATION:
            print("Folder creation is disabled in config.")
            return

        try:
            screenshot_base = config.SCREENSHOT_BASE_PATH
            reports_base = "reports"
            now = datetime.now()
            
            # 1. Get Month name (e.g., "April")
            month_name = now.strftime("%B")
            
            # 2. Get current date as folder name (e.g., "15-04-2026")
            folder_name = now.strftime("%d-%m-%Y")
            
            # 3. Create Screenshot Folders
            FolderManager._create_structure(screenshot_base, month_name, folder_name, is_screenshot=True)
            
            # 4. Create Report Folders removed as requested
            
        except Exception as e:
            print(f"Error creating folders: {e}")

    @staticmethod
    def _create_structure(base_path, month, folder, is_screenshot):
        month_folder = os.path.join(base_path, month)
        main_folder = os.path.join(month_folder, folder)
        
        if not os.path.exists(main_folder):
            os.makedirs(main_folder, exist_ok=True)
            print(f"Created: {os.path.abspath(main_folder)}")
        
        if is_screenshot:
            sub_folders = ["FT UAT", "W2W PROD", "W2W UAT", "Webclient"]
            for sub in sub_folders:
                sub_dir = os.path.join(main_folder, sub)
                if not os.path.exists(sub_dir):
                    os.makedirs(sub_dir, exist_ok=True)
                    print(f"Created sub-folder: {sub}")
                
                if sub == "Webclient":
                    # Deep structure: Webclient/{Before 9, Pre-Market, After 9:15}/{Depth, Index, Scrip}
                    for time_label in ["Before 9", "Pre-Market", "After 9-15"]:
                        time_dir = os.path.join(sub_dir, time_label)
                        for type_label in ["Depth", "Index", "Scrip"]:
                            target_dir = os.path.join(time_dir, type_label)
                            if not os.path.exists(target_dir):
                                os.makedirs(target_dir, exist_ok=True)
                                print(f"Created deep sub-folder: {os.path.relpath(target_dir, sub_dir)}")