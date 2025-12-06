# AI Aimbot

An AI-powered aim assistance tool using YOLOv5 for real-time object detection.

## 🚀 Quick Start (Easy Installation)

### Requirements
- **Windows 10/11**
- **Python 3.11 or newer** - [Download here](https://www.python.org/downloads/)
  - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation!
- **NVIDIA GPU** (recommended) with CUDA support
  - AMD/CPU also supported but slower

### Installation Steps

1. **Download this repository**
   - Click the green "Code" button → "Download ZIP"
   - Extract the ZIP file

2. **Run the setup**
   - Double-click `SETUP.bat`
   - Wait 5-10 minutes for dependencies to install

3. **Run the aimbot**
   - Double-click `RUN_AIMBOT.bat`
   - Configure your settings in the GUI
   - Click "Start Aimbot" and select your game window

That's it! 🎉

## 🎮 How to Use

1. Launch the GUI by double-clicking `RUN_AIMBOT.bat`
2. Configure your settings:
   - **Capture Size**: Screen region to monitor (720x720 recommended)
   - **Mouse Speed**: How fast the aim moves (1.3x default)
   - **Confidence**: Detection threshold (0.2 default)
   - **Headshot Mode**: Aim for heads instead of center mass
3. Click "Start Aimbot"
4. Select the game window from the list
5. **Enable CAPS LOCK** to activate auto-aim
6. Press **P** (or your configured key) to stop

## ⚙️ Configuration

All settings can be adjusted in the GUI and are saved to `AI-Aimbot/config.py`:

- `screenShotHeight/Width`: Capture region size
- `aaMovementAmp`: Mouse movement multiplier
- `confidence`: Detection confidence threshold
- `headshot_mode`: Aim for heads (True/False)
- `visuals`: Show detection overlay (True/False)
- `centerOfScreen`: Prioritize center targets (True/False)

## 🛠️ Advanced Usage

### Manual Installation
```bash
python -m venv .venv
.venv\Scripts\activate
cd AI-Aimbot
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### Console Mode (No GUI)
```bash
.venv\Scripts\activate
cd AI-Aimbot
python main.py
```

### Custom Models
Place custom YOLOv5 models in `AI-Aimbot/customModels/` and update the code to load them.

## 📋 System Requirements

- **OS**: Windows 10/11
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: NVIDIA GPU with CUDA support recommended
- **Disk Space**: 2GB for installation
- **Python**: 3.11 or newer

## 🐛 Troubleshooting

**"Python is not installed"**
- Install Python from python.org
- Make sure "Add Python to PATH" was checked during installation

**Aimbot won't start**
- Make sure you ran `SETUP.bat` first
- Check that your antivirus isn't blocking it

**Tensor size errors**
- The latest version fixes this automatically
- Make sure you pulled the latest code

**Slow detection**
- Lower the capture size (640x640)
- Use a faster model (yolov5n)
- Ensure you have CUDA-enabled GPU

## ⚠️ Disclaimer

This tool is for educational purposes only. Using aim assistance in online multiplayer games may violate terms of service and result in bans. Use at your own risk.

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## 💬 Support

For support, join our Discord: https://discord.gg/rootkitorg
