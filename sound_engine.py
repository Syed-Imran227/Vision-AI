import winsound
import time
import threading

# Frequencies (Hz)
FREQ_LOW = 400
FREQ_MID = 600
FREQ_HIGH = 800
FREQ_SUCCESS = 1000
FREQ_ERROR = 200

# Durations (ms)
DUR_SHORT = 100
DUR_MED = 200
DUR_LONG = 400

def _beep(freq, dur):
    """Play a beep in a separate thread to avoid blocking"""
    def run():
        try:
            winsound.Beep(freq, dur)
        except:
            pass
    threading.Thread(target=run, daemon=True).start()

def _seq(sequence):
    """Play a sequence of (freq, dur) tuples"""
    def run():
        try:
            for freq, dur in sequence:
                winsound.Beep(freq, dur)
                time.sleep(0.05)
        except:
            pass
    threading.Thread(target=run, daemon=True).start()

def play_listening_start():
    """Rising tone: 'Ding'"""
    _seq([(FREQ_MID, DUR_SHORT), (FREQ_HIGH, DUR_SHORT)])

def play_listening_end():
    """Falling tone: 'Dong'"""
    _seq([(FREQ_HIGH, DUR_SHORT), (FREQ_MID, DUR_SHORT)])

def play_processing():
    """Subtle tick"""
    _beep(FREQ_MID, 50)

def play_success():
    """Happy chime"""
    _seq([(FREQ_HIGH, 100), (FREQ_SUCCESS, 200)])

def play_error():
    """Low buzz"""
    _seq([(FREQ_LOW, 200), (FREQ_ERROR, 300)])
