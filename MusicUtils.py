"""
MusicUtils.py
Shared tools for the Auto-Bard Songwriters.
Last Update: 2025-11-22 22:30 EST (v20.0 - Smart Scale Correction)
"""
import random

# ==========================================
# MUSIC THEORY CONSTANTS
# ==========================================
ALL_NOTES = [
    "L1", "L2", "L3", "L4", "L5", "L6", "L7",
    "M1", "M2", "M3", "M4", "M5", "M6", "M7",
    "H1", "H2", "H3", "H4", "H5", "H6", "H7"
]

SCALES = {
    # Pentatonic-ish scales for Wuxia feel
    "GONG": ["L1", "L2", "L3", "L5", "L6", "M1", "M2", "M3", "M5", "M6", "H1", "H2", "H3", "H5", "H6"], 
    "YU":   ["L6", "M1", "M2", "M3", "M5", "M6", "H1", "H2", "H3", "H5", "H6"], 
    "OUTLIER": ["L6", "M1", "M3", "M4", "M5", "M7", "H1", "H2", "H3", "H6"] 
}

# ==========================================
# MOTIF DEVELOPMENT 
# ==========================================

def develop_motif(motif, evolution="variation", scale=SCALES["YU"]):
    """
    Takes a base melody and evolves it.
    CRITICAL UPDATE: Now respects the 'scale' to prevent dissonance.
    """
    new_motif = []
    
    for instruction in motif:
        if len(instruction) == 3:
            notes, modifier, duration = instruction
        elif len(instruction) == 2:
            notes, duration = instruction
            modifier = None
        else:
            continue

        if notes == ["REST"]:
            new_motif.append(instruction)
            continue

        new_notes = []
        for n in notes:
            # If note is not in our mapped list, keep it as is
            if n not in ALL_NOTES:
                new_notes.append(n)
                continue
            
            # --- SMART SCALE LOGIC ---
            # 1. Determine where this note sits in the provided SCALE
            # If the note isn't in the scale, we default to finding it in ALL_NOTES
            # but we prioritize the scale index for movement.
            
            if n in scale:
                curr_idx = scale.index(n)
                pool = scale
            else:
                curr_idx = ALL_NOTES.index(n)
                pool = ALL_NOTES
            
            if evolution == 'variation':
                # Step up/down within the SCALE, not the chromatic list
                shift = random.choice([-1, 0, 1]) 
                new_idx = max(0, min(len(pool)-1, curr_idx + shift))
                new_notes.append(pool[new_idx])
                
            elif evolution == 'inversion':
                # Flip around the midpoint of the scale
                midpoint = len(pool) // 2
                diff = curr_idx - midpoint
                new_idx = max(0, min(len(pool)-1, midpoint - diff))
                new_notes.append(pool[new_idx])
                
            elif evolution == 'expansion':
                # Shift octaves if possible
                if n.startswith("L"): new_notes.append(n.replace("L", "M"))
                elif n.startswith("M"): new_notes.append(n.replace("M", "H"))
                else: new_notes.append(n) 
            else:
                new_notes.append(n) # Fallback
                
        if modifier:
            new_motif.append((new_notes, modifier, duration))
        else:
            new_motif.append((new_notes, duration))
            
    return new_motif

def extend_motif(motif, add_count=2, scale=SCALES["YU"]):
    """
    Appends notes from the scale to end of motif.
    """
    new_motif = list(motif)
    for _ in range(add_count):
        note = random.choice(scale)
        # Faster notes for extensions to avoid dragging
        duration = random.choice([0.5, 0.25])
        new_motif.append(([note], duration))
    return new_motif

def mutate_rhythm(motif):
    """
    Shuffles durations.
    """
    durations = [inst[-1] for inst in motif]
    random.shuffle(durations)
    
    new_motif = []
    for i, instruction in enumerate(motif):
        parts = list(instruction)
        parts[-1] = durations[i]
        new_motif.append(tuple(parts))
        
    return new_motif

