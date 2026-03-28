#!/bin/bash

# macOS Agentic AI - One-Click Installer
echo "🚀 Starting macOS Agentic AI Setup..."

# 1. Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is already installed."
fi

# 2. Install System Dependencies
echo "🛠️ Installing system dependencies (PortAudio)..."
brew install portaudio

# 3. Check for Ollama
if ! command -v ollama &> /dev/null; then
    echo "🧠 Ollama not found. Please download it from https://ollama.com and install it manually."
    echo "After installing Ollama, run: ollama pull gemma3:1b"
else
    echo "✅ Ollama found. Ensuring gemma3:1b is available..."
    ollama pull gemma3:1b
    ollama pull nomic-embed-text
fi

# 4. Setup Python Environment
echo "🐍 Setting up Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Setup Background Daemon
echo "⚙️ Setting up macOS Background Daemon..."
PLIST_PATH="$HOME/Library/LaunchAgents/com.agentic.ai.plist"
WORKING_DIR=$(pwd)

cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.agentic.ai</string>
    <key>ProgramArguments</key>
    <array>
        <string>$WORKING_DIR/venv/bin/python3</string>
        <string>$WORKING_DIR/main.py</string>
        <string>--daemon</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$WORKING_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/agentic_ai.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/agentic_ai.stderr.log</string>
</dict>
</plist>
EOF

# Load the daemon
launchctl load "$PLIST_PATH"

echo "✅ Setup Complete!"
echo "------------------------------------------------"
echo "To start the chat interface, run:"
echo "source venv/bin/activate && python3 main.py"
echo ""
echo "Or talk to the background agent via voice if enabled!"
echo "------------------------------------------------"
