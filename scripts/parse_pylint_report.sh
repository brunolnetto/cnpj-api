#!/bin/bash

# Define the paths for the pylint report and the processed output
PYLINT_REPORT_FILE="pylint_report.txt"
PROCESSED_REPORT_FILE="processed_pylint_report.txt"

# Define the directories to lint (change this to your actual directories)
DIRECTORIES_TO_LINT="backend/app"

# Run pylint and save the report
echo "Generating pylint report..."
pylint $DIRECTORIES_TO_LINT > "$PYLINT_REPORT_FILE"

# Check if the report file was created
if [[ ! -f "$PYLINT_REPORT_FILE" ]]; then
    echo "Failed to generate pylint report!"
    exit 1
fi

# Extract the pylint evaluation grade from the last line of the report
grade=$(grep -oP "rated at \d+\.\d+/10" "$PYLINT_REPORT_FILE" | head -n 1 | grep -oP "\d+\.\d+/10")

# Check if the grade was extracted successfully
if [[ -z "$grade" ]]; then
    echo "Failed to extract pylint grade!"
    exit 1
fi

# Write the evaluation grade at the top of the processed report file
echo "Pylint evaluation grade: $grade" > "$PROCESSED_REPORT_FILE"

# Use awk to parse and format the report, and save to processed report file
echo "Processing pylint report..."
awk -v processed_report="$PROCESSED_REPORT_FILE" '
BEGIN {
    # Initialize counters
    total_errors = 0;
    print "Parsing pylint report...";
}
# Skip lines with "Module" headers
/^************* Module/ {
    next;
}
{
    # Split the line based on the colon to get the parts
    split($0, fields, ":");
    
    # Ensure the line has at least 5 parts
    if (length(fields) >= 5) {
        # Extract file, line, column, type, and message
        file = fields[1];
        line = fields[2];
        col = fields[3];
        type = fields[4];
        
        # Reassemble the message which can span multiple fields
        message = fields[5];
        for (i = 6; i <= length(fields); i++) {
            message = message ":" fields[i];
        }
        
        # Trim leading and trailing spaces from file, line, col, type, and message
        gsub(/^[ \t]+|[ \t]+$/, "", type);
        gsub(/^[ \t]+|[ \t]+$/, "", file);
        gsub(/^[ \t]+|[ \t]+$/, "", line);
        gsub(/^[ \t]+|[ \t]+$/, "", col);
        gsub(/^[ \t]+|[ \t]+$/, "", message);

        # Extract the complete content inside parentheses (at the end of the message)
        if (match(message, /\(([^)]+)\)$/, arr)) {
            description = arr[1];  # Extracts text inside the last parentheses
            # Remove the parentheses and content inside them from the message
            sub(/\s*\([^)]+\)$/, "", message);
        } else {
            description = "";
        }
        
        # Format the message to be in the required style
        formatted_message = file ":" line ":" col ": " message;
        
        # Format the header with error code and description
        header = "Error type: (" type ": " description ") occurrences: " error_count[type];
        
        # Count the total number of errors
        total_errors++;

        # Accumulate errors by type
        if (type in error_types) {
            error_types[type] = error_types[type] "\n" formatted_message;
        } else {
            error_types[type] = formatted_message;
        }
        
        # Save the description for the error type if it exists
        if (description != "") {
            error_description[type] = description;
        }
        
        # Count errors per type
        error_count[type]++;
    }
}
END {
    # Print total errors
    print "Total lint errors: " total_errors >> processed_report;
    print "" >> processed_report;

    # Print errors grouped by type
    for (type in error_types) {
        # Format the header with code and description
        header = "Error type: (" type ": " error_description[type] ") occurrences: " error_count[type];
        print header >> processed_report;
        print error_types[type] >> processed_report;
        print "" >> processed_report;
    }
}
' "$PYLINT_REPORT_FILE"

# Check if the processed report was created
if [[ ! -f "$PROCESSED_REPORT_FILE" ]]; then
    echo "Failed to process pylint report!"
    exit 1
fi

# Delete the original pylint report
echo "Cleaning up..."
rm "$PYLINT_REPORT_FILE"

echo "Processing complete. Results saved to $PROCESSED_REPORT_FILE."
