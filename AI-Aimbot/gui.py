import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import sys
import os
from pathlib import Path

class AimbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Aimbot Controller")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="AI Aimbot", font=('Arial', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status indicator
        self.status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_label = ttk.Label(self.status_frame, text="● Stopped", 
                                      font=('Arial', 12), foreground='red')
        self.status_label.pack()
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="15")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Screen capture size
        ttk.Label(settings_frame, text="Capture Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.capture_size = ttk.Combobox(settings_frame, values=["640x640", "720x720", "800x800", "1024x1024"], 
                                         state="readonly", width=15)
        self.capture_size.set("720x720")
        self.capture_size.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Movement amplifier
        ttk.Label(settings_frame, text="Mouse Speed:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.movement_amp = ttk.Scale(settings_frame, from_=0.5, to=3.0, orient=tk.HORIZONTAL, length=200)
        self.movement_amp.set(1.3)
        self.movement_amp.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.amp_label = ttk.Label(settings_frame, text="1.3x")
        self.amp_label.grid(row=1, column=2, padx=(5, 0))
        self.movement_amp.configure(command=self.update_amp_label)
        
        # Confidence threshold
        ttk.Label(settings_frame, text="Confidence:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confidence = ttk.Scale(settings_frame, from_=0.1, to=0.9, orient=tk.HORIZONTAL, length=200)
        self.confidence.set(0.2)
        self.confidence.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.conf_label = ttk.Label(settings_frame, text="0.2")
        self.conf_label.grid(row=2, column=2, padx=(5, 0))
        self.confidence.configure(command=self.update_conf_label)
        
        # Headshot mode
        self.headshot_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Headshot Mode", variable=self.headshot_var).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Visuals
        self.visuals_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Show Visual Overlay", variable=self.visuals_var).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Center of screen prioritization
        self.center_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Prioritize Center Targets", variable=self.center_var).grid(
            row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Display CPS
        self.cps_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Display CPS in Console", variable=self.cps_var).grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Model selection
        ttk.Label(settings_frame, text="AI Model:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.model_var = ttk.Combobox(settings_frame, values=["yolov5s (Fast)", "yolov5m (Balanced)", "yolov5l (Accurate)"], 
                                      state="readonly", width=15)
        self.model_var.set("yolov5s (Fast)")
        self.model_var.grid(row=7, column=1, pady=5, padx=(10, 0))
        
        # Quit key
        ttk.Label(settings_frame, text="Quit Key:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.quit_key = ttk.Entry(settings_frame, width=5)
        self.quit_key.insert(0, "P")
        self.quit_key.grid(row=8, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start Aimbot", command=self.start_aimbot, width=20)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="■ Stop Aimbot", command=self.stop_aimbot, 
                                   width=20, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Save settings button
        ttk.Button(button_frame, text="💾 Save Settings", command=self.save_settings, width=20).grid(
            row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        instructions = (
            "1. Configure your settings above\n"
            "2. Click 'Start Aimbot' to begin\n"
            "3. Select the game window when prompted\n"
            "4. Enable CAPS LOCK to activate auto-aim\n"
            f"5. Press the Quit Key to stop"
        )
        ttk.Label(info_frame, text=instructions, justify=tk.LEFT).pack(anchor=tk.W)
        
        self.process = None
        self.load_settings()
        
    def update_amp_label(self, value):
        self.amp_label.config(text=f"{float(value):.1f}x")
        
    def update_conf_label(self, value):
        self.conf_label.config(text=f"{float(value):.1f}")
    
    def save_settings(self):
        """Save current settings to config.py"""
        try:
            size = self.capture_size.get().split('x')[0]
            model = self.model_var.get().split(' ')[0]
            
            config_content = f"""# Portion of screen to be captured (This forms a square/rectangle around the center of screen)
screenShotHeight = {size}
screenShotWidth = {size}

# Use "left" or "right" for the mask side depending on where the interfering object is, useful for 3rd player models or large guns
useMask = True
maskSide = "left"
maskWidth = 300
maskHeight = 450

# Autoaim mouse movement amplifier
aaMovementAmp = {self.movement_amp.get():.2f}

# Person Class Confidence
confidence = {self.confidence.get():.2f}

# What key to press to quit and shutdown the autoaim
aaQuitKey = "{self.quit_key.get()}"

# If you want to main slightly upwards towards the head
headshot_mode = {self.headshot_var.get()}

# Displays the Corrections per second in the terminal
cpsDisplay = {self.cps_var.get()}

# Set to True if you want to get the visuals
visuals = {self.visuals_var.get()}

# Smarter selection of people
centerOfScreen = {self.center_var.get()}

# ONNX ONLY - Choose 1 of the 3 below
# 1 - CPU
# 2 - AMD
# 3 - NVIDIA
onnxChoice = 1
"""
            with open('config.py', 'w') as f:
                f.write(config_content)
                
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        """Load settings from config.py if it exists"""
        try:
            import config
            self.capture_size.set(f"{config.screenShotHeight}x{config.screenShotWidth}")
            self.movement_amp.set(config.aaMovementAmp)
            self.confidence.set(config.confidence)
            self.quit_key.delete(0, tk.END)
            self.quit_key.insert(0, config.aaQuitKey)
            self.headshot_var.set(config.headshot_mode)
            self.cps_var.set(config.cpsDisplay)
            self.visuals_var.set(config.visuals)
            self.center_var.set(config.centerOfScreen)
        except:
            pass
    
    def start_aimbot(self):
        """Start the aimbot in a separate process"""
        try:
            # Save settings before starting
            self.save_settings()
            
            # Update UI
            self.status_label.config(text="● Running", foreground='green')
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Get the virtual environment python path
            venv_python = Path("../.venv/Scripts/python.exe")
            if not venv_python.exists():
                venv_python = Path(".venv/Scripts/python.exe")
            if venv_python.exists():
                python_cmd = str(venv_python)
            else:
                python_cmd = sys.executable
            
            # Start the aimbot process
            self.process = subprocess.Popen([python_cmd, "main.py"], 
                                           creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            # Monitor the process
            threading.Thread(target=self.monitor_process, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start aimbot: {str(e)}")
            self.stop_aimbot()
    
    def monitor_process(self):
        """Monitor the aimbot process and update UI when it stops"""
        if self.process:
            self.process.wait()
            self.root.after(0, self.on_process_stopped)
    
    def on_process_stopped(self):
        """Called when the process stops"""
        self.status_label.config(text="● Stopped", foreground='red')
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.process = None
    
    def stop_aimbot(self):
        """Stop the aimbot process"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
        self.on_process_stopped()

def main():
    root = tk.Tk()
    app = AimbotGUI(root)
    
    # Handle window close
    def on_closing():
        if app.process:
            if messagebox.askokcancel("Quit", "Aimbot is still running. Do you want to stop it and quit?"):
                app.stop_aimbot()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
