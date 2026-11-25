---
name: song-analysis
description: >-
  Use this skill when creating, editing, validating, or querying Melodic House
  song analysis YAML files in song-analysis/, generating arrangement or
  drop-out reports, or running STFT frequency-band audio analysis with Python.
---

# Song Analysis Workflow

This skill governs how reference tracks are documented in `song-analysis/` and mined for structural, arrangement, and spectral patterns.

## Key References
Read these files before creating or analyzing track data:
- **Notation Rules:** [NOTATION_SYNTAX.md](../../../song-analysis/NOTATION_SYNTAX.md) — Mandatory `Bar.Beat.16th` timing format and sound library rules.
- **JSON Schema:** [song-schema.json](../../../song-analysis/song-schema.json) — Strict schema for `track_metadata`, `sounds`, `arrangement`, `category` enum values, and `timing` objects.
- **Analysis Objectives:** [ANALYSIS_GOALS.md](../../../song-analysis/ANALYSIS_GOALS.md) — Focal points when summarizing or comparing tracks across the dataset.
- **Audio Spectrum Script:** [frequency-analysis.py](../../../python/frequency-analysis.py) — Computes per-section average dB across 5 frequency bands from a `.wav` file + `.yaml` arrangement.

## 1. Authoring or Updating a Track YAML
1. Add the schema header on line 1 of every file in `song-analysis/`:
   ```yaml
   # yaml-language-server: $schema=./song-schema.json
   ```
2. Populate `track_metadata` (`artist`, `title`, `key_signature`, `bpm`, `time_signature`, `genre`).
3. Define reusable instruments once under top-level `sounds:` (keyed by `snake_case` IDs) using only valid `category` enum values from [song-schema.json](../../../song-analysis/song-schema.json). Keep `pattern` out of `sounds:`—what a sound *plays* belongs on the section element. Record quantitative Hz measurements (especially kick and bass fundamentals) under `frequencies:` (`fundamental_hz`, `fundamental_range_hz`, `span_hz`) rather than burying numbers inside `tonality`.
4. Write all positions in **section-relative** `Bar.Beat.16th` notation (`1.1.1` is always the downbeat of the section):
   - **End-exclusive spans:** An 8-bar loop at the start of a section is `1.1.1 - 9.1.1` (never `1.1.1 - 8.4.4`), or `17.1.1 - end` to run through the end of the section.
   - **Structured `timing` object:** Every element's `timing` must include at least one of `active`, `hits`, or `repeat` (not legacy free-text strings), using `mutes` to carve out pre-transition drop-outs (e.g., `mutes: ["16.3.1 - end"]`).

## 2. Mining Commonalities & Generating Reports
When asked to find patterns or summarize tracks across `song-analysis/*.yaml`, follow [ANALYSIS_GOALS.md](../../../song-analysis/ANALYSIS_GOALS.md):
1. **Element Timelines:** Track section lengths (`duration_bars`) and when foundational layers (kick, sub-bass, pads, arps, vocals) enter, filter open, or strip away.
2. **Transitory Elements & Drop-outs (Highest Priority):** Scan `mutes`, `hits`, `global_transitions`, and `pattern_variation` for:
   - **Micro-Cuts (1–2 beats):** Elements cutting at e.g. `16.3.1` or `16.4.1` before the next section.
   - **Drum Pockets (2–4 bars):** Kick/bass dropping out early (e.g., `13.1.1` or `15.1.1` in a 16-bar phrase).
   - **Transitory Fills:** Dry Foley hits, vocal chops, snare fills, or reverse swells triggered inside those vacuums.
3. **Report Formatting:** Always list the exact songs analyzed, group findings by arrangement technique (not song-by-song), cite concrete DAW coordinates, and save persistent reports to `song-analysis/reports/` (see [arrangement_similarities_7-27-26.md](../../../song-analysis/reports/arrangement_similarities_7-27-26.md) as a reference).

## 3. Running Audio Frequency Analysis
To measure spectral balance per arrangement section against a `.wav` file:
1. Point [frequency-analysis.py](../../../python/frequency-analysis.py) (or invoke `analyze_sections_from_yaml(wav_path, yaml_path)`) at the audio file and its matching YAML file.
2. Run using the workspace virtual environment (`python\.venv\Scripts\python.exe`) so `librosa`, `numpy`, and `pyyaml` are available.

## Validation
After creating or editing any `.yaml` file in `song-analysis/`, validate that it parses cleanly as YAML and conforms to [song-schema.json](../../../song-analysis/song-schema.json) (valid `category` enum strings, regex-compliant `Bar.Beat.16th` coordinates, and structured `timing` objects).
