# Outlaw Script Engine 🏹

The Outlaw Script Engine is a shot-ready anime script generator powered by [AG2](https://github.com/ag2ai/ag2)(formerly AutoGen)'s swarm agent framework. Give it any brief — a scene, a mood, a full music video idea, or nothing at all — and a crew of specialized AI agents turns it into a numbered, paste-ready shot script for AI image/video tools (Higgsfield, Kling, Runway, Pika), rendered in a modern MAPPA-style aesthetic.

Every script resolves into **Robinhood Chain lore**: a gatekept old system, a permissionless network rising, a tokenization act, a builder crew, and a moment of on-chain settlement. Genre, setting, characters, and tone are variables — the throughline never moves.

## Features

- **Specialized Script Crew**

  - 📜 **Lore Agent**: Remaps any brief onto the Robinhood Chain skeleton using the remapping table (cyberpunk, horror, romance, slice of life, music video, or the default locked-out-market scenario) and writes the beat sheet
  - 🎬 **Shots Agent**: Breaks the beats into a numbered shot list with setting, characters, action, and camera direction, honoring the scene budget
  - 🎨 **Style Agent**: Layers on MAPPA-style visual tags (high-contrast rim light, ink-wash shadows, speed lines) and audio/music cues per shot — never lyrics
  - 🧾 **Script Agent**: Assembles the final tool-ready script in the exact `SHOT [n]` format, closing with a logline and continuity note

- **Shot-Ready Output Format**:

  - Numbered shots with duration, setting, characters, action, camera, style tags, and audio cue
  - Logline confirming the Robin Hood throughline
  - Continuity note for consistent shot-to-shot prompting
  - Paste-ready code block plus one-click `.txt` download

- **Customizable Input Parameters**:

  - Free-text concept brief (empty input falls back to the default scenario)
  - Genre skin, video length (single scene or full structured video)
  - Art style override, target tool, mood/tempo notes

- **Built-in Guardrails**:
  - No real public figures or copyrighted characters (original archetypes swapped in)
  - No lyric reproduction — lyrics become instrumentation/tempo descriptors
  - Stylized, non-graphic choreography

## How to Run

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Harlihm/ai_game_design_agent_team.git
   cd ai_game_design_agent_team
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key**:

   - Obtain an OpenAI API key from [OpenAI's platform](https://platform.openai.com)
   - You'll input this key in the app's sidebar when running

4. **Run the Streamlit App**:

   ```bash
   streamlit run outlaw_script_engine.py
   ```

## Usage

1. Enter your OpenAI API key in the sidebar
2. Describe your video in the concept brief (or leave it empty for the default scenario)
3. Pick a genre skin, video length, art style, target tool, and mood notes
4. Click "Generate Script" and watch the crew's summaries land in the sidebar
5. Review the beat sheet, shot list, and style pass in the expandable sections, then copy or download the final script into your video tool
