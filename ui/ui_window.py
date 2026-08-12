# ui_window.py

import tkinter as tk

class NovaUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VISION AI")

        # Frameless Glass Look
        self.root.geometry("500x500")
        self.root.configure(bg="#000000")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85) # Glass transparency
        self.root.overrideredirect(True) # Remove borders

        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 500) // 2
        self.root.geometry(f"500x500+{x}+{y}")

        # Make draggable
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Main Canvas for everything (to handle transparency better)
        self.canvas = tk.Canvas(
            self.root, width=500, height=500,
            bg="#000000", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Arc Reactor / Circle Animation
        self.center_x = 250
        self.center_y = 200
        
        # Outer Ring
        self.ring1 = self.canvas.create_oval(
            self.center_x-80, self.center_y-80,
            self.center_x+80, self.center_y+80,
            outline="#00f2ff", width=2
        )
        
        # Inner Rotating Arc
        self.arc_start = 0
        self.ring2 = self.canvas.create_arc(
            self.center_x-60, self.center_y-60,
            self.center_x+60, self.center_y+60,
            start=0, extent=120, style="arc",
            outline="#00f2ff", width=4
        )

        # Core
        self.core = self.canvas.create_oval(
            self.center_x-10, self.center_y-10,
            self.center_x+10, self.center_y+10,
            fill="#00f2ff", outline=""
        )

        # Text Elements
        self.status_text = self.canvas.create_text(
            250, 320, text="SYSTEM ONLINE",
            fill="#00f2ff", font=("Segoe UI", 12, "bold")
        )

        self.user_text = self.canvas.create_text(
            250, 360, text="",
            fill="#ffffff", font=("Segoe UI", 11), width=400, justify="center"
        )

        self.nova_text = self.canvas.create_text(
            250, 420, text="Vision AI: Ready",
            fill="#00f2ff", font=("Segoe UI", 11), width=400, justify="center"
        )

        self.is_running = True
        self.animate()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def animate(self):
        if not self.is_running: return
        
        # Rotate Arc
        self.arc_start = (self.arc_start + 10) % 360
        try:
            self.canvas.itemconfigure(self.ring2, start=self.arc_start)
        except: pass
        
        # Pulse Core
        import time
        pulse = (time.time() * 5) % 1
        
        try:
            self.root.after(50, self.animate)
        except: pass

    # UI update helpers
    def set_status(self, text):
        if not self.is_running: return
        try:
            self.root.after(0, lambda: self.canvas.itemconfigure(self.status_text, text=text.upper()))
        except: pass

    def set_user(self, text):
        if not self.is_running: return
        try:
            self.root.after(0, lambda: self.canvas.itemconfigure(self.user_text, text=text))
        except: pass

    def set_nova(self, text):
        if not self.is_running: return
        try:
            self.root.after(0, lambda: self.canvas.itemconfigure(self.nova_text, text=text))
        except: pass

    def minimize(self):
        if not self.is_running: return
        try: self.root.after(0, self.root.withdraw)
        except: pass

    def restore(self):
        if not self.is_running: return
        try: self.root.after(0, self.root.deiconify)
        except: pass

    def run(self):
        self.root.mainloop()


def create_ui():
    return NovaUI()