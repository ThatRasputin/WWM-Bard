"""
Bard.py
The Player Engine (Single-Thread Focus).
v19.1: SMART HAND HOTFIX.
       - Fixed: Filtered 'None' values from key lists to prevent crashes on REST instructions.
       - Retains 'Modifier Latching' from v19.0.
Last Update: 2025-11-23 15:15 EST
"""
import time
import ctypes
import msvcrt
import os
import json
import glob
import random

# ==========================================
# CONFIGURATION
# ==========================================
VK_ESCAPE = 0x1B        
COUNTDOWN_SEC = 5       
TIMEOUT_SECONDS = 20    
SONGS_DIR = "songs"     

# === TIMING SETTINGS ===
HUMANIZE_TIMING = True  
TIMING_VARIANCE = 0.002 
PRESS_DURATION = 0.03   # Short reliable tap
MOD_LEAD_TIME = 0.05    # Time to hold Shift before pressing note

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
    if hexKeyCode is None: return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    if hexKeyCode is None: return
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

def interruptible_sleep(duration):
    if duration <= 0: return False
    end_time = time.time() + duration
    while time.time() < end_time:
        if ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000:
            return True
        sleep_chunk = min(0.02, end_time - time.time())
        if sleep_chunk > 0:
            time.sleep(sleep_chunk)
    return False

# ==========================================
# PLAYER ENGINE
# ==========================================

def get_song_duration(notes, bpm):
    total_beats = sum(instruction[-1] for instruction in notes)
    return total_beats * (60.0 / bpm)

def play_song_from_file(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    title = data.get('title', 'Unknown')
    bpm = data.get("bpm", 120)
    
    if 'notes' in data: notes = data.get('notes', [])
    elif 'tracks' in data: notes = data['tracks'].get('Lead_Melody', [])
    else: return

    total_duration = get_song_duration(notes, bpm)
    elapsed_time = 0.0
    active_modifier = None 

    print(f"\n>>> NOW PLAYING: {title} <<<")
    print(f"(Press 'ESC' to stop)")
    ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE) # Clear buffer

    try:
        for i, instruction in enumerate(notes):
            # Parse Instruction
            if len(instruction) == 3: notes_raw, mod_req, duration = instruction
            else: notes_raw, duration = instruction; mod_req = None
            
            if isinstance(notes_raw, str): notes_raw = [notes_raw]
            
            # --- 1. MODIFIER MANAGEMENT (LATCHING) ---
            mod_code = KEYS.get(mod_req) if mod_req else None
            
            if active_modifier != mod_req:
                if active_modifier:
                    old_code = KEYS.get(active_modifier)
                    if old_code: ReleaseKey(old_code)
                
                if mod_req and mod_code:
                    PressKey(mod_code)
                    time.sleep(MOD_LEAD_TIME)
                
                active_modifier = mod_req

            # --- 2. NOTE PLAYBACK ---
            seconds_per_beat = 60.0 / bpm
            base_sleep = duration * seconds_per_beat
            actual_total_duration = base_sleep + random.uniform(0, TIMING_VARIANCE)
            
            start_press = time.time()
            
            # --- FIX v19.1: Filter None values (Rests) ---
            keys_to_press = [KEYS[n] for n in notes_raw if n in KEYS and KEYS[n] is not None]
            
            if keys_to_press:
                for k in keys_to_press: PressKey(k)
                time.sleep(PRESS_DURATION)
                for k in keys_to_press: ReleaseKey(k)
            
            press_overhead = time.time() - start_press
            
            # --- 3. LOOKAHEAD STRATEGY ---
            should_release_mod = True
            if i + 1 < len(notes):
                next_inst = notes[i+1]
                if len(next_inst) == 3: next_mod = next_inst[1]
                else: next_mod = None
                
                if next_mod == active_modifier:
                    should_release_mod = False
            
            if should_release_mod and active_modifier:
                if mod_code: ReleaseKey(mod_code)
                active_modifier = None

            # --- 4. SLEEP & DISPLAY ---
            timer_str = f"[{format_time(elapsed_time)} / {format_time(total_duration)}]"
            print(f"\rPlaying... {timer_str}   ", end="")
            
            remaining_time = max(0, actual_total_duration - press_overhead)
            if interruptible_sleep(remaining_time):
                print("\n[!] Music stopped by user.")
                if active_modifier and mod_code:
                    ReleaseKey(mod_code)
                return

            elapsed_time += (duration * (60.0 / bpm))
            
    finally:
        if active_modifier:
             k = KEYS.get(active_modifier)
             if k: ReleaseKey(k)
            
    print(f"\r[√] Song finished: {format_time(total_duration)}          \n")

def main():
    if not os.path.exists(SONGS_DIR): os.makedirs(SONGS_DIR)
        
    while True:
        files = glob.glob(os.path.join(SONGS_DIR, "*.json"))
        
        print("\n" + "="*40)
        print("   WHERE WINDS MEET - AUTO-BARD (v19.1)")
        print("="*40)
        
        if not files:
            print(f"No songs found in '{SONGS_DIR}/'.")
            input("Press Enter...")
            continue

        for i, fpath in enumerate(files):
            with open(fpath, 'r') as f:
                try:
                    meta = json.load(f)
                    bpm = meta.get("bpm", 120)
                    if 'notes' in meta: notes = meta['notes']
                    elif 'tracks' in meta: notes = meta['tracks'].get('Lead_Melody', [])
                    else: notes = []
                    print(f"{i+1}. {meta.get('title', 'Unknown')} [{format_time(get_song_duration(notes, bpm))}]")
                except:
                    print(f"{i+1}. [Corrupt File] {os.path.basename(fpath)}")
                
        print(f"Q. Quit")
        
        start_time = time.time()
        choice = None
        
        while True:
            if time.time() - start_time > TIMEOUT_SECONDS:
                choice = str(random.randint(0, len(files) - 1) + 1)
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