# `screen(wet=True)` changes the label, not the geometry — the composing script draws the wash-water pipe

The original spec for `mineral-processing-pfd` (issue #1) described the parametric screen primitive's `wet` flag as adding "a wash-water spray inlet line" itself. The shipped `screen()` in `scripts/pid_lib.py` doesn't do that — `wet=True` only appends `(wet)`/`(dry)` to the label; drawing the actual wash-water pipe is left to the composing script, same as every other equipment primitive in this library.

**Why the deviation:** every primitive here — `vessel()` first, in the `pfd-generator` fork point, and every mineral-processing primitive after it — follows one rule without exception: a primitive draws its own body and internals, never its own inlet/outlet pipe stubs (see the module docstring in `scripts/pid_lib.py`). The reason is layout control: the composing script is the only place that knows where a nozzle can land without colliding with a neighboring line, so nozzle routing always happens there, in `pipe()` calls, never inside a primitive. Giving `screen()` a one-off exception — drawing its own wash-water line internally — would silently break that invariant for one primitive out of twenty-seven, which is a worse inconsistency than diverging from the spec's exact wording.

**Decision:** `wet`/`dry` stays a label-only flag on `screen()`. Any drawing that needs a wet screen draws the wash-water pipe itself, in `BLUE`, into the screen's top span — documented in the primitive's own docstring and in `references/mineral-processing-symbols.md`.

## Status

Accepted.
