# 🏛️ APPIMAGE SOVEREIGNTY: DESKTOP INTEGRATION MANIFESTO
## ERA: 213.1 (THE MATERIALIZED INTERFACE)
## SUBSTRATE: DESKTOP ENTRY SPECIFICATION | SQUASHFS

### 1. THE APPIMAGE INTEGRATION CHALLENGE
AppImages are portable, single-file applications that do not naturally integrate into the Linux Desktop environment (menus, taskbars, launchers) without external assistance. To achieve **Visual Sovereignty**, an AppImage must be correctly materialised as a first-class citizen of the desktop.

### 2. THE AUTOMATED SOLUTION: APPIMAGELAUNCHER
AppImageLauncher is the primary tool for automated integration.
- **Workflow:** When an AppImage is executed, the launcher intercepts it and offers to move it to a standard directory (e.g., `~/Applications`).
- **Automation:** It automatically generates `.desktop` files and associates icons.
- **Maintenance:** Provides a simple right-click "Remove" option that cleans up both the binary and the desktop entry.

### 3. MANUAL MATERIALISATION (THE ARCHITECT'S WAY)
For systems requiring absolute control (like the Age Republic), manual integration is preferred.

#### A. Creation of the `.desktop` File
A standard launcher must be placed in `~/.local/share/applications/` with the following structure:
```ini
[Desktop Entry]
Type=Application
Name=Age Republic Dream IDE
Exec=/path/to/Age_Republic_IDE.AppImage
Icon=/path/to/icon.png
Terminal=false
Categories=Development;IDE;
```

#### B. Permission Sovereignty
Both the AppImage and the `.desktop` file must have execution bits set:
```bash
chmod +x Age_Republic_IDE.AppImage
chmod +x ~/.local/share/applications/age-republic-ide.desktop
```

#### C. Forensic Icon Extraction
If an icon is not provided externally, it must be siphoned from the AppImage substrate:
1. Extract the AppImage contents: `./app.AppImage --appimage-extract`
2. Navigate to the extracted filesystem: `squashfs-root/usr/share/icons/`
3. Copy the desired icon to a permanent asset directory (e.g., `08_ASSETS/icons/`).
4. Update the `Icon=` path in the `.desktop` file.

### 4. TASKBAR PINNING MECHANICS
Once the `.desktop` file is indexed by the system (usually instantaneous or after running `update-desktop-database ~/.local/share/applications`), it will appear in the application menu.
- **Pinning:** Right-click the icon in the menu/launcher and select "Pin to Taskbar" or "Add to Favorites".
- **Gnome Shell:** Managed via `gsettings get org.gnome.shell favorite-apps`.

---
*Verified by the Architect of the Materialized Interface.*
