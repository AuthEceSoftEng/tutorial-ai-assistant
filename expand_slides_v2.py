"""
Slide Deck Expansion Script (Robust In-Place Overwrite)
--------------------------------------------------------
This script opens the user's original `finalpresentation.pptx` slide deck, 
clears and overwrites Slides 19-24 in-place with our restructured 5-Phase workshop content, 
and then appends new slides for the remaining phases and the final "Thank You" slide.

By avoiding deleting slide XML elements, it preserves all internal relationship IDs (rIds) 
perfectly, ensuring a highly stable and correct output presentation.

To run:
  python expand_slides_v2.py
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- DESIGN THEME CONFIGURATION ---
# Premium Slate Light Theme to blend seamlessly with the corporate ISSEL white template
COLOR_TEXT_PRIMARY = RGBColor(15, 23, 42)     # Deep Slate 900 (for titles / main text)
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)      # Slate 600 (for bullet point descriptions)
COLOR_ACCENT = RGBColor(0, 77, 124)           # Exact Brand Teal-Blue #004D7C (for category and headers)
COLOR_ACCENT_BG = RGBColor(241, 245, 249)     # Slate 100 (soft gray for container background)
COLOR_ACCENT_BORDER = RGBColor(226, 232, 240) # Slate 200 (subtle container border)
COLOR_GREEN = RGBColor(22, 163, 74)           # Success Green 600

FONT_TITLE = "Arial"
FONT_BODY = "Arial"

def set_slide_background(slide):
    """Protects template by keeping original white/graphic slide backgrounds."""
    pass

def clear_slide(slide):
    """Safely removes all shapes from a slide, leaving a blank canvas with the original background."""
    for shape in list(slide.shapes):
        el = shape.element
        el.getparent().remove(el)

def add_header(slide, title_text, category_text="HANDS-ON WORKSHOP"):
    """Adds a standardized, premium top header with category and title."""
    # Category Tracker
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_BODY
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_ACCENT
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_PRIMARY

def add_accent_bar(slide):
    """Protects the native ISSEL blue vertical border by avoiding duplicate drawing."""
    pass

def add_bullet_points(slide, points, left=0.8, top=1.8, width=6.0, height=5.0):
    """Draws rich bullet points in a textbox."""
    txt_box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txt_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    for i, (title, desc) in enumerate(points):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(14.5)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(14)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(3)

def add_code_box(slide, title, code_text, left=7.2, top=1.8, width=5.3, height=4.8):
    """Draws a premium light-theme code block with Slate 200 border styling."""
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.color.rgb = COLOR_ACCENT_BORDER
    code_bg.line.width = Pt(1)
    
    tf = code_bg.text_frame
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = f"💻 {title}"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p_code = tf.add_paragraph()
    p_code.text = code_text
    p_code.font.name = "Courier New"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = COLOR_TEXT_PRIMARY
    p_code.space_before = Pt(10)

def expand_presentation():
    original_path = "finalpresentation.pptx"
    expanded_path = "finalpresentation_expanded.pptx"
    
    print(f"🔄 Loading '{original_path}'...")
    prs = Presentation(original_path)
    
    # ----------------------------------------------------
    # OVERWRITE SLIDE 19: The 5-Phase Progression Map
    # ----------------------------------------------------
    print("✨ Overwriting Slide 19: The 5-Phase Progression Map...")
    slide19 = prs.slides[19]
    clear_slide(slide19)
    add_accent_bar(slide19)
    add_header(slide19, "The 5-Phase Progression Map")
    
    summary_box = slide19.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.5))
    p = summary_box.text_frame.paragraphs[0]
    p.text = "Our Journey Roadmap: Evolving from simple API connections to full autonomous agency."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    phases = [
        ("Phase 1", "Stateless Connection", "Problem: Stateless APIs\nSolution: Compiling local message history arrays"),
        ("Phase 2", "Instant Streaming", "Problem: High latency pauses\nSolution: Yielding token chunks for immediate feedback"),
        ("Phase 3", "Conversational Web UI", "Problem: Dark console text\nSolution: Transitioning to Chainlit async session bubbles"),
        ("Phase 4", "Local MCP Tools", "Problem: Static AI isolation\nSolution: Exposing coordinates, weather, and travel logs"),
        ("Phase 5", "Resilient Parallel Agent", "Problem: Slow & fragile loops\nSolution: Concurrent execution, self-correction, & collapsible runs")
    ]
    
    block_width = Inches(2.1)
    block_height = Inches(4.2)
    spacing = Inches(0.3)
    start_left = Inches(0.8)
    top_pos = Inches(2.3)
    
    for i, (ph, name, desc) in enumerate(phases):
        left_pos = start_left + i * (block_width + spacing)
        shape = slide19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, block_width, block_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_ACCENT_BG
        shape.line.color.rgb = COLOR_ACCENT if i == 4 else COLOR_ACCENT_BORDER
        shape.line.width = Pt(2.5 if i == 4 else 1)
        
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = ph.upper()
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        
        p2 = tf.add_paragraph()
        p2.text = name
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_PRIMARY
        p2.space_before = Pt(8)
        
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_before = Pt(16)

    # ----------------------------------------------------
    # OVERWRITE SLIDE 20: Phase 1: The CLI Chatbot
    # ----------------------------------------------------
    print("✨ Overwriting Slide 20: Phase 1: The CLI Chatbot...")
    slide20 = prs.slides[20]
    clear_slide(slide20)
    add_accent_bar(slide20)
    add_header(slide20, "Phase 1: The CLI Chatbot (main1.py)")
    
    bullets = [
        ("The Stateless Challenge", "LLM APIs are fundamentally stateless. They do not remember previous interactions. Every prompt is a brand-new, isolated request."),
        ("Architectural Solution", "We maintain conversation memory client-side using structured LangChain message arrays:\n• SystemMessage: Sets behavioral boundaries\n• HumanMessage: Represents the user input\n• AIMessage: Stores the model response"),
        ("Compiling History", "On every turn, we append user text to the list, invoke the model (`invoke()`), print the reply, and append it back to context.")
    ]
    add_bullet_points(slide20, bullets)
    
    code = (
        "messages = [SystemMessage(content=prompt)]\n\n"
        "while True:\n"
        "    user_input = input(\"\\nYou: \")\n"
        "    if user_input.lower() in [\"exit\"]: break\n\n"
        "    # Append new user interaction\n"
        "    messages.append(HumanMessage(content=user_input))\n\n"
        "    # Blocking invoke execution\n"
        "    response = aimodel.invoke(messages)\n"
        "    print(f\"\\nAI: {response.content}\")\n\n"
        "    # Save response in context memory\n"
        "    messages.append(response)"
    )
    add_code_box(slide20, "main1.py (Core Loop)", code)

    # ----------------------------------------------------
    # OVERWRITE SLIDE 21: Phase 2: CLI with Streaming
    # ----------------------------------------------------
    print("✨ Overwriting Slide 21: Phase 2: CLI with Streaming...")
    slide21 = prs.slides[21]
    clear_slide(slide21)
    add_accent_bar(slide21)
    add_header(slide21, "Phase 2: CLI with Streaming (main2.py)")
    
    bullets = [
        ("The Latency UX Bottleneck", "Waiting for a complete 200+ word model response creates a long, unnatural pause of 10+ seconds, causing high user drop-off."),
        ("Generator Paradigm Shift", "Instead of a single blocking API payload, the server starts yielding individual token chunks the moment they are generated."),
        ("Implementing stream()", "We swap `.invoke()` with `.stream()`, iterating over incoming chunks and flushing characters immediately to the console.")
    ]
    add_bullet_points(slide21, bullets)
    
    code = (
        "print(\"AI: \", end=\"\", flush=True)\n"
        "full_response = \"\"\n\n"
        "# Iterate token chunks dynamically\n"
        "for chunk in aimodel.stream(messages):\n"
        "    content = chunk.content\n"
        "    # Flush immediately to console\n"
        "    print(content, end=\"\", flush=True)\n"
        "    full_response += content\n"
        "print()\n\n"
        "# Save complete response\n"
        "messages.append(\n"
        "    AIMessage(content=full_response)\n"
        ")"
    )
    add_code_box(slide21, "main2.py (Streaming)", code)

    # ----------------------------------------------------
    # OVERWRITE SLIDE 22: Phase 3: Moving to a Web UI with Chainlit
    # ----------------------------------------------------
    print("✨ Overwriting Slide 22: Phase 3: Moving to a Web UI...")
    slide22 = prs.slides[22]
    clear_slide(slide22)
    add_accent_bar(slide22)
    add_header(slide22, "Phase 3: Moving to a Web UI (main3_chainlit.py)")
    
    bullets = [
        ("Moving to the Browser", "Transitioning from a text console to a beautiful browser-based UI is the key to creating production-ready consumer applications."),
        ("Conversational Framework", "We leverage Chainlit, an async web framework designed specifically for conversational UIs, avoiding generic page-reload overheads."),
        ("Async Lifecycle Hooks", "Uses event-driven callbacks for non-blocking UI updates:\n• `@cl.on_chat_start`: Configures session prompt state\n• `@cl.on_message`: Streams response bubbles asynchronously")
    ]
    add_bullet_points(slide22, bullets)
    
    code = (
        "@cl.on_message\n"
        "async def on_message(message: cl.Message):\n"
        "    history = cl.user_session.get(\"messages\")\n"
        "    history.append(HumanMessage(content=message.content))\n\n"
        "    assistant_msg = cl.Message(content=\"\")\n"
        "    await assistant_msg.send()\n\n"
        "    # Stream response chunks asynchronously\n"
        "    full_response = \"\"\n"
        "    async for chunk in aimodel.astream(history):\n"
        "        content = chunk.content\n"
        "        if isinstance(content, str):\n"
        "            full_response += content\n"
        "            await assistant_msg.stream_token(content)\n\n"
        "    await assistant_msg.update()\n"
        "    history.append(AIMessage(content=full_response))"
    )
    add_code_box(slide22, "main3_chainlit.py (Web Setup)", code)

    # ----------------------------------------------------
    # OVERWRITE SLIDE 23: Model Context Protocol (MCP)
    # ----------------------------------------------------
    print("✨ Overwriting Slide 23: Model Context Protocol...")
    slide23 = prs.slides[23]
    clear_slide(slide23)
    add_accent_bar(slide23)
    add_header(slide23, "Model Context Protocol (MCP)", category_text="THE ARCHITECTURE STANDARD")
    
    bullets = [
        ("The Integration Dilemma", "Before MCP, connecting an LLM to new tools required custom, brittle integration scripts that broke whenever APIs updated."),
        ("The Standard: 'USB-C' for AI", "An open protocol standard that standardizes how LLM applications securely connect to data sources, files, and local execution tools."),
        ("Dynamic Schema Discovery", "The LLM acts as a universal client. At runtime, it dynamically queries the MCP server, learns available tools, and binds them to its engine.")
    ]
    add_bullet_points(slide23, bullets, width=11.5)

    # ----------------------------------------------------
    # OVERWRITE SLIDE 24: Phase 4: Exposing Local Tools via MCP
    # ----------------------------------------------------
    print("✨ Overwriting Slide 24: Phase 4: Exposing Local Tools via MCP...")
    slide24 = prs.slides[24]
    clear_slide(slide24)
    add_accent_bar(slide24)
    add_header(slide24, "Phase 4: Exposing Local Tools via MCP")
    
    bullets = [
        ("Empowering the LLM with Tools", "We build a lightweight FastMCP server (`mcpserver.py`) exposing custom python utilities that the LLM discovers at runtime."),
        ("Baseline Tools: math & system time", "Includes exactly 2 simple tools (`add_numbers` and `get_time`) to easily verify clean tool integration without external API calls."),
        ("Modular Examples & Sandbox", "Includes modular servers (Weather geocoding, journal notes, advanced developer tools) and an interactive editing sandbox inside Colab!")
    ]
    add_bullet_points(slide24, bullets)
    
    code = (
        "from fastmcp import FastMCP\n"
        "from datetime import datetime\n\n"
        "mcp = FastMCP(\"MyAssistantTools\")\n\n"
        "@mcp.tool()\n"
        "def add_numbers(a: int, b: int) -> int:\n"
        "    \"\"\"\n"
        "    Add two numbers together.\n"
        "    \"\"\"\n"
        "    return a + b\n\n"
        "@mcp.tool()\n"
        "def get_time() -> dict:\n"
        "    \"\"\"\n"
        "    Returns active system time.\n"
        "    \"\"\"\n"
        "    dt = datetime.now().astimezone()\n"
        "    return {\"time\": dt.strftime(\"%H:%M:%S\")}\n\n"
        "if __name__ == \"__main__\":\n"
        "    mcp.run(transport=\"http\", port=8001)"
    )
    add_code_box(slide24, "mcpserver.py", code)

    # ----------------------------------------------------
    # APPEND NEW SLIDES (At the end)
    # ----------------------------------------------------
    layout_content = prs.slide_layouts[1]
    layout_two_content = prs.slide_layouts[3]
    
    # NEW SLIDE 25: The Mechanics of the Agentic Loop
    print("✨ Appending Slide 25: The Mechanics of the Agentic Loop...")
    slide25 = prs.slides.add_slide(layout_content)
    clear_slide(slide25)
    set_slide_background(slide25)
    add_accent_bar(slide25)
    add_header(slide25, "The Mechanics of the Agentic Loop", category_text="AGENT ORCHESTRATION")
    
    bullets = [
        ("Linear Chains vs. Agent Loops", "Standard chains flow straight from input to output. Agents require a dynamic reasoning loop: LLM decides, executes tools, and reviews outcomes."),
        ("1. Interception Protocol", "When the LLM needs facts, it returns a structured list of tool calls containing arguments, halting verbal text rendering."),
        ("2. Local Python Execution", "The client runtime intercepts the call, halts output, runs the designated Python tools locally, and injects results as `ToolMessage` context."),
        ("3. Grounded Verbalization", "The LLM is re-invoked with the new facts, reasons over the history, and verbalizes a correct, verified final answer to the user.")
    ]
    add_bullet_points(slide25, bullets, width=11.5)

    # NEW SLIDE 26: Phase 5: Building a Resilient Parallel Agent
    print("✨ Appending Slide 26: Phase 5: Resilient Parallel Agent...")
    slide26 = prs.slides.add_slide(layout_two_content)
    clear_slide(slide26)
    set_slide_background(slide26)
    add_accent_bar(slide26)
    add_header(slide26, "Phase 5: Resilient Parallel Agent")
    
    bullets = [
        ("Asynchronous Concurrency", "Sequential tool execution is slow. We use `asyncio.gather()` to execute all requested tool calls in parallel, dropping latencies by 60%+."),
        ("Exception Feedback Loop", "If a tool fails, we wrap the execution in a `try-except` block and feed the traceback back to the LLM. The LLM reads the error and self-corrects without crashing."),
        ("Native Visual Traces", "We integrate Chainlit's `cl.Step` to automatically render tool inputs, runtimes, and outputs dynamically under collapsible UI bubbles.")
    ]
    add_bullet_points(slide26, bullets)
    
    code = (
        "while response.tool_calls:\n"
        "    messages.append(response)\n"
        "    \n"
        "    # Spawn concurrent execution tasks\n"
        "    tasks = [\n"
        "        run_single_tool(tc, tool_map) \n"
        "        for tc in response.tool_calls\n"
        "    ]\n"
        "    \n"
        "    # Parallel execution speed offense!\n"
        "    tool_results = await asyncio.gather(*tasks)\n"
        "    \n"
        "    for result_msg in tool_results:\n"
        "        messages.append(result_msg)\n"
        "        \n"
        "    # Re-invoke LLM with grounded facts\n"
        "    response = await bound_model.ainvoke(messages)"
    )
    add_code_box(slide26, "main4_agent_chainlit.py", code)

    # NEW SLIDE 27: Concluding Thank You
    print("✨ Appending Slide 27: Concluding Thank You slide...")
    slide27 = prs.slides.add_slide(layout_content)
    clear_slide(slide27)
    set_slide_background(slide27)
    add_accent_bar(slide27)
    
    sub_box = slide27.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(0.5))
    p = sub_box.text_frame.paragraphs[0]
    p.text = "EESTEC LC THESSALONIKI  |  ARTIFICIAL INTELLIGENCE SYMPOSIUM"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    title_box = slide27.shapes.add_textbox(Inches(1.2), Inches(2.7), Inches(11.0), Inches(1.0))
    p = title_box.text_frame.paragraphs[0]
    p.text = "Thank You!"
    p.font.name = FONT_TITLE
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    info_box = slide27.shapes.add_textbox(Inches(1.2), Inches(4.0), Inches(11.0), Inches(2.5))
    tf = info_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Themistoklis Diamantopoulos"
    p.font.name = FONT_BODY
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = "thdiaman@issel.ee.auth.gr"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_ACCENT
    p2.space_before = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = "Intelligent Systems & Software Engineering Lab (ISSEL)\nElectrical and Computer Engineering Dept., Aristotle University of Thessaloniki, Greece"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_TEXT_MUTED
    p3.space_before = Pt(20)
    
    # Save the expanded slide presentation
    prs.save(expanded_path)
    print(f"🎉 Expanded presentation successfully saved in-place as '{expanded_path}'!")

if __name__ == "__main__":
    expand_presentation()
