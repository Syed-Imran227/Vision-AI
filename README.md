# Vision AI - Advanced Voice Assistant

Vision AI is an advanced, modular, AI-powered voice assistant tailored to provide comprehensive screen reading, web navigation, system control, and conversational capabilities using Google's Generative AI. 

## ✨ Features

- **Conversational Intelligence**: Powered by `google-genai` for natural language processing and dynamic task processing.
- **Vision & Screen OCR**: Capable of reading text from the screen and analyzing visual information using OpenCV and Tesseract (`pytesseract`).
- **Smart Web Automation**: Seamlessly navigates the web, reads web pages, and controls the browser autonomously via Selenium.
- **Voice Capabilities**: Real-time voice interaction using `SpeechRecognition` and local TTS (Text-to-Speech) engines.
- **System Control**: Execute local system commands, file management, and system utilities directly via voice instructions.
- **Intuitive UI**: A sleek, user-friendly graphical interface visualizing the current state, processing status, and conversational history of Vision AI.

## 📁 Architecture

The project is structured into modular domain-specific components to ensure a clean, maintainable architecture:

```text
voice_assistant/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── config.json          # Application configuration
├── audio/               # Speech synthesis (TTS), recognition, and sound effects
├── core/                # Brain of the AI: LLM client and command dispatcher
├── vision/              # Screen reading, OCR, and smart PDF/image parsing
├── web/                 # Browser automation and smart web reading agents
├── system/              # System utilities and local system control handlers
├── ui/                  # Dashboard and interface components
├── scripts/             # Useful development and setup scripts
└── tests/               # Unit and integration tests
```

## 🛠️ Prerequisites

- **Python 3.8+**
- **Tesseract OCR**: Needs to be installed on your system and added to your system `PATH`.
- **Google Chrome**: Required for the Selenium web automation module (`chromedriver` is managed locally).
- **Microphone**: A working microphone setup for voice commands.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vision-ai.git
   cd vision-ai
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Ensure you have a `.env` file or export the required API keys to use the Generative AI features:
   ```env
   GEMINI_API_KEY=your_google_genai_key_here
   ```

## 🎯 Usage

Start the Vision AI voice assistant by running the main entry point:

```bash
python main.py
```

The application will launch the UI dashboard and automatically begin listening for your commands. Say `"Hello"` to initialize the sequence!

## 📝 License

This project is built for educational and personal productivity purposes. Please ensure you comply with the terms of service of the third-party APIs used.
