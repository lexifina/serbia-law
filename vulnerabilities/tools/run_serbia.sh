#!/usr/bin/env bash
# Serbia-only run of global-law's vulnerability detectors (no sync: pins.json is written by hand for serbia-law).
cd "$(dirname "$0")"
export LE_WORKERS=6 LE_GREP_THREADS=6 PYTHONIOENCODING=utf-8
P="python -X utf8"
set -x
$P ingest/extract.py && $P ingest/trailers.py
$P ingest/textscan.py && $P ingest/refscan.py
$P ingest/headings.py
$P detectors/trailer_only.py run; $P detectors/rank.py run; $P detectors/text_detectors.py run
$P detectors/ref_detectors.py run; $P detectors/placeholder_ref.py run; $P detectors/late_extension.py run
$P detectors/dead_fine.py run; $P detectors/notes_scan.py run
$P detectors/currency_scan.py run; $P detectors/dup_labels.py run
$P release/build_release.py out
echo DONE
