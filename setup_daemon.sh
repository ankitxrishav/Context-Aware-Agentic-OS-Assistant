#!/bin/bash

# Configuration
PLIST_NAME="com.agentic.ai.plist"
PLIST_SOURCE="/Users/ankitkumar/Desktop/agentic-ai/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "🧭 Agentic AI: Installing Background Daemon..."

# Check if source exists
if [ ! -f "$PLIST_SOURCE" ]; then
    echo "Error: $PLIST_NAME not found in current directory!"
    exit 1
fi

# Copy the plist to LaunchAgents
cp "$PLIST_SOURCE" "$PLIST_DEST"
echo "✅ Copied $PLIST_NAME to $PLIST_DEST"

# Unload previous version if exists
launchctl unload "$PLIST_DEST" 2>/dev/null
echo "✅ Unloaded previous daemon version (if any)"

# Load and start the LaunchAgent
launchctl load "$PLIST_DEST"
echo "✅ Registered and started the Agentic AI daemon!"

echo "---"
echo "Status: Running in background."
echo "Logs: /tmp/agentic_ai.stdout.log | /tmp/agentic_ai.stderr.log"
echo "Control: To stop, run 'launchctl unload $PLIST_DEST'"
