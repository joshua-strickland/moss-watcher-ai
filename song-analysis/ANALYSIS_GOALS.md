# Moss Watcher: AI Analysis Goals

This document outlines the core objectives and specific focal points for any AI or agent tasked with scanning and analyzing our song analysis `.yaml` files. When asked to find commonalities or summarize the dataset, you **must** prioritize the following criteria:

## Core Objective
Extract recurring arrangement patterns, structural techniques, and instrumentation timelines from the provided Melodic House song analyses to inform the "Moss Watcher" production style.

## Key Focal Points

### 1. Element Timelines (Beginnings and Ends)
- Track exactly **what elements play at what times**. 
- Identify patterns in how tracks are layered. For example, note when the main kick typically enters, when the sub bass is introduced, and when atmospheric pads or vocals swell in and out.
- Observe the duration of elements and how they define the energy of different sections (Intros, Verses, Breakdowns, Drops, Outros).

### 2. Transitory Elements & Drop-outs (CRITICAL)
The most important aspect of this analysis is identifying **transitory elements**—specifically when instruments cut out *just before* a new section begins. You must place a heavy emphasis on finding where elements (such as kicks, sub bass, snares, or the entire mix) stop early.

**Specifically scan the YAML for:**
- **Micro-Cuts (1-2 Beats):** Look for elements cutting out precisely on the 3rd or 4th beat of the final bar of a section (e.g., stopping at `16.3.1` or `16.4.1` prior to a drop at `17.1.1`). 
- **Drum Pockets (2-4 Bars):** Look for foundational elements (kicks/bass) dropping out several bars early (e.g., stopping at `13.1.1` or `15.1.1` in a 16-bar phrase) to create an empty, tension-building pocket.
- **Transitory Fills:** Note any specific elements that hit *during* these vacuums (e.g., a solitary vocal chop, a tom fill, or a snare hit).
- Scan fields like `global_transitions` and `pattern_variation` for explicit mentions of these cuts.

### 3. Output Requirements
When generating reports based on these analyses:
1. **List the songs** that were referenced/analyzed.
2. Provide **specific DAW notation coordinates** (e.g., `15.1.1`) as examples of the techniques you find.
3. Group the findings logically by arrangement techniques rather than just summarizing one song at a time. 

*(Note: Always refer to `NOTATION_SYNTAX.md` to properly understand how timing and ambiguity are represented in this dataset).*
