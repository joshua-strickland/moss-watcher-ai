# Moss Watcher: Song Analysis Notation Syntax

This document defines the standardized syntax used to describe timing, positions, and patterns in our YAML song analysis files. Agents and LLMs must strictly adhere to these rules to ensure consistent dataset parsing across all song analyses.

## 1. Timing and Position Format

All timing and positional references must be indicated using strict DAW notation format:
**`Bar.Beat.16th`**

- **Bar:** The measure number (starting at 1).
- **Beat:** The quarter-note beat within the bar (1 to 4 in 4/4 time).
- **16th:** The 16th-note division within the beat (1 to 4).

## 2. Indicating Duration and Spans

When denoting a span of time (e.g., an element that plays for 8 bars), use the exact start point and the exact end point (up to, but not including). The end position should cleanly line up with the start position of the following bar or section.

**Format:** `[Start_Position] - [End_Position]`

### Rules for Spans:
- **DO NOT** use relative terminology like "bar 1 to 8".
- **DO NOT** end a full-bar span on the last beat of a bar (e.g., `8.4.4`).
- **DO** use the start of the *next* bar to indicate the end of a span that lasts a full number of bars. 
  - *Example:* An 8-bar loop starting at the beginning of the song spans from `1.1.1 - 9.1.1`.
- If an element is present in *both* bar 15 and bar 16, its span is `15.1.1 - 17.1.1` (because it lasts through the entirety of bar 16, ending at the moment bar 17 begins).

### Example Sequence:
- Intro (16 bars): `1.1.1 - 17.1.1`
- Verse A (32 bars): `17.1.1 - 49.1.1`

## 3. Open-Ended Timings
If an element starts at a specific position and continues indefinitely (or until the end of the section), use the `and on` notation appended to the DAW position.
- **Correct:** `17.1.1 and on`
- **Incorrect:** `bar 17 and on`

## 4. Single Hits and Exact Placements
If an element hits exactly once or starts at a precise time without a defined span, use a single DAW coordinate.
- **Correct:** `8.1.1`
- **Incorrect:** `bar 8`
- **Correct:** `16.3.1` (Meaning bar 16, beat 3, first 16th note)

By following these strict parsing rules, an LLM reading these YAML files can precisely recreate the timeline of a track without ambiguity.

## 5. Ambiguous or Repeating Patterns
If a pattern repeats relative to the current bar and you want to denote the beat/16th positions without specifying an absolute bar number, use `x` as a wildcard for the bar.
- **Correct:** `x.2.1` or `x.4.3`
- **Incorrect:** `bar.2.2` or `beat 2`
