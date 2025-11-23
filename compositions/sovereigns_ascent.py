"""
sovereigns_ascent.py
A grand, sweeping Guqin piece.
v13.0: FLUIDITY UPDATE.
       - Optimized for Bard v19.
       - Removed safety rests in Soliloquy.
       - Tightened Waterfall Bridge timing.
Last Update: 2025-11-23 14:05 EST
"""
import MusicUtils as utils
import random

def compose():
    TITLE = "The Sovereign's Ascent (Fluid v13)"
    BPM = 96  
    SCALE = utils.SCALES["GONG"]
    
    track = []

    theme_main = [
        (["L5", "M2"], 1.0), (["M1", "M5"], 0.5), (["M2", "M6"], 1.0), (["M5", "H1"], 1.5),
        (["H2", "M6"], 1.0), (["H1", "M5"], 1.0), (["M6", "M3"], 0.5), (["M5", "L5"], 2.0)
    ]
    
    theme_counter = [
        (["H3", "H6"], 1.0), (["H2", "H5"], 1.0), (["H1", "H3"], 0.5), (["M6", "H1"], 0.5),
        (["M5", "M2"], 1.0), (["M3", "L6"], 1.0), (["L5", "M1"], 3.0)
    ]

    def movement_1_earth():
        t = []
        t.extend(utils.strum(["L1", "L5", "M2"], duration=4.0, speed=0.25))
        t.extend(utils.strum(["L2", "M1", "M5"], duration=4.0, speed=0.25))
        t.extend(utils.strum(["L5", "M2", "M6"], duration=4.0, speed=0.25))
        
        t.extend(utils.style_apply(theme_main, 'standard'))
        heavy_theme = utils.develop_motif(theme_main, evolution='expansion', scale=SCALE)
        t.extend(utils.style_apply(heavy_theme, 'expressive'))
        
        low_walk = ["L5", "L6", "M1", "M2", "M3", "M2", "M1", "L6"]
        for n in low_walk:
            t.extend(utils.strum([n, "L1"], duration=2.0, speed=0.15))
        return t

    def movement_2_wind():
        t = []
        t.extend(utils.slide("M2", "H2", 2.0))
        t.extend(utils.slide("H2", "M5", 2.0))
        
        inverted = utils.develop_motif(theme_main, evolution='inversion', scale=SCALE)
        t.extend(utils.style_apply(inverted, 'expressive'))
        
        inverted_var = utils.develop_motif(inverted, evolution='variation', scale=SCALE)
        t.extend(utils.style_apply(inverted_var, 'virtuoso'))
        
        textures = ["H5", "H6", "H3", "H2"]
        for n in textures:
            t.extend(utils.ornament(n, duration=3.0, type="trill"))
        return t

    def section_soliloquy():
        t = []
        # UPDATED: No Rests. Continuous flow using the new engine speed.
        melody = ["H5", "H2", "M6", "H1"]
        for n in melody:
            t.extend(utils.ornament(n, duration=2.5, type="vibrato")) 
            # Replaced rest with a quick slide transition
            t.extend(utils.slide(n, n, 0.5)) 
            
        t.extend(utils.slide("H2", "M5", 3.0))
        return t

    def movement_3_fire():
        t = []
        roots = ["M2", "M5", "M6", "H1", "M6", "M5", "M2", "L5"]
        for root in roots:
            t.extend(utils.chug([root, "L5"], count=4, duration=0.25)) 
            t.extend(utils.strum([root, "M5", "H2"], duration=3.0, speed=0.05)) 
            
        run_notes = ["M5", "M6", "H1", "H2", "H3", "H5"]
        t.extend(utils.arpeggio(run_notes, 0.15, 'up'))   
        t.extend(utils.arpeggio(run_notes, 0.15, 'down')) 
        t.extend(utils.chug(["H5"], 4, 0.25)) 
        t.extend(utils.arpeggio(run_notes, 0.15, 'random'))
        t.extend(utils.arpeggio(run_notes, 0.15, 'up'))
        t.extend(utils.strum(["H1", "H5"], 4.0, 0.05))
        return t

    def movement_4_water():
        t = []
        chords = [
            ["H5", "H3", "H1", "M6"], ["H3", "H2", "M6", "M5"], 
            ["H2", "H1", "M5", "M3"], ["H1", "M6", "M3", "M2"], ["M6", "M5", "M2", "L5"]
        ]
        
        for chord in chords:
            t.extend(utils.arpeggio(chord, note_duration=0.20, direction='down'))
            up_chord = chord[::-1] 
            t.extend(utils.strum(up_chord, duration=4.0, speed=0.15)) 
            t.extend(utils.ornament(chord[0], 2.0, "trill"))
            
        circle = ["M5", "M6", "H1", "M6"]
        t.extend(utils.arpeggio(circle, 0.2, 'up'))
        t.extend(utils.arpeggio(circle, 0.25, 'up')) 
        t.extend(utils.arpeggio(circle, 0.3, 'up'))  
        t.extend(utils.strum(["L1", "L5", "M1", "M5"], 6.0, 0.2))
        return t

    def section_finale():
        t = []
        t.extend(utils.dynamic_tremolo(["L5", "M2", "M5", "H2"], duration=10.0, start_speed=0.1, end_speed=0.3))
        
        final_chords = [
            (["L1", "L5", "M2"], 6.0),
            (["L2", "L6", "M3"], 6.0),
            (["L5", "M2", "M5", "H2"], 10.0) 
        ]
        
        for chord_data in final_chords:
            notes, dur = chord_data
            t.extend(utils.strum(notes, duration=dur, speed=0.2))
        return t

    track.extend(utils.rest(0.5))
    track.extend(movement_1_earth())
    track.extend(movement_2_wind())
    track.extend(section_soliloquy())
    track.extend(movement_3_fire())
    track.extend(movement_4_water())
    track.extend(utils.style_apply(theme_main, 'virtuoso'))
    track.extend(utils.style_apply(theme_counter, 'virtuoso'))
    track.extend(section_finale())
    
    return {
        "title": TITLE,
        "bpm": BPM,
        "notes": track
    }