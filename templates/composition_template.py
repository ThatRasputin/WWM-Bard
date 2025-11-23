"""
template.py
A blank canvas for the Jade Zither.
v1.0: Initial Setup.
Last Update: 2025-11-23
"""
import MusicUtils as utils
import random

def compose():
    # --- CONFIGURATION ---
    TITLE = "Untitled Composition"
    BPM = 100 # Standard Adagio is ~90-100, Allegro ~120
    
    # Select a scale to help with algorithmic generation (GONG, YU, or OUTLIER)
    CURRENT_SCALE = utils.SCALES["YU"] 
    
    track = []

    # --- DEFINITIONS ---
    # Define your main themes or riffs here
    main_theme = [
        (["L6", "M3"], 1.0), 
        (["M1"], 0.5), 
        (["M2"], 0.5), 
        (["L6"], 2.0)
    ]

    # --- SECTIONS ---
    def section_intro():
        t = []
        t.extend(utils.rest(1.0))
        # Example: A slow strum to start
        t.extend(utils.strum(["L1", "L5", "M1"], duration=4.0, speed=0.15))
        return t

    def section_main():
        t = []
        # Example: Play the theme, then play it with 'expressive' variations
        t.extend(utils.style_apply(main_theme, 'standard', scale=CURRENT_SCALE))
        t.extend(utils.style_apply(main_theme, 'expressive', scale=CURRENT_SCALE))
        return t

    def section_climax():
        t = []
        # Example: Fast Arpeggios
        chord = ["M6", "H1", "H3"]
        t.extend(utils.arpeggio(chord, note_duration=0.15, direction='up'))
        t.extend(utils.arpeggio(chord, note_duration=0.15, direction='down'))
        t.extend(utils.strum(chord, duration=2.0, speed=0.05))
        return t

    # --- ARRANGEMENT ---
    # Order your sections here
    track.extend(section_intro())
    track.extend(section_main())
    track.extend(section_climax())
    
    # Optional: Check expected length in console during compile
    utils.check_length(track, BPM)

    return {
        "title": TITLE,
        "bpm": BPM,
        "notes": track
    }