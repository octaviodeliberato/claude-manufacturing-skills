# A fixed-shaft cone crusher's setting is a batch sequence, not a continuous loop

`mineral-processing-pfd` first drew every cone crusher's closed-side setting (CSS) the hydraulic-setting way: a `ZIC` in setting or load mode, a power/pressure override that opens the CSS, and continuous wear compensation (`references/control-strategies.md`, Circuit 1, sourced from Hulthén 2010 and Metso's crushing handbook). That only holds for cones whose setting moves hydraulically under load. The first real use, on a plant running Metso HP500s, showed the gap. Fixed-shaft cones (Symons family, Metso HP) set the CSS by turning the bowl on its thread through a hydraulically driven ring gear, and only with the chamber empty and the clamping pressure released. The plant supplied this information; the research file does not cover it.

**Decision:** the skill resolves each cone crusher's **adjustment family** (see `CONTEXT.md`) before drawing its setting. A fixed-shaft cone gets a batch chain:

- `ZT` counts pulses from the ring gear;
- `ZY` computes the CSS from a calibrated zero;
- `ZC` runs the adjustment sequence and drives the adjustment-ring `motor()`.

The power and tramp-release pressure limits act on the crusher's feed (or are an alarm-only `PI` when the crusher has no feeder of its own), never on the CSS. The advanced block writes the CSS target for the next adjustment window into the `ZC`. A new final-element class, **CRUSHER SETTING (BATCH)**, names this.

**Rejected:** drawing a `ZIC` on a fixed-shaft cone with a note saying it is adjusted only when empty. The drawing would claim a continuous loop and an override that cannot exist, and the narrative would contradict the symbols.

**Consequences:** the hydraulic-setting rows stay as they were. The fixed-shaft rows replace only the CSS rows of each tier. The calibration factor (mm per pulse) and the zero procedure are vendor data, so the skill lists them as pending items rather than quoting numbers. Hulthén's +3.5 % RTO yield gain was measured with the CSS moved under load, so it is not quoted for fixed-shaft cones.

## Status

Accepted.
