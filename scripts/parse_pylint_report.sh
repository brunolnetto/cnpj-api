#!/bin/bash

# Paths
PYLINT_REPORT_FILE="pylint_report.txt"
PROCESSED_REPORT_FILE="processed_pylint_report.txt"
DIRECTORIES_TO_LINT="backend/app"

# Generate pylint report
echo "Generating pylint report..."
pylint "$DIRECTORIES_TO_LINT" > "$PYLINT_REPORT_FILE" || {
  echo "Failed to generate pylint report!"
  exit 1
}

# Extract grade
if ! grade=$(grep -oP "rated at \d+\.\d+/10" "$PYLINT_REPORT_FILE" | grep -oP "\d+\.\d+/10" | head -n 1); then
  echo "Failed to extract pylint grade!"
  exit 1
fi

echo "Pylint evaluation grade: $grade" > "$PROCESSED_REPORT_FILE"
echo "Processing pylint report..."

awk -v output="$PROCESSED_REPORT_FILE" '
BEGIN {
  total = 0
  print "Parsing pylint report..."
}
/^\*{10} Module/ { next }
{
  split($0, f, ":");
  if (length(f) < 5) next

  file=f[1]; line=f[2]; col=f[3]; type=f[4]
  msg=f[5]; for (i=6; i<=length(f); i++) msg=msg ":" f[i]

  gsub(/^ +| +$/, "", file)
  gsub(/^ +| +$/, "", line)
  gsub(/^ +| +$/, "", col)
  gsub(/^ +| +$/, "", type)
  gsub(/^ +| +$/, "", msg)

  desc=""
  if (match(msg, /\(([^)]+)\)$/, arr)) {
    desc=arr[1]
    sub(/\s*\([^)]+\)$/, "", msg)
  }

  fmt=file":"line":"col": " msg
  err[type]=(type in err) ? err[type] "\n" fmt : fmt
  count[type]++
  if (!(type in descr) && desc != "") descr[type]=desc
  total++
}
END {
  print "Total lint errors: " total >> output
  print "" >> output
  for (t in err) {
    hdr = "Error type: (" t ": " descr[t] ") occurrences: " count[t]
    print hdr >> output
    print err[t] >> output
    print "" >> output
  }
}' "$PYLINT_REPORT_FILE"

[[ -f "$PROCESSED_REPORT_FILE" ]] || {
  echo "Failed to process pylint report!"
  exit 1
}

rm "$PYLINT_REPORT_FILE"
echo "Processing complete. Results saved to $PROCESSED_REPORT_FILE."
