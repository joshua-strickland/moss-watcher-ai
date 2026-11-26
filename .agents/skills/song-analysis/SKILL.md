---
name: song-analysis
description: >-
  Use this skill when creating, editing, validating, or querying Melodic House
  song analysis YAML files in song-analysis/, generating arrangement or
  drop-out reports.
---

# Song Analysis Workflow

This skill governs how reference tracks are documented in `song-analysis/` and mined for structural, arrangement, and spectral patterns.

## Key References
Read these files before creating or analyzing track data:
- **Notation Rules:** [NOTATION_SYNTAX.md](../../../song-analysis/NOTATION_SYNTAX.md) — Mandatory `Bar.Beat.16th` timing format and sound library rules.
- **JSON Schema:** [song-schema.json](../../../song-analysis/song-schema.json) — Strict schema for `track_metadata`, `sounds`, `arrangement`, `category` enum values, and `timing` objects.

## 1. Authoring or Updating a Track YAML
1. Add the schema header on line 1 of every file in `song-analysis/`:
   ```yaml
   # yaml-language-server: $schema=./song-schema.json
   ```
2. Populate `track_metadata` (`artist`, `title`, `key_signature`, `bpm`, `time_signature`, `genre`).
3. Define reusable instruments once under top-level `sounds:` (keyed by `snake_case` IDs) using only valid `category` enum values from [song-schema.json](../../../song-analysis/song-schema.json). Keep `pattern` out of `sounds:`—what a sound *plays* belongs on the section element. Record quantitative Hz measurements (especially kick and bass fundamentals) under `frequencies:` (`fundamental_hz`, `fundamental_range_hz`, `span_hz`) rather than burying numbers inside `tonality`.
   - **Pay special attention to signature Melodic House sound groups when documenting tracks:**
     - **Progressive Drum & Percussion Stacking (`Drums - Hats`, `Drums - Shakers`, `Drums - Snare`, `Drums - Clap`, `Drums - Rides`):** Log distinct hat/shaker/snare layers separately so mid-section entries (e.g., `17.1.1 - end`) are preserved, and record when existing drums step up in volume, shed a hi-cut filter, or densify their rhythm in `notes`, `automation`, or `pattern_variation`.
     - **Novel / Non-Standard Percussion (`Drums - Other Percussive`):** Actively listen for and log odd percussive ear-candy outside the standard 4-on-the-floor kick/hat/snare kit—e.g., metallic/cowbell-like hits, tonal/cutoff/sonar toms, woodblocks, treble clicks, or steel-drum-like hits—noting their syncopated `pattern` and how they keep the groove feeling fresh.
     - **Pads & Atmospheric Washes (`Synth - Pad`, `Synth - Granular Pad`, plus related `Synth - Swell`, `Vocals - Atmosphere`, `Vocals - Swell`):** Distinguish sustained chordal pads from granular/textured washes and multi-bar swells, noting filter character (low-passed, band-passed, resonant), reverb tail length, and which sections they occupy.
     - **Synth Plucks (`Synth - Pluck`, and closely paired `Synth - Arp`):** As the primary driving melodic element in Melodic House, carefully document the main pluck (and any secondary/transitionary plucks), capturing waveform/filter character, delay/reverb space, rhythmic `pattern` (syncopated motif vs. continuous pulse vs. spaced phrases), and cutoff `automation` across sections.
4. Write all positions in **section-relative** `Bar.Beat.16th` notation (`1.1.1` is always the downbeat of the section):
   - **End-exclusive spans:** An 8-bar loop at the start of a section is `1.1.1 - 9.1.1` (never `1.1.1 - 8.4.4`), or `17.1.1 - end` to run through the end of the section.
   - **Structured `timing` object:** Every element's `timing` must include at least one of `active`, `hits`, or `repeat` (not legacy free-text strings), using `mutes` to carve out pre-transition drop-outs (e.g., `mutes: ["16.3.1 - end"]`).

## 2. Mining Commonalities & Generating Reports
This is the main goal of analyzing songs: to find commonalities between analyzed songs and create a report on the similarities between them.

The aim is to extract recurring arrangement patterns, structural techniques, and instrumentation timelines from the provided Melodic House song analyses to inform the "Moss Watcher" production style.

When asked to find patterns or summarize tracks across `song-analysis/*.yaml`, follow these instructions:

> **Skip Incomplete / Stub Files:** Before analyzing, filter out and skip any `.yaml` file whose `arrangement` property is empty (`null` or `[]`) or contains only placeholder sections with no `elements` populated. Do **not** include skipped stub songs in calculations or in the report's analyzed-songs list.

### 1. Element Timelines (Beginnings and Ends)
- Track exactly **what elements play at what times**.
- Identify patterns in how tracks are arranged and layered. For example, note when the main kick typically enters, when the sub bass is introduced, and when atmospheric pads or vocals swell in and out. Note what sections they typically occur in
- Observe the duration of elements and how they define the energy of different sections (Intros, Verses, Breakdowns, Drops, Outros).

