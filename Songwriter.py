"""
Songwriter.py
Compiles composition modules into playable JSON files.
Last Update: 2025-11-22 20:45 EST (v11.0 - Added Duration Calc)
"""
import os
import json
import importlib.util
import sys
import random 
import glob

# CONFIG
COMPOSITIONS_DIR = "compositions"
OUTPUT_DIR = "songs"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[+] Created '{OUTPUT_DIR}' folder.")

def get_duration_str(song_data):
    """Calculates formatted duration (MM:SS) from song data."""
    bpm = song_data.get('bpm', 120)
    notes = song_data.get('notes', [])
    
    # Handle legacy multi-track if necessary
    if not notes and 'tracks' in song_data:
         notes = song_data['tracks'].get('Lead_Melody', [])

    if not notes:
        return "00:00"

    # Sum the last element of every instruction (the duration)
    total_beats = sum(instruction[-1] for instruction in notes)
    total_seconds = total_beats * (60.0 / bpm)
    
    m = int(total_seconds // 60)
    s = int(total_seconds % 60)
    return f"{m:02d}:{s:02d}"

def save_song(filename, song_data):
    path = os.path.join(OUTPUT_DIR, filename)
    duration_str = get_duration_str(song_data)
    
    # Check status before writing
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                existing_data = json.load(f)
            
            if existing_data == song_data:
                print(f"[=] Skipped (Unchanged): {song_data.get('title', filename)} [{duration_str}]")
                return
            
            status_msg = "[~] Overwrote"
        except Exception as e:
            status_msg = f"[!] Fixed Corrupt File ({e})"
    else:
        status_msg = "[+] Created"
    
    # Write file
    with open(path, 'w') as f:
        json.dump(song_data, f, indent=2)
    
    print(f"{status_msg}: {song_data.get('title', filename)} [{duration_str}] -> {path}")

def load_and_compile():
    print(f"\nScanning '{COMPOSITIONS_DIR}/' for tracks...\n")
    
    if not os.path.exists(COMPOSITIONS_DIR):
        os.makedirs(COMPOSITIONS_DIR)
        print(f"Created '{COMPOSITIONS_DIR}' folder.")
        return

    files = [f for f in os.listdir(COMPOSITIONS_DIR) if f.endswith('.py') and not f.startswith('__')]
    
    if not files:
        print("No composition files found.")
        return

    for filename in files:
        module_name = filename[:-3]
        file_path = os.path.join(COMPOSITIONS_DIR, filename)
        
        try:
            # CRITICAL: SEED THE RANDOMNESS
            random.seed(module_name)
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, 'compose'):
                song_data = module.compose()
                
                # Check for BOTH single-track ('notes') or multi-track ('tracks') content
                if 'title' in song_data and ('notes' in song_data or 'tracks' in song_data):
                    json_name = filename.replace(".py", ".json")
                    save_song(json_name, song_data)
                else:
                    print(f"[!] Error in {filename}: Returned dictionary is missing required 'title', 'notes', or 'tracks' keys.")
            else:
                print(f"[-] Skipped {filename}: No compose() function found.")
                
        except Exception as e:
            print(f"[!] Failed to compile {filename}: {e}")

if __name__ == "__main__":
    print("========================================")
    print("   WWM SONGWRITER ENGINE")
    print("========================================")
    ensure_output_dir()
    load_and_compile()
    print("\nDone! Run 'Bard.py' to play.")