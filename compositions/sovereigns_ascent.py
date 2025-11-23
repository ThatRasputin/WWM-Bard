"""
sovereigns_ascent.py
A grand, sweeping Guqin piece.
v6.0: Increased Density and Tempo. Fixed Dissonance via MusicUtils v20.
Last Update: 2025-11-22 22:35 EST
"""
import MusicUtils as utils
import random

def compose():
    # ==========================================
    # SETTINGS
    # ==========================================
    TITLE = "The Sovereign's Ascent"
    BPM = 110 # Increased from 85 to reduce dragging
    SCALE = utils.SCALES["GONG"] 
    
    track = []

    # ==========================================
    # CORE MOTIFS (Thickened with Harmony)
    # ==========================================
    # We now use dyads (two notes) to make it sound fuller
    main_motif = [
        (["L5", "M2"], 1.0), # Chord
        (["M2", "M5"], 0.5),
        (["M5", "H1"], 2.0), # Held chord
        (["M6", "M5"], "SHIFT", 0.5), # Slide
    ]
    
    # More active secondary theme
    secondary_motif = [
        (["M5", "M2"], 1.0),
        (["M6", "M3"], 0.5),
        (["H1", "M5"], 0.5),
        (["H2", "M6"], 1.0),
        (["M5"], 1.0)
    ]

    # ==========================================
    # PHRASE BUILDERS
    # ==========================================
    
    def section_intro():
        t = []
        t.extend(utils.rest(0.5))
        # Faster sweeps
        t.extend(utils.strum(["L1", "L5", "M2"], duration=2.0, speed=0.1))
        t.extend(utils.strum(["L2", "L6", "M3"], duration=2.0, speed=0.1))
        t.extend(utils.strum(["L3", "M1", "M5", "H1"], duration=3.0, speed=0.08))
        # No empty rest here, sustain into theme
        return t

    def section_main_theme():
        t = []
        # progressive_repeat will now use the FIXED develop_motif (no bad notes)
        # Count increased to 4 to establish groove at higher tempo
        complex_run = utils.progressive_repeat(main_motif, count=4, scale=SCALE)
        t.extend(utils.style_apply(complex_run, style_level='expressive'))
        
        # Dense answer
        t.extend(utils.extend_motif(secondary_motif, add_count=4, scale=SCALE))
        return t

    def section_bridge():
        t = []
        chord_progression = [
            ["L6", "M3", "M6"],
            ["M1", "M5", "H1"],
            ["M2", "M6", "H2"]
        ]
        
        for i, chord in enumerate(chord_progression):
            # Tighter timing on arpeggios
            t.extend(utils.arpeggio(chord, note_duration=0.2, direction='up')) 
            t.extend(utils.arpeggio(chord, note_duration=0.1, direction='down'))
            # Fill the gaps with strums instead of silence
            if i == 1:
                t.extend(utils.strum(chord, duration=1.0, speed=0.05))
        return t

    def section_climax():
        t = []
        # Constant motion - no single note tapping
        t.extend(utils.dynamic_tremolo(["L5", "M2", "M5"], duration=3.0, start_speed=0.15, end_speed=0.05))
        
        run_notes = ["M2", "M3", "M5", "M6", "H1", "H2", "H3", "H5"]
        # Double chugs for density
        t.extend(utils.chug([run_notes[0], run_notes[2]], 4, 0.25))
        t.extend(utils.arpeggio(run_notes[4:], 0.15, 'up'))
        
        # Big chords
        t.extend(utils.strum(["M5", "H2", "H5"], duration=2.0, speed=0.05))
        t.extend(utils.strum(["M6", "H3", "H6"], duration=2.0, speed=0.05))
        t.extend(utils.strum(["H1", "H5"], duration=1.0, speed=0.05))
        return t

    def section_soliloquy():
        t = []
        # Faster pacing even in the slow part
        melody = ["M5", "M3", "M2", "L6", "L5"]
        for note in melody:
            t.extend(utils.ornament(note, duration=1.5, type="trill"))
            # Very short breaths only
            t.extend(utils.rest(0.25))
        return t

    def section_outro():
        t = []
        t.extend(utils.slide("H5", "M5", duration=2.0))
        t.extend(utils.strum(["L1", "L5", "M1", "M5", "H1"], duration=6.0, speed=0.2)) 
        return t

    # ==========================================
    # ARRANGEMENT
    # ==========================================
    
    track.extend(section_intro())                   
    track.extend(section_main_theme())        
    track.extend(section_bridge())
    track.extend(section_main_theme()) 
    
    track.extend(section_climax())                  
    track.extend(section_soliloquy())               
    
    track.extend(section_outro())                   
        
    return {
        "title": TITLE,
        "bpm": BPM,
        "notes": track
    }