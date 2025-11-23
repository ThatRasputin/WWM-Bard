"""
flesh_and_bone.py
A dark, rhythmic martial track.
Inspired by '96 Quite Bitter Beings'.
v9.1: THE EXTENDED CUT (Smart Hand Optimized).
      - Riff Timing Fixed: Padded to 8 beats.
      - Arrangement: Verses (4 cycles), Bridge, Grand Chorus.
      - Verified for Bard v19.1 (Rest Safe).
      - Target: ~1:50 | BPM: 96
Last Update: 2025-11-23 15:15 EST
"""
import MusicUtils as utils
import random

def compose():
    TITLE = "Flesh and Bone (Smart v9.1)"
    BPM = 96 
    SCALE = utils.SCALES["YU"] 
    
    track = []

    # ==========================================
    # THE RIFF (Fixed to 8 Beats / 2 Bars)
    # ==========================================
    # PART 1: The Call (2 Beats Play + 2 Beats Rest)
    riff_head = [
        (["L6"], 0.5), (["M1"], 0.5), (["M3"], 0.5), (["L6"], 0.5),
        (["REST"], 2.0) 
    ]
    
    # PART 2: The Run (4 Beats Continuous)
    riff_tail = [
        (["L6"], 0.5), (["M1"], 0.5), 
        (["M3"], 0.5), (["M4"], 0.5), # The Bitter Note
        (["M3"], 0.5), (["M1"], 0.5), 
        (["L7"], 0.5), (["L5"], 0.5)  
    ]

    full_riff = riff_head + riff_tail 

    # ==========================================
    # SECTIONS
    # ==========================================

    def section_intro():
        t = []
        t.extend(utils.rest(0.5))
        t.extend(utils.dynamic_tremolo(["L2", "L6"], duration=4.0, start_speed=0.12, end_speed=0.08))
        t.extend(utils.ornament("M4", duration=1.0, type="trill")) 
        t.extend(utils.slide("M4", "M3", 1.0))
        return t

    def section_verse_extended(style='standard'):
        t = []
        
        # 1. Base Riff
        t.extend(full_riff)
        t.extend(full_riff)
        
        # 2. Heavy Riff
        heavy = []
        for instruction in full_riff:
            notes = instruction[0]
            if notes == ["REST"]: 
                heavy.append(instruction)
                continue
            
            if "L6" in notes: notes = ["L2", "L6"]
            heavy.append((notes, instruction[1]))
            
        if style == 'mute':
            t.extend(utils.style_apply(heavy, 'mute'))
            t.extend(utils.style_apply(heavy, 'mute'))
        else:
            t.extend(heavy)
            t.extend(heavy)
            
        return t

    def section_pre_chorus():
        t = []
        t.extend(utils.chug(["L6", "M1"], 4, 0.5)) 
        t.extend(utils.strum(["M1", "M3", "M4"], 2.0, 0.05)) 
        t.extend(utils.slide("M4", "M3", 0.5)) 
        t.extend(utils.strum(["M2", "M5"], 1.5, 0.05))
        return t

    def section_chorus_grand(loops=2):
        t = []
        progression = [
            (["L6", "M1", "M3"], 2.0), # Am
            (["M1", "M3", "M5"], 2.0), # C
            (["L5", "M2", "M5"], 4.0)  # G
        ]
        
        for i in range(loops):
            if i == 0 or i == 2: 
                 for chord, dur in progression:
                    t.extend(utils.strum(chord, duration=dur, speed=0.05))
            else: 
                 for chord, dur in progression:
                    t.extend(utils.arpeggio(chord, note_duration=0.2, direction='up'))
                    remain = dur - (len(chord)*0.2)
                    if remain > 0: t.extend(utils.strum(chord, remain, 0.05))
        return t

    def section_bridge_atmospheric():
        t = []
        t.extend(utils.rest(0.5))
        t.extend(utils.dynamic_tremolo(["L2"], 4.0, 0.2, 0.2)) 
        
        melody = ["H1", "M6", "M4", "M3"]
        for n in melody:
            t.extend(utils.ornament(n, duration=1.5, type="vibrato"))
            
        t.extend(utils.slide("M3", "L6", 2.0))
        return t

    def section_solo_extended():
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
        t = []
        high_notes = ["M3", "M4", "M3", "M1"] 
        low_notes = ["L6", "L2"]
        
        t.extend(utils.arpeggio(high_notes, 0.2, 'down'))
        t.extend(utils.chug(low_notes, 4, 0.5))
        t.extend(utils.arpeggio(high_notes, 0.15, 'random'))
        t.extend(utils.strum(["L1", "L5", "L6"], 6.0, 0.15)) 
        return t

    # ==========================================
    # ARRANGEMENT
    # ==========================================
    track.extend(section_intro())
    track.extend(section_verse_extended(style='standard'))
    track.extend(section_pre_chorus())
    track.extend(section_chorus_grand(loops=2))
    track.extend(section_verse_extended(style='mute'))
    track.extend(section_bridge_atmospheric())
    track.extend(section_solo_extended())
    track.extend(section_chorus_grand(loops=4))
    track.extend(section_outro_heavy())
    
    return {
        "title": TITLE,
        "bpm": BPM,
        "notes": track
    }