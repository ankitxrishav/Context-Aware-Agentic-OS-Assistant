# Agentic AI Windows Setup Script
Write-Host "🧭 Starting Windows Setup for Agentic AI..." -ForegroundColor Cyan

# 1. Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install it from python.org" -ForegroundColor Red
    exit
}

# 2. Check for Ollama
if (!(Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️ Ollama not found. Ensure it is installed and running." -ForegroundColor Yellow
} else {
    Write-Host "📥 Pulling Gemma3:1B model..."
    ollama pull gemma3:1b
}

# 3. Virtual Environment
Write-Host "🐍 Creating Virtual Environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

# 4. Install Dependencies
Write-Host "📦 Installing Dependencies..."
pip install -r requirements.txt
# Windows specific dependency for voice if needed
# pip install pipwin
# pipwin install pyaudio

Write-Host "✅ Setup Complete! To start the agent, run:" -ForegroundColor Green
Write-Host ".\venv\Scripts\activate"
Write-Host "python main.py"
