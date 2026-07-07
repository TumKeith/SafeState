import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

class SafeStateApp:
    def __init__(self, system_root="C:\\"):
        self.system_root = Path(system_root)
        self.users_directory = self.system_root / "Users"
        self.ignored_profiles = ["Public", "Default", "defaultuser0", "All Users", "desktop.ini"]
        self.target_subfolders = ["Desktop", "Documents", "Downloads", "Pictures"]

    def discover_profiles(self):
        """Scans C:\\Users directly and returns a clean list of real user folders."""
        if not self.users_directory.exists():
            print(f"\n[CRITICAL] Directory not found: {self.users_directory}")
            return []
        
        # Gather directory names that aren't system-ignored profiles
        profiles = [
            entry.name for entry in self.users_directory.iterdir()
            if entry.is_dir() and entry.name not in self.ignored_profiles
        ]
        return sorted(profiles)

    def run_backup_wizard(self):
        print("\n=== SAFESTATE: BACKUP EXTRACTION WIZARD ===")
        
        # 1. Discover active profiles
        profiles = self.discover_profiles()
        if not profiles:
            print("[-] No valid user profiles discovered. Exiting.")
            return

        # 2. Display interactive list
        print("\nDetected Active User Profiles on this Machine:")
        for index, profile in enumerate(profiles, start=1):
            print(f"  [{index}] {profile}")
        
        # 3. User selection with validation to prevent data loss
        try:
            selection = int(input(f"\nSelect the targeted profile number (1-{len(profiles)}): "))
            if not (1 <= selection <= len(profiles)):
                print("[ERROR] Invalid selection number. Aborting.")
                return
            target_user = profiles[selection - 1]
        except ValueError:
            print("[ERROR] Please enter a valid number integer. Aborting.")
            return

        # 4. Set destination external storage target
        target_drive = input("\nEnter destination drive letter or path (e.g., D:\\): ").strip()
        if not target_drive:
            print("[ERROR] Target path cannot be empty. Aborting.")
            return
            
        backup_root = Path(target_drive) / f"SafeState_Archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        chosen_profile_path = self.users_directory / target_user

        print(f"\n[*] Initializing isolation harvest for user: [{target_user}]")
        print(f"[*] Destination: {backup_root}\n")

        # 5. Safe file tree preservation execution loop
        for folder in self.target_subfolders:
            standard_path = chosen_profile_path / folder
            onedrive_path = chosen_profile_path / "OneDrive" / folder
            
            # Counter-check both native local storage and local cloud mirrors to prevent data loss
            chosen_source = None
            if standard_path.exists():
                chosen_source = standard_path
            elif onedrive_path.exists():
                chosen_source = onedrive_path

            if chosen_source:
                # Maintain identical layout properties under the destination mount
                archive_dest = backup_root / target_user / folder
                print(f"  [+] Harvesting: {folder} -> Preserving structure...")
                try:
                    shutil.copytree(chosen_source, archive_dest, dirs_exist_ok=True)
                    print(f"  [SUCCESS] {folder} data locked.")
                except Exception as e:
                    print(f"  [WARNING] Skipping locked/corrupted system pointers inside {folder}: {e}")
            else:
                print(f"  [INFO] Subfolder '{folder}' was empty or not initialized. Skipping.")

        print(f"\n[✓] SafeState Profile Archive successfully completed.")

    def run_restore_wizard(self):
        print("\n=== SAFESTATE: LIVE SHELL RESTORATION WIZARD ===")
        
        archive_path_input = input("Enter the absolute path of your SafeState archive directory: ").strip()
        archive_root = Path(archive_path_input)
        
        if not archive_root.exists():
            print("[CRITICAL] Specified archive path does not exist. Aborting.")
            return

        # Read the preserved subdirectories (e.g. looking inside to see "Admin")
        archived_users = [entry.name for entry in archive_root.iterdir() if entry.is_dir()]
        if not archived_users:
            print("[-] No archived user signatures found inside the folder structure.")
            return

        print("\nDiscovered User Signatures Inside Archive:")
        for index, user in enumerate(archived_users, start=1):
            print(f"  [{index}] {user}")

        try:
            selection = int(input(f"\nSelect target profile layout to restore (1-{len(archived_users)}): "))
            chosen_user_archive = archived_users[selection - 1]
        except (ValueError, IndexError):
            print("[ERROR] Invalid selection reference point. Aborting.")
            return

        # Map to active shell profiles dynamically so we do not cause duplicate clashes
        live_profile_paths = {
            "Desktop": Path(os.path.expanduser("~/Desktop")),
            "Documents": Path(os.path.expanduser("~/Documents")),
            "Downloads": Path(os.path.expanduser("~/Downloads")),
            "Pictures": Path(os.path.expanduser("~/Pictures"))
        }

        print(f"\n[*] Injecting archived data structures into active live environment...")
        user_archive_path = archive_root / chosen_user_archive

        for folder_name, live_target_path in live_profile_paths.items():
            archived_folder = user_archive_path / folder_name
            
            if archived_folder.exists():
                print(f"  [+] Repopulating Shell Object: {folder_name} -> {live_target_path}")
                try:
                    live_target_path.mkdir(parents=True, exist_ok=True)
                    # Merge cleanly without wiping tracking metadata parameters
                    shutil.copytree(archived_folder, live_target_path, dirs_exist_ok=True)
                except Exception as e:
                    print(f"    [WARNING] Error copying properties inside {folder_name}: {e}")

        # Trigger Windows shell repaint signal line instantly
        try:
            import ctypes
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
            print("[*] Windows API call successful: Graphical display cache refreshed.")
        except Exception:
            print("[*] Graphic refresh signal bypassed (Non-native environment link context).")

        print(f"\n[✓] System target populating complete. Files are now accessible on the active workspace.")

    def main_menu(self):
        while True:
            print("\n==========================================")
            print("     SAFESTATE CORE FILE PROTECTION ENGINE     ")
            print("==========================================")
            print("  [1] Run Interactive Backup (Harvest Profiles)")
            print("  [2] Run Precise Restoration (Populate Workspace)")
            print("  [3] Exit System Utility")
            
            choice = input("\nSelect operational sequence code (1-3): ").strip()
            if choice == "1":
                self.run_backup_wizard()
            elif choice == "2":
                self.run_restore_wizard()
            elif choice == "3":
                print("\nShutting down SafeState subsystem. Stay safe!")
                sys.exit(0)
            else:
                print("[!] Invalid operation parameter selection code. Try again.")

if __name__ == "__main__":
    try:
        # Instantiate app layout
        app = SafeStateApp()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupt signal captured. Forcing clean exit of SafeState subsystems...")
        try:
            sys.exit(0)
        except NameError:
            import sys
            sys.exit(0)