### 2. Transitory Elements & Drop-outs (CRITICAL)
The most important aspect of this analysis is identifying **transitory elements**—specifically when instruments cut out or come in *just before* a new section begins. You must place a heavy emphasis on finding where elements (such as kicks, sub bass, snares, or the entire mix) stop early.

**Specifically scan the YAML for:**
- **Micro-Cuts (1-2 Beats):** Look for elements cutting out precisely on the 3rd or 4th beat of the final bar of a section (e.g., stopping at `16.3.1` or `16.4.1` prior to a drop at `17.1.1`).
- **Medium-cuts (1-4 Bars):** Look for foundational elements (kicks/bass) dropping out one to several bars early (e.g., stopping at `13.1.1` or `15.1.1` or `16.1.1` in a 16-bar phrase) to create an empty, tension-building pocket.
- **Transitory Fills:** Note any specific elements that hit *during* these vacuums (e.g., a solitary vocal chop, a tom fill, or a snare hit).
- Scan fields like `global_transitions` and `pattern_variation` for explicit mentions of these cuts.

### 3. Signature Melodic House Elements (Drum Stacking, Percussive Ear-Candy, Pads, and Synth Plucks)
Dedicated sections of your analysis and commonality reports should examine how tracks deploy these core pillars and **which sections they play in**:
- **Progressive Drum & Percussion Layer Stacking (`Drums - *`):**
  - Identify how percussive stacks evolve as sections progress—such as stacking sharper/upbeat hi-hats, shakers, or rides on top of foundational hats, layering claps with snares, or boosting snare/hat volume and high-frequency brightness (e.g., removing a hi-cut filter).
  - Scan `timing.active` start offsets (e.g., `9.1.1`, `17.1.1`, `25.1.1`, `33.1.1`), `notes`, `automation`, and `pattern_variation`—as well as Verse 1 vs. Verse 2 or Chorus A vs. Chorus B differences—to pinpoint **when** percussive stack changes or volume/filter adjustments happen.
  - Quantify **how many bars typically pass** before a new percussive layer is added or an existing drum sound gets louder/brighter (e.g., every 8 bars, 16 bars, or 32 bars within a section, or across section boundaries).
- **Odd / Novel Percussion (`Drums - Other Percussive`):**
  - Melodic House relies heavily on unusual percussive hits beyond the standard 4-on-the-floor kick, hat, and snare—such as metallic hits, tonal/cutoff toms, rim/wood hits, or treble clicks—to introduce novelty and keep listeners engaged over long arrangements.
  - Track *what* these sounds are (`tonality`), *how* they sit rhythmically against the 4/4 pulse (`pattern`, e.g., off-beat `x.1.3`/`x.3.3` syncopation, sparse call-and-response `hits`, or multi-bar `repeat` cycles), and *when* they enter or swap out (e.g., mid-verse groove evolutions, breakdown textures, or pre-section fills).
- **Pads & Atmospheric Layers (`Synth - Pad`, `Synth - Granular Pad`, and adjacent `Synth - Swell`, `Vocals - Atmosphere`, `Vocals - Swell`):**
  - Identify how sustained harmonic pads, granular textures, and ambient vocal/synth swells establish space and emotional continuity.
  - Compare **which sections they play in** across tracks—for example, setting the initial atmosphere in **Intros**, sitting filtered or sidechained beneath **Verses/Choruses**, stepping forward to carry **Breakdowns/Bridges** when drums and bass drop out, or ringing into **Outros**—and note how multiple pad layers stack, alternate, or sweep their filter cutoffs between sections.
- **Synth Plucks (`Synth - Pluck`, alongside supporting `Synth - Arp` layers):**
  - Synth plucks are the primary driving melodic force in Melodic House, typically carrying the core hook or chordal pulse.
  - Analyze commonalities in **how plucks are designed and sequenced** (warm low-passed saw plucks, key-tracked or LFO/automated filter cutoffs, dotted-8th/16th delays, long reverb tails; continuous 8th/16th rhythms vs. dotted syncopation vs. spaced melodic phrases; main lead plucks vs. secondary counter/transition plucks).
  - Map **which sections plucks drive and how they evolve**—such as entering muted/filtered in **Intros**, anchoring the groove in **Verses**, opening their low-pass cutoff through **Builds** to peak brightness in **Drops/Choruses**, and filtering down or soloing in **Breaks/Outros**.

### 4. Output Requirements
When generating reports based on these analyses:
1. **List the songs** that were referenced/analyzed.
2. Provide **specific DAW notation coordinates** (e.g., `15.1.1`) as examples of the techniques you find.
3. Group the findings logically by arrangement techniques rather than just summarizing one song at a time.
4. Leave a report under song-analysis/reports

*(Note: Always refer to `NOTATION_SYNTAX.md` to properly understand how timing and ambiguity are represented in this dataset).*


## Validation
After creating or editing any `.yaml` file in `song-analysis/`, validate that it parses cleanly as YAML and conforms to [song-schema.json](../../../song-analysis/song-schema.json) (valid `category` enum strings, regex-compliant `Bar.Beat.16th` coordinates, and structured `timing` objects).
