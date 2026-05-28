"""
Slide PowerPoint Compiler
---------------------------
This script programmatically generates a premium, widescreen (16:9) PowerPoint presentation 
representing the restructured 5-Phase Hands-On AI Assistant Workshop.

It uses the `python-pptx` library to build custom, modern dark-mode slides with curated 
harmonies, slate layout blocks, and outstanding readable typography.

To compile:
  pip install python-pptx
  python build_slides.py
"""

import sys
import subprocess
import os

# --- DEFENSIVE ENVIRONMENT SETUP ---
# Ensure python-pptx is installed before compilation
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    print("🔄 Library 'python-pptx' is missing. Proactively installing it...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

# --- DESIGN THEME CONFIGURATION ---
# Premium slate dark mode palette
COLOR_BG = RGBColor(15, 23, 42)        # Deep slate (Slate 900)
COLOR_TEXT_PRIMARY = RGBColor(248, 250, 252) # Soft white (Slate 50)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)   # Soft gray (Slate 400)
COLOR_ACCENT = RGBColor(99, 102, 241)        # Electric Indigo (Indigo 500)
COLOR_ACCENT_BG = RGBColor(30, 41, 59)       # Dark slate box (Slate 800)
COLOR_GREEN = RGBColor(34, 197, 94)          # Success Green (Green 500)

FONT_TITLE = "Arial"
FONT_BODY = "Arial"

def set_slide_background(slide):
    """Fills slide background with premium deep slate color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

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
    """Adds a beautiful vertical highlight bar on the left edge of the slide."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.0), Inches(0.0), Inches(0.15), Inches(7.5)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_ACCENT
    bar.line.fill.background() # No border

def create_deck():
    # 1. Initialize presentation & set 16:9 widescreen aspect ratio
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_layout = prs.slide_layouts[6] # Blank slide layout
    
    # ----------------------------------------------------
    # SLIDE 1: Title Slide (Premium Center Glow)
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    
    # Left edge vertical accent line
    add_accent_bar(slide)
    
    # Subtitle / Symposium tag
    sub_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(0.5))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = "EESTEC LC THESSALONIKI  |  ARTIFICIAL INTELLIGENCE SYMPOSIUM"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    # Giant bold title
    title_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.7), Inches(11.0), Inches(1.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Part 2: Hands-On Workshop\nBuilding Your AI Assistant"
    p.font.name = FONT_TITLE
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    # Presenter and lab information
    info_box = slide.shapes.add_textbox(Inches(1.2), Inches(4.7), Inches(11.0), Inches(1.5))
    tf = info_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Evolving from Autocomplete to Autonomous Agentic Architectures"
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = "Intelligent Systems & Software Engineering Lab (ISSEL)\nElectrical and Computer Engineering Dept., Aristotle University of Thessaloniki, Greece"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(12)

    # ----------------------------------------------------
    # SLIDE 2: 5-Phase Progression Map
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "The 5-Phase Progression Map")
    
    # Context summary
    summary_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.5))
    p = summary_box.text_frame.paragraphs[0]
    p.text = "Our ladder of complexity: We introduce exactly one foundational system shift per phase to build up the agent."
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    # 5 Phase blocks
    phases = [
        ("Phase 1", "CLI Chatbot", "statelessness, messages, history, LCEL invoke"),
        ("Phase 2", "CLI with Streaming", "generator chunks, real-time streaming, latency drop"),
        ("Phase 3", "Chainlit Web UI", "skip Streamlit, async event callbacks, session storage"),
        ("Phase 4", "Local MCP Tools", "math, system clock, weather, journal notes, sandbox"),
        ("Phase 5", "Parallel Agent", "async gather, resilient error feedback, collapsible run logs")
    ]
    
    block_width = Inches(2.1)
    block_height = Inches(4.2)
    spacing = Inches(0.3)
    start_left = Inches(0.8)
    top_pos = Inches(2.3)
    
    for i, (ph, name, desc) in enumerate(phases):
        left_pos = start_left + i * (block_width + spacing)
        
        # Add visual block shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, block_width, block_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_ACCENT_BG
        shape.line.color.rgb = COLOR_ACCENT if i == 4 else COLOR_TEXT_MUTED
        shape.line.width = Pt(2.5 if i == 4 else 1)
        
        # Text inside block
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)
        
        # Phase header
        p = tf.paragraphs[0]
        p.text = ph.upper()
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        
        # Phase Name
        p2 = tf.add_paragraph()
        p2.text = name
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_PRIMARY
        p2.space_before = Pt(8)
        
        # Phase Description
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_before = Pt(16)

    # ----------------------------------------------------
    # SLIDE 3: Phase 1: The CLI Chatbot
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Phase 1: The CLI Chatbot (main1.py)")
    
    # Left bullet points
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("LLMs are Stateless by Design", "The API endpoints have no memory. Every prompt is a brand-new, isolated request. Memory must be managed manually on the client side."),
        ("The Message Schema", "We represent chat content using LangChain structure classes:\n• SystemMessage: Steers personality & boundaries\n• HumanMessage: Represents the user's input\n• AIMessage: The assistant's text response"),
        ("Message History Compilation", "We maintain a persistent Python list context: messages = [system_prompt]. On every turn, we append inputs, invoke the model, and record replies.")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(18)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)
        
    # Right code snippet box
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.fill.background()
    
    tf_code = code_bg.text_frame
    tf_code.margin_left = tf_code.margin_right = Inches(0.2)
    tf_code.margin_top = Inches(0.2)
    tf_code.word_wrap = True
    
    p = tf_code.paragraphs[0]
    p.text = "main1.py (Core Message Loop)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_code.add_paragraph()
    p2.text = (
        "messages = [SystemMessage(content=prompt)]\n\n"
        "while True:\n"
        "    user_input = input(\"\\nYou: \")\n"
        "    if user_input.lower() in [\"exit\"]: break\n\n"
        "    # Append new user interaction\n"
        "    messages.append(\n"
        "        HumanMessage(content=user_input)\n"
        "    )\n\n"
        "    # Blocking invoke execution\n"
        "    response = aimodel.invoke(messages)\n"
        "    print(f\"\\nAI: {response.content}\")\n\n"
        "    # Save response in context memory\n"
        "    messages.append(response)"
    )
    p2.font.name = "Courier New"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(12)

    # ----------------------------------------------------
    # SLIDE 4: Phase 2: CLI with Streaming
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Phase 2: CLI with Streaming (main2.py)")
    
    # Left text block
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("The UX Latency Problem", "Waiting for a complete 300-word model response creates an artificial pause of 10+ seconds, causing user impatience and poor application feel."),
        ("The Generator Paradigm Shift", "Instead of a single blocking API payload, the server starts yielding individual token chunks the moment they are generated."),
        ("Implementing stream()", "We swap aimodel.invoke() with the aimodel.stream() generator, iterating over chunks and immediately flushing console outputs.")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(20)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)
        
    # Right code snippet box
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.fill.background()
    
    tf_code = code_bg.text_frame
    tf_code.margin_left = tf_code.margin_right = Inches(0.2)
    tf_code.margin_top = Inches(0.2)
    tf_code.word_wrap = True
    
    p = tf_code.paragraphs[0]
    p.text = "main2.py (Token Stream Iteration)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_code.add_paragraph()
    p2.text = (
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
    p2.font.name = "Courier New"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(16)

    # ----------------------------------------------------
    # SLIDE 5: Model Context Protocol (MCP)
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Model Context Protocol (MCP)", category_text="THE ARCHITECTURE STANDARD")
    
    # Left column: The Standard
    left_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    
    p = tf_left.paragraphs[0]
    p.text = "The 'USB-C' for Artificial Intelligence"
    p.font.name = FONT_TITLE
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf_left.add_paragraph()
    p2.text = (
        "Historically, connecting an LLM to external APIs required custom, brittle integration scripts "
        "that broke whenever endpoints updated. \n\n"
        "MCP established a standard runtime protocol. Instead of hardcoding API bindings, "
        "the LLM acts as a universal client that dynamically queries tool schemas from "
        "MCP servers at runtime."
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(14)
    
    # Right column: Architectural diagram (Visual Blocks)
    # LLM Box
    b_llm = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(2.2), Inches(4.5), Inches(1.0))
    b_llm.fill.solid()
    b_llm.fill.fore_color.rgb = COLOR_ACCENT
    b_llm.line.fill.background()
    p = b_llm.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "MCP CLIENT (LLM / Application)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    # Arrow down
    arrow = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.45), Inches(3.4), Inches(0.6), Inches(0.8))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = COLOR_TEXT_MUTED
    arrow.line.fill.background()
    
    # Server Box
    b_srv = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(4.4), Inches(4.5), Inches(2.0))
    b_srv.fill.solid()
    b_srv.fill.fore_color.rgb = COLOR_ACCENT_BG
    b_srv.line.color.rgb = COLOR_ACCENT
    
    tf_srv = b_srv.text_frame
    tf_srv.word_wrap = True
    tf_srv.margin_top = Inches(0.2)
    
    p = tf_srv.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "MCP SERVER (Microservice)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf_srv.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = (
        "• Tools (Recursive searches, HTML scrapers)\n"
        "• Resources (File assets, Live audit logs)\n"
        "• Schema Discovery (Autogenerated JSON)"
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(12)

    # ----------------------------------------------------
    # SLIDE 6: Phase 3: Bypassing Streamlit for Chainlit
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Phase 3: Bypassing Streamlit for Chainlit (main3_chainlit.py)")
    
    # Left text
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("The Case Against Streamlit", "Streamlit is designed for analytical dashboards. For chat agents, it is a poor fit: it forces complex browser-reloads, lacks native async generators, and demands verbose, fragile session state management."),
        ("Chainlit: Conversational UI Native", "A lightweight, async framework designed specifically for conversational AI applications. Provides built-in session handlers and rich media layouts."),
        ("Async Lifecycle Callbacks", "• @cl.on_chat_start: Sets system prompts & session memory\n• @cl.on_message: Handles prompts concurrently inside fully asynchronous, non-blocking loops")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(14)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)
        
    # Right code snippet box
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.fill.background()
    
    tf_code = code_bg.text_frame
    tf_code.margin_left = tf_code.margin_right = Inches(0.2)
    tf_code.margin_top = Inches(0.2)
    tf_code.word_wrap = True
    
    p = tf_code.paragraphs[0]
    p.text = "main3_chainlit.py (Chainlit Async Chat)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_code.add_paragraph()
    p2.text = (
        "@cl.on_message\n"
        "async def on_message(message: cl.Message):\n"
        "    # Get messages from session storage\n"
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
    p2.font.name = "Courier New"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(8)

    # ----------------------------------------------------
    # SLIDE 7: Phase 4: Creating an Advanced MCP Server
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Phase 4: Exposing Local Tools via MCP (mcpserver.py)")
    
    # Left column: Explanations
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("The Challenge: Standardized Local APIs", "Model Context Protocol creates an open runtime communication standard. Parameter type hints and docstrings generate dynamic JSON schemas for LLMs."),
        ("Baseline Tools: math & system clock", "Includes add_numbers(a, b) and get_time() to quickly verify clean, robust protocol execution without API network dependencies."),
        ("Modular Example Servers in Repo", "Includes mcp_simple.py, mcp_weather.py (REST forecasting), mcp_journal.py (file system storage), and mcp_advanced.py (AST analysis)."),
        ("Colab Interactive Sandbox", "Students edit, add, or remove tools inside their notebook directly to compile and launch mcpserver.py on Port 8001!")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(12)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(3)
        
    # Right code snippet box
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.fill.background()
    
    tf_code = code_bg.text_frame
    tf_code.margin_left = tf_code.margin_right = Inches(0.2)
    tf_code.margin_top = Inches(0.2)
    tf_code.word_wrap = True
    
    p = tf_code.paragraphs[0]
    p.text = "mcpserver.py (Baseline Tools Server)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_code.add_paragraph()
    p2.text = (
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
    p2.font.name = "Courier New"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(8)

    # ----------------------------------------------------
    # SLIDE 8: The Mechanics of the Agentic Loop
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "The Mechanics of the Agentic Loop", category_text="AGENT ORCHESTRATION")
    
    # Left column: Explanations
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("The Interception Protocol", "When an LLM determines it needs external data, it returns a structured list of tool calls containing arguments, halting verbal text rendering."),
        ("Executing the Intercept", "The client-side runtime detects these tool calls, halts output streaming, extracts the arguments, and executes the designated Python tools locally."),
        ("Grounding and Context Feedback", "The execution results are packaged into a list of ToolMessage objects. These are appended to the conversation history, and the LLM is immediately re-invoked."),
        ("Final Verbalization", "The LLM uses this injected factual context to generate a correct, grounded, and verified final explanation, then outputs it to the user.")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(14)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)
        
    # Right Column: Visual execution path (Diagram)
    # Start Box
    s_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(1.8), Inches(4.5), Inches(0.8))
    s_box.fill.solid()
    s_box.fill.fore_color.rgb = COLOR_ACCENT_BG
    s_box.line.color.rgb = COLOR_ACCENT
    p = s_box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "1. User Prompt Input"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    # Loop box
    l_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(3.0), Inches(4.5), Inches(2.2))
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = COLOR_ACCENT_BG
    l_box.line.color.rgb = COLOR_ACCENT
    l_box.line.width = Pt(2)
    tf_l = l_box.text_frame
    tf_l.word_wrap = True
    tf_l.margin_top = Inches(0.15)
    
    p = tf_l.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "🔄 THE ACTIVE AGENTIC CYCLE"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_l.add_paragraph()
    p2.text = (
        "2. LLM requests Tool Execution\n"
        "3. Local Python runner executes Tools\n"
        "4. Output injected as ToolMessage context\n"
        "5. LLM re-evaluates message history"
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(12)
    
    # End Box
    e_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(5.6), Inches(4.5), Inches(0.8))
    e_box.fill.solid()
    e_box.fill.fore_color.rgb = COLOR_GREEN
    e_box.line.fill.background()
    p = e_box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "6. Final Streamed Answer"
    p.font.name = FONT_TITLE
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # ----------------------------------------------------
    # SLIDE 9: Phase 5: Building a Resilient Parallel Agent
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Phase 5: Building a Resilient Parallel Agent (main4_agent_chainlit.py)")
    
    # Left column: Explanations
    txt_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf = txt_box.text_frame
    tf.word_wrap = True
    
    bullets = [
        ("Speed Offense: Asynchronous Parallel Execution", "Sequential execution creates massive user delay. We implement asyncio.gather() to fire all requested tool calls concurrently, dropping latencies by over 60%!"),
        ("Defensive Safety: Exception Feedback Loops", "If an API call fails (network drop, invalid path), standard loops crash. We wrap executions in a try-except, feeding the error back to the LLM as ToolMessage. The LLM parses it and self-corrects."),
        ("Seamless UX: Native collapsible Step Logs", "We use Chainlit's cl.Step class, which automatically maps tool inputs, execution times, and outputs directly into collapsible parent-child logs.")
    ]
    
    for i, (title, desc) in enumerate(bullets):
        p_title = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p_title.text = f"• {title}"
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_ACCENT
        if i > 0: p_title.space_before = Pt(14)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)
        
    # Right code snippet box
    code_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    code_bg.fill.solid()
    code_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    code_bg.line.fill.background()
    
    tf_code = code_bg.text_frame
    tf_code.margin_left = tf_code.margin_right = Inches(0.2)
    tf_code.margin_top = Inches(0.2)
    tf_code.word_wrap = True
    
    p = tf_code.paragraphs[0]
    p.text = "main4_agent_chainlit.py (Parallel Agent Loop)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_code.add_paragraph()
    p2.text = (
        "while response.tool_calls:\n"
        "    history.append(response)\n"
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
        "        history.append(result_msg)\n"
        "        \n"
        "    # Re-invoke LLM with grounded facts\n"
        "    response = await bound_model.ainvoke(history)"
    )
    p2.font.name = "Courier New"
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(14)

    # ----------------------------------------------------
    # SLIDE 10: Summary & Workshop Challenge
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    add_accent_bar(slide)
    add_header(slide, "Summary & Workshop Challenge", category_text="KEY TAKEAWAYS")
    
    # Left block
    left_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.0))
    tf_left = left_box.text_frame
    tf_left.word_wrap = True
    
    p = tf_left.paragraphs[0]
    p.text = "Summary of Key Lessons"
    p.font.name = FONT_TITLE
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tf_left.add_paragraph()
    p2.text = (
        "• **Memory is a Client-Side state**: History must be accumulated and re-sent.\n\n"
        "• **MCP standardizes capabilities**: Expose complex system processes under an open runtime standard.\n\n"
        "• **Bypass Streamlit for Chat**: Use specialized conversational UIs like Chainlit for native token streams and collapsible logs.\n\n"
        "• **Build Resilient Loops**: Concurrent tool runs (`asyncio.gather()`) and fallback error logging are essential for production-grade AI systems."
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_before = Pt(14)
    
    # Right block: The Challenge (Accent border container)
    ch_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    ch_bg.fill.solid()
    ch_bg.fill.fore_color.rgb = COLOR_ACCENT_BG
    ch_bg.line.color.rgb = COLOR_ACCENT
    ch_bg.line.width = Pt(2)
    
    tf_ch = ch_bg.text_frame
    tf_ch.margin_left = tf_ch.margin_right = Inches(0.3)
    tf_ch.margin_top = Inches(0.3)
    tf_ch.word_wrap = True
    
    p = tf_ch.paragraphs[0]
    p.text = "🚀 YOUR HANDS-ON CHALLENGE"
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    
    p2 = tf_ch.add_paragraph()
    p2.text = (
        "1. Open **`mcpserver.py`** and write a third tool:\n"
        "   `travel_journal(action: str, content: str = '') -> str`\n"
        "   This tool should append preferences and trip notes to 'travel_journal.txt' or read them on demand.\n\n"
        "2. Launch **`main4_agent_chainlit.py`** and prompt your agent:\n"
        "   *\"Check the weather in Athens, and write inside my travel journal that Athens is sunny!\"*\n\n"
        "3. Verify that the Parallel Agent executes these tool runs in parallel and handles user dialogue seamlessly!"
    )
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(16)
    
    # 6. Save presentation to file
    output_filename = "hands_on_workshop.pptx"
    prs.save(output_filename)
    print(f"🎉 Widescreen PowerPoint Presentation compiled successfully as '{output_filename}'!")

if __name__ == "__main__":
    create_deck()
