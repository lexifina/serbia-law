cd "$(dirname "$0")"
export LE_WORKERS=6 LE_GREP_THREADS=6 PYTHONIOENCODING=utf-8
P="python -X utf8"
$P detectors/trailer_only.py run; $P detectors/rank.py run
$P ingest/refscan.py --fileact serbia-law; $P detectors/ref_detectors.py run
$P release/build_release.py out
echo DONE
