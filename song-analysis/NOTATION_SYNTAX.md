# Moss Watcher: Song Analysis Notation Syntax

This document defines the standardized syntax used to describe sounds, timing, positions, and patterns in our YAML song analysis files. Agents and LLMs must strictly adhere to these rules to ensure consistent dataset parsing across all song analyses.

## 1. Timing and Position Format

All timing and positional references must be indicated using strict DAW notation format:
**`Bar.Beat.16th`**

- **Bar:** The measure number, **relative to the start of the section** (bar 1 is the first bar of the section).
- **Beat:** The quarter-note beat within the bar (1 to 4 in 4/4 time).
- **16th:** The 16th-note division within the beat (1 to 4).

Positions are section-relative so that correcting one section's `duration_bars` never forces renumbering later sections. Absolute song positions are derived by adding up the `duration_bars` of the preceding sections.

## 2. Indicating Duration and Spans

When denoting a span of time (e.g., an element that plays for 8 bars), use the exact start point and the exact end point (up to, but not including). The end position should cleanly line up with the start position of the following bar or section.

**Format:** `[Start_Position] - [End_Position]`

### Rules for Spans:
- **DO NOT** use relative terminology like "bar 1 to 8".
- **DO NOT** end a full-bar span on the last beat of a bar (e.g., `8.4.4`).
- **DO** use the start of the *next* bar to indicate the end of a span that lasts a full number of bars.
  - *Example:* An 8-bar loop starting at the beginning of a section spans from `1.1.1 - 9.1.1`.
- If an element is present in *both* bar 15 and bar 16, its span is `15.1.1 - 17.1.1` (because it lasts through the entirety of bar 16, ending at the moment bar 17 begins).

## 3. Open-Ended Timings
If an element starts at a specific position and continues until the end of the section, use `end` as the end position.
- **Correct:** `17.1.1 - end`
- **Correct:** `1.1.1 - end` (plays for the whole section; replaces the old `constant`)
- **Incorrect:** `17.1.1 and on`, `bar 17 and on`

## 4. Single Hits and Exact Placements
If an element hits exactly once or starts at a precise time without a defined span, use a single DAW coordinate.
- **Correct:** `8.1.1`
- **Incorrect:** `bar 8`
- **Correct:** `16.3.1` (Meaning bar 16, beat 3, first 16th note)

## 5. Ambiguous or Repeating Patterns
If a pattern repeats relative to the current bar and you want to denote the beat/16th positions without specifying a bar number, use `x` as a wildcard for the bar. This is for describing a sound's `pattern`, not its `timing`.
- **Correct:** `x.2.1` or `x.4.3`
- **Incorrect:** `bar.2.2` or `beat 2`

## 6. The Sound Library

Each file has a top-level `sounds:` map. Each entry describes a sound once — what it *is* — keyed by a `snake_case` ID:

```yaml
sounds:
  prime_pluck:
    category: Synth - Pluck     # required
    label: prime synth pluck
    tonality: ...
    automation: ...
```

Section elements reference a sound with `sound: <id>`. The library holds only what the sound *is*; what it *plays* belongs to the section, so `pattern` is always written on the element:

```yaml
- sound: prime_pluck
  pattern: shifts between 8th & quarter notes
  notes: reverb amount changes to accent certain notes
  timing:
    hits: ["7.4.3"]
```

Any of `label`, `tonality` or `automation` set on the element overrides the library value for that section only. Use `notes` for what is different about the sound in that section (more reverb, louder hits) instead of rewriting `tonality`.

One-off sounds that appear in only one place may be written inline with `category` instead of `sound`.

## 7. The Timing Object

Every element has a `timing` object describing *when* it plays, using the notation from sections 1–4:

```yaml
timing:
  description: free text, for loose or approximate timing
  active:                 # spans where the sound plays
    - "1.1.1 - 9.1.1"
    - "17.1.1 - end"
  hits:                   # single moments (entries, one-shots, fills)
    - "12.4.1"
  repeat:                 # regular cycles
    - start: "13.1.1"
      every_bars: 4       # a new cycle starts every 4 bars
      length_bars: 2      # each occurrence lasts 2 bars
      until: "33.1.1"     # optional, end exclusive, defaults to end
  mutes:                  # spans or single positions where the sound drops out
    - "16.4.1"
    - "48.1.1 - end"
```

Rules:
- At least one of `active`, `hits` or `repeat` is required; `description` alone is not enough.
- `active`, `hits` and `repeat` combine: the sound plays wherever any of them says it does. `mutes` are then removed from that result.
- A single-position mute means the hit at that position is dropped.
- List spans in order and do not overlap them.
- When the real timing is loose ("roughly every 3-4 bars"), write the best approximation in the strict fields and explain it in `description`.

By following these strict parsing rules, an LLM or a timeline UI reading these YAML files can precisely recreate the timeline of a track without ambiguity.
