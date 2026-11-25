# v42 display recovery — 2026-11-09

Status: unresolved. Do not treat the candidate as a committed or verified CAD build.

## Follow-up — 2026-11-10

The CAD capability query responded immediately and advertised supported writes. No missing-runtime or disconnected-runtime diagnostic was returned. Opening the existing design again stayed on panel (done 2/29). A source query and a whole-part rewrite using the saved 2D-union candidate were submitted; neither returned a completed result before the waiting orchestration was stopped. The original managed panel source remained unchanged at the final Git check. A pipeline report was requested but likewise did not return promptly. No new build or handoff has been verified. This does not establish that reinstalling the runtime would help.

Further diagnosis needs application diagnostics showing request queuing, build cancellation/timeout handling and the edit recovery path. In the app, Settings → Advanced → Diagnostics → Export logs provides those diagnostics. Do not repeat unchanged rebuilds as a recovery strategy.

The original 23 MB STEP remains on disk. The existing panel source uses overlapping translated copies of entire 32-feature scale and number profiles (9 copies), 26 retention profiles (25 copies), and 19 letter profiles (9 copies). On this machine, repeated rebuild progress stays on panel, done 2 of 29 parts, without returning a usable CAD response after restart.

The adjacent candidate preserves all parameter names, defaults, original translation samples, feature coordinates and extrusion depths. It unions translated faces per feature in 2D before extruding, then cuts the panel with those tools, rather than subtracting overlapping multi-solid 3D cutters. The candidate has not been validated or committed to managed CAD source.

The CAD open request returned a confirmed 600-second timeout during cell execution of panel. Source inspection returned the original panel source and parameters at revision d8735744031ab13899df4952f81c33fe33167766bf2919ebdc7ec3e0a5058865. The optimization edit request did not return a completed result before its orchestration was stopped. No successful build or export has been observed. Do not hand-edit managed source or cache files to install the candidate. Resume through the CAD editor once the CAD service responds, inspect the resulting preview and slot/inlay fit, then publish a matching handoff STEP. Existing unrelated staged reference deletions and application migration changes have been left intact.
