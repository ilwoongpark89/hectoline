#!/bin/sh
# grade.sh PREDICTIONS.jsonl RUN_ID GRADING_DIR [SWEBENCH_BIN]
# The official grader on the predictions of one arm, in batches of at most five instances. After each batch the
# evaluation containers of the run are removed with `swebench images clean`; with RM_IMAGES=1 the instance images
# of the batch go too, so only the log folders stay. Instances already graded under RUN_ID are skipped by the grader. Before each batch the free space of / is checked against the
# owner's floor of 150 GB by `diskutil info /`; the script stops when the floor would be crossed.
# Results: GRADING_DIR/logs/run_evaluation/RUN_ID/<arm>/<instance>/report.json per instance and the run report
# GRADING_DIR/<arm>.RUN_ID.json that the harness writes at the end of each batch.
set -eu
PRED=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
RUN_ID=$2
DIR=$3
SWEBENCH=${4:-swebench}
FLOOR_GB=150
mkdir -p "$DIR"
cd "$DIR"
ids=$(python3 -c "import json,sys; print(' '.join(json.loads(l)['instance_id'] for l in open(sys.argv[1]) if l.strip()))" "$PRED")
batch=""
n=0
run_batch() {
  free=$(diskutil info / | awk -F: '/Container Free Space/ {print $2}' | awk '{print $1}')
  echo "$(date '+%F %T') free ${free} GB, batch: $1"
  if [ "$(printf '%.0f' "$free")" -lt "$FLOOR_GB" ]; then
    echo "free space ${free} GB is under the floor of ${FLOOR_GB} GB, grading stops before this batch" >&2
    exit 3
  fi
  set -- $1
  args=""
  for i in "$@"; do args="$args -i $i"; done
  # shellcheck disable=SC2086
  "$SWEBENCH" eval verified -p "$PRED" --run-id "$RUN_ID" -j 2 -t 3600 $args || echo "grader exit $? on batch $*" >&2
  "$SWEBENCH" images clean --run-id "$RUN_ID" || true
  if [ "${RM_IMAGES:-0}" = 1 ]; then  # both arms share the instance images, so the caller removes them after the second arm
    for i in "$@"; do
      docker images --format '{{.Repository}}:{{.Tag}}' | grep -i "$(echo "$i" | sed 's/__/_1776_/')" | xargs docker rmi -f >/dev/null 2>&1 || true
    done
  fi
}
for id in $ids; do
  batch="$batch $id"
  n=$((n + 1))
  if [ $n -eq 5 ]; then
    run_batch "$batch"
    batch=""
    n=0
  fi
done
if [ -n "$batch" ]; then
  run_batch "$batch"
fi
echo "$(date '+%F %T') grading done for $RUN_ID"
