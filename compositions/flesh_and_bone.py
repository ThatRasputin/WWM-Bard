"""
flesh_and_bone.py
A dark, rhythmic martial track.
Inspired by '96 Quite Bitter Beings'.
v9.0: THE EXTENDED CUT.
      - Riff Timing Fixed: Padded to 8 beats (Standard 4/4) for better groove.
      - Arrangement Doubled: Verses now play 4 cycles (Clean x2, Heavy x2).
      - Added 'Atmospheric Bridge' and 'Grand Chorus' for duration.
      - Target: ~1:50 | BPM: 96
Last Update: 2025-11-23 15:00 EST
"""
import MusicUtils as utils
import random

def compose():
    TITLE = "Flesh and Bone (Extended v9)"
    BPM = 96 
    SCALE = utils.SCALES["YU"] 
    
    track = []

    # ==========================================
    # THE RIFF (Fixed to 8 Beats / 2 Bars)
    # ==========================================
    # PART 1: The Call (2 Beats Play + 2 Beats Rest)
    riff_head = [
        (["L6"], 0.5), (["M1"], 0.5), (["M3"], 0.5), (["L6"], 0.5),
        (["REST"], 2.0) # Extended rest to complete the 4/4 bar
    ]
    
    # PART 2: The Run (4 Beats Continuous)
    riff_tail = [
        (["L6"], 0.5), (["M1"], 0.5), 
        (["M3"], 0.5), (["M4"], 0.5), # The Bitter Note
        (["M3"], 0.5), (["M1"], 0.5), 
        (["L7"], 0.5), (["L5"], 0.5)  
    ]

    full_riff = riff_head + riff_tail # Total 8 Beats (approx 5s per cycle)

    # ==========================================
    # SECTIONS
    # ==========================================

    def section_intro():
        # ~5s
        t = []
        t.extend(utils.rest(0.5))
        t.extend(utils.dynamic_tremolo(["L2", "L6"], duration=4.0, start_speed=0.12, end_speed=0.08))
        t.extend(utils.ornament("M4", duration=1.0, type="trill")) 
        t.extend(utils.slide("M4", "M3", 1.0))
        return t

    def section_verse_extended(style='standard'):
        # 4 Cycles = ~20s
        t = []
        
        # 1. Base Riff (Play twice)
        t.extend(full_riff)
        t.extend(full_riff)
        
        # 2. Heavy Riff (Play twice)
        heavy = []
        for instruction in full_riff:
            notes = instruction[0]
            if notes == ["REST"]: 
                heavy.append(instruction)
                continue
            
            # Add Bass Octave
            if "L6" in notes: notes = ["L2", "L6"]
            heavy.append((notes, instruction[1]))
            
        if style == 'mute':
            t.extend(utils.style_apply(heavy, 'mute'))
            t.extend(utils.style_apply(heavy, 'mute'))
        else:
            t.extend(heavy)
            t.extend(heavy) # Double heavy
            
        return t

    def section_pre_chorus():
        # ~5s
        t = []
        t.extend(utils.chug(["L6", "M1"], 4, 0.5)) 
        t.extend(utils.strum(["M1", "M3", "M4"], 2.0, 0.05)) 
        t.extend(utils.slide("M4", "M3", 0.5)) 
        t.extend(utils.strum(["M2", "M5"], 1.5, 0.05))
        return t

    def section_chorus_grand(loops=2):
        # 8 Beats per loop (~5s per loop)
        t = []
        progression = [
            (["L6", "M1", "M3"], 2.0), # Am
            (["M1", "M3", "M5"], 2.0), # C
            (["L5", "M2", "M5"], 4.0)  # G
        ]
        
        for i in range(loops):
            # Evolving Texture
            if i == 0 or i == 2: # Strumming (Odd loops)
                 for chord, dur in progression:
                    t.extend(utils.strum(chord, duration=dur, speed=0.05))
            else: # Arpeggios (Even loops)
                 for chord, dur in progression:
                    t.extend(utils.arpeggio(chord, note_duration=0.2, direction='up'))
                    remain = dur - (len(chord)*0.2)
                    if remain > 0: t.extend(utils.strum(chord, remain, 0.05))
        return t

    def section_bridge_atmospheric():
        # ~10s
        t = []
        t.extend(utils.rest(0.5))
        # Spooky high notes over a drone
        t.extend(utils.dynamic_tremolo(["L2"], 4.0, 0.2, 0.2)) # Drone
        
        melody = ["H1", "M6", "M4", "M3"]
        for n in melody:
            t.extend(utils.ornament(n, duration=1.5, type="vibrato"))
            
        t.extend(utils.slide("M3", "L6", 2.0))
        return t

    def section_solo_extended():
        # ~15s
        t = []
        
        # 1. Fast Run
        scale_run = ["M1", "M3", "M5", "M6", "H1", "H2"]
        t.extend(utils.arpeggio(scale_run, 0.15, 'up')) 
        t.extend(utils.chug(["H2"], 4, 0.2))
        
        # 2. Bitter Bends
        t.extend(utils.ornament("M3", 1.0, "trill"))
        t.extend(utils.slide("M3", "M4", 0.5))
        t.extend(utils.chug(["M4"], 4, 0.2)) 
        
        # 3. Tapping Finale
        tap_notes = ["H1", "M6", "H2", "M5"]
        t.extend(utils.arpeggio(tap_notes, 0.12, 'random'))
        t.extend(utils.arpeggio(tap_notes, 0.12, 'up'))
        t.extend(utils.slide("M5", "L6", 2.0))
        return t

    def section_outro_heavy():
        # ~10s
        t = []
        high_notes = ["M3", "M4", "M3", "M1"] 
        low_notes = ["L6", "L2"]
        
        # Call
        t.extend(utils.arpeggio(high_notes, 0.2, 'down'))
        # Response
        t.extend(utils.chug(low_notes, 4, 0.5))
        # Final Call
        t.extend(utils.arpeggio(high_notes, 0.15, 'random'))
        # Final Slam
        t.extend(utils.strum(["L1", "L5", "L6"], 6.0, 0.15)) 
        return t

    # ==========================================
    # ARRANGEMENT
    # ==========================================
    
    # 1. Intro (~5s)
    track.extend(section_intro())
    
    # 2. Verse 1 (Clean x2, Heavy x2) -> ~20s
    track.extend(section_verse_extended(style='standard'))
    
    # 3. Pre-Chorus (~5s)
    track.extend(section_pre_chorus())
    
    # 4. Chorus 1 (2 Loops) -> ~10s
    track.extend(section_chorus_grand(loops=2))
    
    # 5. Verse 2 (Muted x2, Heavy x2) -> ~20s
    track.extend(section_verse_extended(style='mute'))
    
    # 6. Bridge (Atmospheric) -> ~10s
    track.extend(section_bridge_atmospheric())
    
    # 7. Solo (Extended) -> ~15s
    track.extend(section_solo_extended())
    
    # 8. Grand Chorus (4 Loops) -> ~20s
    track.extend(section_chorus_grand(loops=4))
    
    # 9. Outro -> ~10s
    track.extend(section_outro_heavy())
    
    # Total Estimate: ~115 seconds (1:55)
    
    return {
        "title": TITLE,
        "bpm": BPM,
        "notes": track
    }