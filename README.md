# SafeState Core File Protection Engine

SafeState is a lightweight, autonomous local backup and disaster recovery utility designed for systems engineers and administrators. Unlike standard commercial backup software that relies on the active user session environment, SafeState is architected to interface directly with the underlying storage volume structure. This enables reliable data harvesting from pre-installation boot environments (Windows PE ISO) or elevated administration states without permission clashes or profile corruption.

## Architectural Highlights

* **Direct Disk Path Discovery:** Bypasses active environment variables (`%USERPROFILE%`) to programmatically scan `C:\Users\`, filtering out system defaults to identify true human data vectors.
* **Targeted Profile Harvesting:** Isolates and extracts high-priority user shell workspaces (`Desktop`, `Documents`, `Downloads`, `Pictures`) directly from the physical disk layout.
* **Live Shell Restoration Protocol:** Maps archived data back into the active operating system shell structures dynamically, utilizing system environment tracking to eliminate account-naming collision risks.
* **Graphical Cache Refresh:** Leverages the native Windows API (`shell32.SHChangeNotify`) to trigger an immediate interface redraw, populating user icons on the workspace in real time without requiring a system reboot.

## System Requirements

* **Operating System:** Windows 10 / 11 / Windows Server (Fully functional within WinPE custom ISO environments)
* **Language:** Python 3.x (Standard Library deployment)
* **Permissions:** Administrative Privileges (Required for global sector file extraction)

## Deployment & Usage

### 1. Execution
Launch the utility from an elevated command prompt or terminal environment:
```bash
python safestate.py