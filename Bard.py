"""
Bard.py
The Player Engine (Single-Thread Focus).
Last Update: 2025-11-22 00:23 EST (v15.0 - Reverted to Single Track)
"""
import time
import ctypes
import msvcrt
import os
import json
import glob
import random
# Removed threading import

# ==========================================
# CONFIGURATION
# ==========================================
STOP_HOTKEY = 0x01      # ESC key scan code
COUNTDOWN_SEC = 5       # Seconds to switch window
TIMEOUT_SECONDS = 20    # Menu auto-pick timeout
SONGS_DIR = "songs"     

# === TIMING SETTINGS ===
HUMANIZE_TIMING = True  
TIMING_VARIANCE = 0.005 
PRESS_DURATION = 0.05   
MOD_LEAD_TIME = 0.15    

# ==========================================
# DIRECT INPUT SETUP
# ==========================================
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_ushort), ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

KEYS = {
    "L1": 0x2C, "L2": 0x2D, "L3": 0x2E, "L4": 0x2F, "L5": 0x30, "L6": 0x31, "L7": 0x32,
    "M1": 0x1E, "M2": 0x1F, "M3": 0x20, "M4": 0x21, "M5": 0x22, "M6": 0x23, "M7": 0x24,
    "H1": 0x10, "H2": 0x11, "H3": 0x12, "H4": 0x13, "H5": 0x14, "H6": 0x15, "H7": 0x16,
    "SHIFT": 0x2A, "CTRL": 0x1D, "REST": None
}

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def play_chord(note_data, duration, bpm):
    seconds_per_beat = 60.0 / bpm
    base_sleep = duration * seconds_per_beat
    actual_total_duration = base_sleep + random.uniform(0, TIMING_VARIANCE)

    keys_to_press = []
    modifier = None

    if len(note_data) == 2:
        notes_raw, _ = note_data 
    elif len(note_data) == 3:
        notes_raw, modifier, _ = note_data
    else:
        notes_raw = note_data 

    if isinstance(notes_raw, str): notes_raw = [notes_raw]

    for n in notes_raw:
        k = KEYS.get(n)
        if k: keys_to_press.append(k)

    mod_code = KEYS.get(modifier) if modifier else None
    
    if keys_to_press:
        # EXECUTION SEQUENCE (Identical to previous single-track logic)
        if mod_code:
            PressKey(mod_code)
            time.sleep(MOD_LEAD_TIME)
        for k in keys_to_press:
            PressKey(k)
        time.sleep(PRESS_DURATION)
        for k in keys_to_press:
            ReleaseKey(k)
        if mod_code:
            time.sleep(0.01)
            ReleaseKey(mod_code)
        
        overhead = PRESS_DURATION + (MOD_LEAD_TIME if mod_code else 0) + (0.05 if mod_code else 0)
        time.sleep(max(0, actual_total_duration - overhead))
    else:
        time.sleep(actual_total_duration)

def get_song_duration(notes, bpm):
    total_beats = 0
    for instruction in notes:
        total_beats += instruction[-1]
    return total_beats * (60.0 / bpm)

def play_song_from_file(filepath):
    # No global stop flag needed in single-thread mode
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    title = data.get('title', 'Unknown')
    bpm = data.get("bpm", 120)
    
    # Check for both formats: use 'notes' key if available, else flatten 'tracks'
    if 'notes' in data:
        notes = data.get('notes', [])
    elif 'tracks' in data:
        # CONVERSION: Flatten all tracks into one sequence (simulating threads)
        # This is where we manually interleave the notes if we had multiple tracks
        print("[!] Warning: Converting multi-track JSON to single-thread sequence.")
        # NOTE: For simplicity and to fix the noise issue, we will only play the LEAD track.
        notes = data['tracks'].get('Lead_Melody', [])
    else:
        print("[!] Error: No valid 'notes' or 'tracks' found.")
        return

    total_duration = get_song_duration(notes, bpm)
    elapsed_time = 0.0

    print(f"\n>>> NOW PLAYING: {title} <<<")
    print(f"(Press 'ESC' to stop)")

    try:
        for instruction in notes:
            if ctypes.windll.user32.GetAsyncKeyState(0x1B) & 0x8000:
                print("\n[!] Music stopped by user.")
                return
            
            timer_str = f"[{format_time(elapsed_time)} / {format_time(total_duration)}]"
            print(f"\rPlaying... {timer_str}   ", end="")
            
            duration = instruction[-1]
            play_chord(instruction, duration, bpm)
            elapsed_time += (duration * (60.0 / bpm))
            
    finally:
        pass
            
    print(f"\r[√] Song finished: {format_time(total_duration)}          \n")

def main():
    if not os.path.exists(SONGS_DIR):
        os.makedirs(SONGS_DIR)
        
    while True:
        files = glob.glob(os.path.join(SONGS_DIR, "*.json"))
        
        print("\n" + "="*40)
        print("   WHERE WINDS MEET - AUTO-BARD")
        print("="*40)
        
        if not files:
            print(f"No songs found in '{SONGS_DIR}/'.")
            input("Press Enter...")
            continue

        for i, fpath in enumerate(files):
            with open(fpath, 'r') as f:
                meta = json.load(f)
                print(f"{i+1}. {meta.get('title', 'Unknown')}")
        print(f"Q. Quit")
        
        start_time = time.time()
        choice = None
        
        while True:
            if time.time() - start_time > TIMEOUT_SECONDS:
                rnd_idx = random.randint(0, len(files) - 1)
                choice = str(rnd_idx + 1)
                break
            if msvcrt.kbhit():
                choice = msvcrt.getwche().lower()
                break
            time.sleep(0.1)

        if choice == 'q': break
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                print(f"\n[Loading]...")
                for i in range(COUNTDOWN_SEC, 0, -1):
                    print(f"Starting in {i}...", end="\r")
                    time.sleep(1)
                play_song_from_file(files[idx])
        else:
            print("\nInvalid selection.")

if __name__ == "__main__":
    main()