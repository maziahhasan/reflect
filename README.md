# Reflect: Your Wellness Companion

Reflect is a serene, AI-powered wellness app built with Streamlit. It serves as a compassionate companion that remembers your conversations, tracks your moods, and provides tools for mental well-being. Designed for calm reflection, it offers features like chat with memory, journaling, mood logging, grounding exercises, and daily affirmations—all without judgment or rush.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web app framework for interactive UI.
- **Plotly**: Library for creating interactive mood tracking charts.
- **HTML/CSS**: Custom styling with Google Fonts (DM Serif Display and DM Sans) for a calm, serene interface.
- **Custom Modules**: agent.py for AI chat, memory management, and wellness functions.

## Features

- **💬 Chat with Memory**: Engage in conversations where Reflect remembers past interactions to provide personalized, context-aware responses.
- **📊 Mood Tracking**: Log your daily moods and visualize trends over time with interactive charts.
- **📓 Journaling**: Use guided prompts to write reflective entries, saved securely in the app's memory.
- **📝 Personal Notes**: Save notes on patterns, feelings, or insights for Reflect to reference.
- **🛠 Wellness Tools**: Access breathing exercises (e.g., Box Breathing, 5-4-3-2-1), daily affirmations, and crisis resources.
- **🌿 Calm Design**: Custom styling with a soothing color palette and fonts for a peaceful user experience.
- **Crisis Support**: Automatic detection and display of helplines when needed.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/memory-agent.git
   cd memory-agent
   ```

2. Install dependencies:
   ```
   pip install streamlit plotly
   ```
   (Note: Ensure you have Python 3.8+ installed.)

3. Run the app:
   ```
   streamlit run app.py
   ```

## Usage

- Open the app in your browser after running the command above.
- Start with a mood check-in to set the tone.
- Use the tabs to chat, journal, save notes, view mood analytics, or access tools.
- Reflect's memory persists during your session; data is stored in session state.

## Dependencies

- Streamlit
- Plotly (for mood charts)
- Custom module: agent.py (handles chat, memory, and wellness functions)

## Project Structure

- app.py: Main Streamlit application file.
- agent.py: Backend logic for AI chat, memory management, and wellness tools (not included in this repo; implement or mock as needed).

## Contributing

Feel free to fork and contribute improvements. Ensure changes align with the calm, supportive ethos of the app.

## License

This project is open-source. Use responsibly and prioritize user well-being.
