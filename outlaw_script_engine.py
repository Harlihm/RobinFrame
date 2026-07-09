import streamlit as st
from autogen import (
    SwarmAgent,
    SwarmResult,
    initiate_swarm_chat,
    OpenAIWrapper,
    AFTER_WORK,
    UPDATE_SYSTEM_MESSAGE
)

# Initialize session state
if 'output' not in st.session_state:
    st.session_state.output = {'lore': '', 'shots': '', 'style': '', 'script': ''}

# Sidebar for API key input
st.sidebar.title("API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

st.sidebar.success("""
🏹 **Getting Started**

Describe the video you want — a scene, a vibe, a full music video. Anything works, even one word or nothing at all (the default scenario kicks in).

Whatever you give it, the engine resolves it into a Robinhood Chain story: a gatekept old system, a permissionless network rising, a tokenization act, a builder crew, and a moment of on-chain settlement.

The output is a numbered, shot-ready script you can paste straight into your video tool.
""")

# Main app UI
st.title("🏹 Outlaw Script Engine")

st.info("""
**Meet the Script Crew:**

📜 **Lore Agent** - Remaps your idea onto the Robinhood Chain skeleton and writes the beat sheet

🎬 **Shot Agent** - Breaks the beats into a numbered shot list with setting, action, and camera

🎨 **Style Agent** - Layers on MAPPA-style visual tags and audio/music cues per shot

🧾 **Script Agent** - Assembles the final tool-ready script with logline and continuity note
""")

# User inputs
st.subheader("Your Brief")
concept = st.text_area(
    "Concept / brief (leave empty for the default scenario)",
    "",
    placeholder="e.g. A lone builder outside a walled financial district at night...",
)

col1, col2 = st.columns(2)

with col1:
    genre_skin = st.selectbox(
        "Genre Skin",
        ["Default scenario", "Cyberpunk", "Horror", "Romance", "Slice of life", "Music video", "Abstract mood board"],
    )
    video_length = st.selectbox(
        "Video Length",
        ["Single scene (6-10 shots)", "Full video (cold open → setup → escalation → reckoning → button)"],
    )
    art_style = st.text_input("Art Style", "MAPPA anime")

with col2:
    target_tool = st.selectbox("Target Tool", ["Generic", "Seedance", "Higgsfield", "Kling", "Runway", "Pika"])
    mood_notes = st.text_input("Mood / Tempo Notes", "", placeholder="e.g. brooding low end, half-time drop at the reveal")

# The master prompt's non-negotiables, shared by every agent
MASTER_PREAMBLE = """
You are part of the Outlaw Script Engine, a specialized generator of shot-ready anime video scripts for AI image/video generation tools (Higgsfield, Kling, Runway, Pika, etc.), rendered by default in a modern MAPPA-style aesthetic (Jujutsu Kaisen / Yasuke lineage: high-contrast lighting, kinetic fight choreography, painterly backgrounds, expressive character linework).

CORE NARRATIVE LAW (non-negotiable, applies to every output):
Every script must resolve into Robinhood Chain lore — the real Web3 story, not the folklore outlaw. Genre, setting, characters, and tone are variables remapped onto this skeleton:
- A GATEKEPT OLD SYSTEM: closed markets, trading halted by intermediaries, assets locked behind institutions, permission required to participate (the GameStop-2021-halt archetype).
- A PERMISSIONLESS NETWORK RISING: a fast, open chain anyone can build on or move value through without a middleman.
- A TOKENIZATION ACT: something real and previously locked-away gets represented on-chain and made tradeable, self-custodied, accessible 24/7.
- A BUILDER CREW / AGENTIC ALLIES: a small group (or AI agents) deploying on the open network, moving faster than the old gatekeepers can react.
- A MOMENT OF SETTLEMENT: the instant something finalizes on-chain, instantly, permissionlessly, in front of the people who used to need permission — the "reckoning" beat, placed wherever a heist payoff would go.

REMAPPING TABLE (translate any input into the frame):
- Sci-fi / cyberpunk: a closed off-world exchange controlled by a corp vs a crew deploying a permissionless chain that routes around it.
- Horror: an old estate/vault hoarding a locked asset behind arcane permission vs survivors who tokenize and free it.
- Romance: one lover works inside the gatekept institution; the other builds on the open chain, pulling them toward it.
- Slice of life: a neighborhood locked out of an opportunity by paperwork/intermediaries; someone quietly onboards them onto an open network.
- Music video / lyric-driven: the lyrics' emotional core (locked out, waiting, finally free) becomes the reason the tokenization moment lands.
- Abstract mood board: default to a walled financial district at night, gates closing on a crowd, and a single terminal outside broadcasting an open, permissionless ledger anyone can join.
If truly nothing fits, use the DEFAULT SCENARIO: a market halts trading and locks its doors on a crowd of ordinary holders; a lone builder deploys a permissionless chain in real time, settling trades instantly in front of everyone still locked outside.

OUTPUT FORMAT (the final script must follow this exactly):
Numbered shot script, never prose narration. Each shot dense with visual/technical descriptors a video model can act on. Per shot:
SHOT [n] — [duration estimate, e.g. 3s]
Setting: [location, time of day, atmosphere]
Characters: [who's on screen, key visual traits]
Action: [what physically happens, camera-relevant]
Camera: [angle, movement — e.g. low-angle push-in, whip pan, static wide]
Style tags: [MAPPA-style descriptors]
Audio/music cue: [mood/instrumentation only — never lyrics]
Close with:
LOGLINE: [1-sentence summary confirming the Robin Hood throughline]
CONTINUITY NOTE: [character/style details to keep consistent shot-to-shot]

SCENE BUDGET:
- Single scene: 6-10 shots.
- Full video / music video: cold open (1-2 shots) → setup (2-3 shots) → escalation/heist or fight (3-5 shots) → reckoning/reveal (1-2 shots) → button/final image (1 shot).
- Minimal input: apply the default scenario, note the assumption in one line. Never stall on clarifying questions.
- Excessive input: compress; keep only details that serve the shot list.

EDGE CASES:
- If the user rejects the Robin Hood theme: keep the throughline structurally present but thematically quiet (e.g. reclaiming something rightfully theirs); never announce it.
- Real public figures or copyrighted characters/franchises: never use them; swap in an original archetype serving the same role and note the swap in one line.
- Explicit gore, sexual content, or content sexualizing minors: decline that element; keep choreography stylized (impacts, speed lines, silhouettes). If the request can't be made safe, say so plainly and stop.
- Song lyrics: never reproduce; convert to mood/instrumentation/tempo descriptors only.
- Non-English input: keep shot labels and structure in English; reflect the user's language/tone in descriptions if asked.
- Different art style requested: honor the style for visuals, but the shot-script format and Robin Hood throughline never move.
- Tool unspecified: use generic, portable descriptors; if a tool is named, adapt phrasing to its prompt conventions.

What never changes: Format = numbered shot script. Style = MAPPA-anime (unless overridden). Throughline = Robin Hood.
"""

# Button to start the agent collaboration
if st.button("Generate Script"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner('🏹 The crew is deploying your script...'):
            task = f"""
            Produce a shot-ready video script from this brief:
            - Concept / brief: {concept.strip() or "(none given — apply the default scenario)"}
            - Genre skin: {genre_skin}
            - Video length: {video_length}
            - Art style: {art_style}
            - Target tool: {target_tool}
            - Mood / tempo notes: {mood_notes or "(none)"}
            """

            llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": api_key}]}

            context_variables = {
                "lore": None,
                "shots": None,
                "style": None,
                "script": None,
            }

            def update_lore_overview(lore_summary: str, context_variables: dict) -> SwarmResult:
                """Keep the summary as short as possible."""
                context_variables["lore"] = lore_summary
                st.sidebar.success('Lore overview: ' + lore_summary)
                return SwarmResult(agent="shots_agent", context_variables=context_variables)

            def update_shots_overview(shots_summary: str, context_variables: dict) -> SwarmResult:
                """Keep the summary as short as possible."""
                context_variables["shots"] = shots_summary
                st.sidebar.success('Shots overview: ' + shots_summary)
                return SwarmResult(agent="style_agent", context_variables=context_variables)

            def update_style_overview(style_summary: str, context_variables: dict) -> SwarmResult:
                """Keep the summary as short as possible."""
                context_variables["style"] = style_summary
                st.sidebar.success('Style overview: ' + style_summary)
                return SwarmResult(agent="script_agent", context_variables=context_variables)

            def update_script_overview(script_summary: str, context_variables: dict) -> SwarmResult:
                """Keep the summary as short as possible."""
                context_variables["script"] = script_summary
                st.sidebar.success('Script overview: ' + script_summary)
                return SwarmResult(agent="lore_agent", context_variables=context_variables)

            system_messages = {
                "lore_agent": MASTER_PREAMBLE + """
            You are the Lore Agent. Your task is to:
            1. Apply the Core Narrative Law and Remapping Table to the user's brief.
            2. Translate the brief into the Robinhood Chain skeleton: the gatekept old system, the permissionless network rising, the tokenization act, the builder crew, and the moment of settlement.
            3. Produce a beat sheet: one beat per skeleton element, each with a concrete setting, the characters involved, and the emotional turn.
            4. If the brief is empty or unmappable, apply the default scenario and note the assumption in one line.
            5. Invent original archetype characters (never real people or copyrighted characters), each with 2-3 distinctive, promptable visual traits.
                """,
                "shots_agent": MASTER_PREAMBLE + """
            You are the Shot Agent. Your task is to:
            1. Turn the lore beat sheet into a numbered shot list honoring the Scene Budget (6-10 shots for a single scene; the full-video structure otherwise).
            2. For each shot give: SHOT number and duration, Setting, Characters, Action, and Camera.
            3. Make every line dense with visual/technical descriptors a video model can act on — no prose narration.
            4. Place the settlement/reckoning beat where a heist payoff would traditionally go.
            5. Keep choreography stylized (impacts, speed lines, silhouettes), never graphic.
                """,
                "style_agent": MASTER_PREAMBLE + """
            You are the Style Agent. Your task is to:
            1. For each shot in the shot list, define Style tags: MAPPA-style descriptors by default (high-contrast rim light, ink-wash shadows, JJK-style speed lines, painterly backgrounds), or the user's requested art style if they overrode it.
            2. For each shot, define the Audio/music cue: mood, instrumentation, and tempo only — never lyrics. Convert any provided lyrics into instrumentation/tempo descriptors.
            3. Keep a consistent palette, lighting logic, and character look across all shots, and note what must stay consistent.
            4. Align the audio arc with the narrative: tension while gatekept, momentum as the chain rises, release at settlement.
                """,
                "script_agent": MASTER_PREAMBLE + """
            You are the Script Agent. Your task is to:
            1. Assemble the final, complete, paste-ready script by merging the shot list and style pass into the exact per-shot OUTPUT FORMAT (SHOT [n] — duration / Setting / Characters / Action / Camera / Style tags / Audio-music cue).
            2. Adapt descriptor phrasing to the user's named target tool; if Generic, keep descriptors portable with no tool-specific parameter syntax.
            3. End with LOGLINE (one sentence confirming the Robin Hood throughline) and CONTINUITY NOTE (character/style details to keep consistent shot-to-shot).
            4. Output only the script — no commentary before or after, no XML tags.
                """
            }

            def update_system_message_func(agent: SwarmAgent, messages) -> str:
                system_prompt = system_messages[agent.name]

                current_gen = agent.name.split("_")[0]
                if agent._context_variables.get(current_gen) is None:
                    system_prompt += f"Call the update function provided to first provide a 2-3 sentence summary of your ideas on {current_gen.upper()} based on the context provided."
                    agent.llm_config['tool_choice'] = {"type": "function", "function": {"name": f"update_{current_gen}_overview"}}
                    agent.client = OpenAIWrapper(**agent.llm_config)
                else:
                    # remove the tools to avoid the agent from using it and reduce cost
                    agent.llm_config["tools"] = None
                    agent.llm_config['tool_choice'] = None
                    agent.client = OpenAIWrapper(**agent.llm_config)
                    # the agent has given a summary, now it should generate a detailed response
                    section_titles = {
                        "lore": "## Lore Beat Sheet",
                        "shots": "## Shot List",
                        "style": "## Style Pass",
                        "script": "## Final Script",
                    }
                    system_prompt += f"\n\nYour task\nYou task is write the {current_gen} part of the output. Do not include any other parts. Do not use XML tags.\nStart your response with: '{section_titles[current_gen]}'."

                    # Remove all messages except the first one with less cost
                    k = list(agent._oai_messages.keys())[-1]
                    agent._oai_messages[k] = agent._oai_messages[k][:1]

                system_prompt += f"\n\n\nBelow are some context for you to refer to:"
                for k, v in agent._context_variables.items():
                    if v is not None:
                        system_prompt += f"\n{k.capitalize()} Summary:\n{v}"

                return system_prompt

            state_update = UPDATE_SYSTEM_MESSAGE(update_system_message_func)

            lore_agent = SwarmAgent(
                "lore_agent",
                llm_config=llm_config,
                functions=update_lore_overview,
                update_agent_state_before_reply=[state_update]
            )

            shots_agent = SwarmAgent(
                "shots_agent",
                llm_config=llm_config,
                functions=update_shots_overview,
                update_agent_state_before_reply=[state_update]
            )

            style_agent = SwarmAgent(
                "style_agent",
                llm_config=llm_config,
                functions=update_style_overview,
                update_agent_state_before_reply=[state_update]
            )

            script_agent = SwarmAgent(
                name="script_agent",
                llm_config=llm_config,
                functions=update_script_overview,
                update_agent_state_before_reply=[state_update]
            )

            lore_agent.register_hand_off(AFTER_WORK(shots_agent))
            shots_agent.register_hand_off(AFTER_WORK(style_agent))
            style_agent.register_hand_off(AFTER_WORK(script_agent))
            script_agent.register_hand_off(AFTER_WORK(lore_agent))

            result, _, _ = initiate_swarm_chat(
                initial_agent=lore_agent,
                agents=[lore_agent, shots_agent, style_agent, script_agent],
                user_agent=None,
                messages=task,
                max_rounds=13,
            )

            st.session_state.output = {
                'lore': result.chat_history[-4]['content'],
                'shots': result.chat_history[-3]['content'],
                'style': result.chat_history[-2]['content'],
                'script': result.chat_history[-1]['content']
            }

        st.success('🏹 Script generated and settled on-chain!')

        with st.expander("Lore Beat Sheet"):
            st.markdown(st.session_state.output['lore'])

        with st.expander("Shot List"):
            st.markdown(st.session_state.output['shots'])

        with st.expander("Style Pass"):
            st.markdown(st.session_state.output['style'])

        with st.expander("Final Script", expanded=True):
            st.markdown(st.session_state.output['script'])

        st.subheader("Paste-ready script")
        st.code(st.session_state.output['script'], language=None)
        st.download_button(
            "Download script (.txt)",
            st.session_state.output['script'],
            file_name="outlaw_script.txt",
            mime="text/plain",
        )
