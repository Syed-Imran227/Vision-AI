# main.py

import threading
import sys
from ui_window import create_ui
from speech_engine import speak, listen_continuous
from command_handler import process_command

# Global shutdown flag
_shutdown_requested = False

def request_shutdown():
    """Request graceful shutdown of the application"""
    global _shutdown_requested
    _shutdown_requested = True

from sound_engine import play_listening_start, play_listening_end, play_processing

def nova_loop(ui):
    speak("Hello sir, Vision AI online. I am listening.")
    ui.set_nova("Hello sir, Vision AI online.")
    ui.set_status("Always Listening")

    for user_cmd in listen_continuous():
        # Check for shutdown request
        if _shutdown_requested:
            speak("Shutting down. Goodbye!")
            ui.set_nova("Shutting down. Goodbye!")
            ui.set_status("Offline")
            break
            
        if not user_cmd:
            continue

        # Feedback: Heard something
        play_listening_end()
        play_processing()

        ui.set_user(user_cmd)
        ui.set_status("Processing…")

        # Execute command
        try:
            response = process_command(user_cmd, ui)
            
            # Check if shutdown was requested by command
            if _shutdown_requested:
                ui.set_nova(response)
                speak(response)
                break

            ui.set_nova(response)
            speak(response)
            
        except Exception as e:
            print(f"Error processing command: {e}")
            ui.set_nova(f"Error: {str(e)}")
            speak("I encountered an error while processing that command.")

        if not _shutdown_requested:
            ui.set_status("Listening…")


def main():
    ui = create_ui()

    t = threading.Thread(target=nova_loop, args=(ui,), daemon=True)
    t.start()

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nVision AI shutting down...")
        request_shutdown()
    finally:
        # Cleanup resources
        cleanup_resources()
        
def cleanup_resources():
    """Clean up browser and other resources before exit"""
    try:
        from browser_control import _driver
        if _driver is not None:
            _driver.quit()
            print("Browser closed successfully")
    except Exception as e:
        print(f"Cleanup warning: {e}")
    
    # Give threads time to finish
    import time
    time.sleep(0.5)
    sys.exit(0)

if __name__ == "__main__":
    main()
