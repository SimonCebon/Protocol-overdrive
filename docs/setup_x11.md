# Setting up X11 Forwarding on Windows (for Docker)

Since Docker runs a headless Linux system, it cannot display graphics (like a game window) on its own. We need to "forward" the video output from the Docker container to your Windows screen. This requires an **X Server**.

We recommend **VcXsrv** (Windows X Server).

## 1. Install VcXsrv
1.  Download **VcXsrv** from SourceForge: [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)
2.  Run the installer (default options are fine).

## 2. Launch XLaunch (IMPORTANT)
After installation, search for "XLaunch" in your Start Menu and run it. You must configure it **exactly** as follows for Docker to work:

1.  **Display Settings**: Select "Multiple windows". Click *Next*.
2.  **Client Startup**: Select "Start no client". Click *Next*.
3.  **Extra Settings**:
    *   [x] **Clipboard** (Optional, keeps copy-paste working)
    *   [x] **Native opengl** (Crucial for games/Pygame)
    *   [x] **Disable access control** (CRITICAL: This allows the Docker container to connect. Without this, it will fail.)
4.  Click *Next*, then *Finish*.

You should see a small X icon in your system tray.

## 3. Verify
Once running, try double-clicking `run_game.bat` again. The game window should now appear on your Windows desktop.