def progressive_repeat(motif, count, scale=SCALES["YU"]):
    """
    Plays a motif 'count' times, applying evolutions AND extensions.
    """
    block = []
    evolutions = ['base', 'variation', 'extension', 'variation']
    
    for i in range(count):
        evo = evolutions[i % len(evolutions)]
        
        if evo == 'base':
            block.extend(motif)
        elif evo == 'extension':
            block.extend(extend_motif(motif, add_count=3, scale=scale))
        else:
            block.extend(develop_motif(motif, evolution=evo, scale=scale))
            
    return block

# ==========================================
# TECHNIQUE GENERATORS
# ==========================================

def tremolo(notes_list, duration, modifier=None, speed=0.125):
    count = int(duration / speed)
    block = []
    for _ in range(count):
        if modifier: block.append((notes_list, modifier, speed))
        else: block.append((notes_list, speed))
    return block

def dynamic_tremolo(notes_list, duration, modifier=None, start_speed=0.25, end_speed=0.05):
    block = []
    current_time = 0
    current_speed = start_speed
    while current_time < duration:
        if modifier: block.append((notes_list, modifier, current_speed))
        else: block.append((notes_list, current_speed))
        current_time += current_speed
        if current_speed > end_speed: current_speed -= 0.01
        elif current_speed < end_speed: current_speed += 0.01
        current_speed = max(0.02, current_speed)
    return block

def slide(start_note, end_note, duration):
    step_time = duration / 3
    return [
        ([start_note], step_time),
        ([start_note], "SHIFT", step_time), 
        ([end_note], step_time)
    ]

def ornament(note, duration, type="trill"):
    if type == "trill":
        fast = 0.1
        main = duration - (fast * 2)
        return [([note], fast), ([note], "SHIFT", fast), ([note], main)]
    else:
        return [([note], "CTRL", 0.15), ([note], duration - 0.15)]

def arpeggio(chord, note_duration=0.25, direction='up', modifier=None):
    notes = list(chord)
    if direction == 'down': notes.reverse()
    elif direction == 'random': random.shuffle(notes)
    block = []
    for note in notes:
        if modifier: block.append(([note], modifier, note_duration))
        else: block.append(([note], note_duration))
    return block

def strum(chord, duration=1.0, speed=0.05, modifier=None):
    strum_time = len(chord) * speed
    sustain_time = max(0, duration - strum_time)
    block = []
    for note in chord:
        if modifier: block.append(([note], modifier, speed))
        else: block.append(([note], speed))
    if sustain_time > 0: block.append((["REST"], sustain_time))
    return block

def chug(notes_list, count, duration=0.25):
    block = []
    for _ in range(count): block.append((notes_list, duration))
    return block

def rest(duration):
    return [(["REST"], duration)]

def style_apply(pattern, style_level="base", scale=SCALES["YU"]):
    new_pattern = []
    for instruction in pattern:
        if len(instruction) == 3: notes, modifier, duration = instruction
        elif len(instruction) == 2: notes, duration = instruction; modifier = None
        else: continue
        
        if notes == ["REST"]:
            new_pattern.append(instruction)
            continue

        if style_level == 'virtuoso':
            # Reduced probability of crazy fills to keep it grounded
            if duration >= 1.0 and random.random() > 0.6:
                scale_segment = [n for n in scale if n in ALL_NOTES[5:15]]
                fill_notes = random.sample(scale_segment, k=3)
                new_pattern.extend(arpeggio(fill_notes, 0.125, 'up'))
                new_pattern.append((random.choice(notes), 'SHIFT', 0.5))
            else: new_pattern.append(instruction)
        
        elif style_level == 'expressive':
            if random.random() < 0.3:
                new_pattern.extend(slide(notes[0], notes[0], duration)) 
            else: new_pattern.append(instruction)

        elif style_level == 'standard':
            new_pattern.append(instruction)
        
        elif style_level == 'mute':
            if random.random() > 0.7: new_pattern.append((["REST"], duration))
            else: new_pattern.append(instruction)
        else: new_pattern.append(instruction)
            
    return new_pattern

def check_length(notes, bpm=120):
    total_beats = sum(n[-1] for n in notes)
    seconds = total_beats * (60.0 / bpm)
    print(f"Section Length: {seconds:.1f} seconds ({total_beats} beats at {bpm} BPM)")