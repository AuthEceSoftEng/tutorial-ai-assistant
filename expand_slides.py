"""
Slide Deck Expansion Script (Improved)
----------------------------
This script opens the user's original `finalpresentation.pptx` slide deck, 
removes the temporary hands-on placeholder slides (Slides 19-23), 
inserts our restructured 5-Phase workshop slides in their place, 
and moves the concluding 'Thank You' slide back to the very end.

It uses the original presentation's pre-defined slide layouts (Layout 1 for Content, 
Layout 3 for Side-by-Side Code/Concepts) so the new slides perfectly match the existing 
presentation's background styles, fonts, and borders.

To run:
  python expand_slides.py
"""

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def add_bullet_points(content_placeholder, points):
    """Fills a content placeholder with rich bullet points (bold titles, muted descriptions)."""
    tf = content_placeholder.text_frame
    tf.word_wrap = True
    
    # Use first paragraph for first bullet
    p_first = tf.paragraphs[0]
    p_first.space_after = Pt(8)
    
    for i, (title, desc) in enumerate(points):
        p = p_first if i == 0 else tf.add_paragraph()
        p.space_after = Pt(12)
        p.level = 0
        
        # Add bold title
        run_title = p.add_run()
        run_title.text = f"{title}: "
        run_title.font.bold = True
        run_title.font.size = Pt(14)
        
        # Add normal description
        run_desc = p.add_run()
        run_desc.text = desc
        run_desc.font.size = Pt(13)

def add_code_box(content_placeholder, title, code_text):
    """Formats a content placeholder as a premium dark-mode code frame."""
    tf = content_placeholder.text_frame
    tf.word_wrap = True
    
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.15)
    
    p_title = tf.paragraphs[0]
    p_title.text = f"💻 {title}"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(11)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(99, 102, 241) # Indigo accent
    p_title.space_after = Pt(8)
    
    p_code = tf.add_paragraph()
    p_code.text = code_text
    p_code.font.name = "Courier New"
    p_code.font.size = Pt(9.5)
    p_code.font.color.rgb = RGBColor(226, 232, 240) # Light gray code

def expand_presentation():
    original_path = "finalpresentation.pptx"
    expanded_path = "finalpresentation_expanded.pptx"
    
    print(f"🔄 Loading '{original_path}'...")
    prs = Presentation(original_path)
    sldIdLst = prs.slides._sldIdLst
    
    # 1. Delete placeholders (indices 19 to 23)
    # Deleting in reverse order to keep indices stable
    print("🧹 Removing temporary hands-on placeholder slides...")
    for idx in sorted([19, 20, 21, 22, 23], reverse=True):
        del sldIdLst[idx]
        
    # At this point, the "Thank You!" slide (originally at index 24) is now at index 19.
    
    # Layouts in original presentation:
    # 1: Title and Content
    # 3: Two Content (perfect for side-by-side concepts and code!)
    layout_content = prs.slide_layouts[1]
    layout_two_content = prs.slide_layouts[3]
    
    # 2. Add our new restructured slides (which will be appended after index 19)
    # ----------------------------------------------------
    # NEW SLIDE: The 5-Phase Progression Map
    # ----------------------------------------------------
    print("✨ Creating Slide: The 5-Phase Progression Map...")
    slide = prs.slides.add_slide(layout_content)
    slide.shapes.title.text = "The 5-Phase Progression Map"
    
    bullets = [
        ("Phase 1: CLI Chatbot (main1.py)", "Stateless LLM communication & manual message history lists."),
        ("Phase 2: CLI with Streaming (main2.py)", "Yielding token chunks dynamically via generators for a 90% latency drop."),
        ("Phase 3: Chainlit Web UI (main3_chainlit.py)", "Bypassing Streamlit entirely in favor of an async-native conversational UI."),
        ("Phase 4: Advanced MCP Server (mcpserver_advanced.py)", "Exposing recursive code searches, HTML web scraping, and persistent file logging."),
        ("Phase 5: Resilient Parallel Agent (main4_agent_chainlit.py)", "Culmination. Parallel async execution, exception safety, and collapsible traces.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
    # ----------------------------------------------------
    # NEW SLIDE: Phase 1: The CLI Chatbot
    # ----------------------------------------------------
    print("✨ Creating Slide: Phase 1: The CLI Chatbot...")
    slide = prs.slides.add_slide(layout_two_content)
    slide.shapes.title.text = "Phase 1: The CLI Chatbot (main1.py)"
    
    bullets = [
        ("Stateless LLM Endpoints", "API endpoints do not store history. Memory is managed client-side using arrays."),
        ("Message Schemas", "LangChain structure classes:\n• SystemMessage: Sets boundaries\n• HumanMessage: User input\n• AIMessage: Model response"),
        ("Invoke Loop", "We append interactions to a list and call aimodel.invoke(messages) on every turn.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
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
    add_code_box(slide.placeholders[2], "main1.py (Core Loop)", code)
    
    # ----------------------------------------------------
    # NEW SLIDE: Phase 2: CLI with Streaming
    # ----------------------------------------------------
    print("✨ Creating Slide: Phase 2: CLI with Streaming...")
    slide = prs.slides.add_slide(layout_two_content)
    slide.shapes.title.text = "Phase 2: CLI with Streaming (main2.py)"
    
    bullets = [
        ("The Latency Bottleneck", "Waiting for a model to finish writing 200+ words creates long, unnatural pauses of 10+ seconds."),
        ("The Stream Solution", "Instead of a single blocking API payload, the server starts yielding individual token chunks immediately."),
        ("Generator Loop", "We swap .invoke() with .stream(), iterating over chunks and immediately flushing console outputs with flush=True.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
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
    add_code_box(slide.placeholders[2], "main2.py (Streaming)", code)

    # ----------------------------------------------------
    # NEW SLIDE: Phase 3: Moving to a Web UI with Chainlit
    # ----------------------------------------------------
    print("✨ Creating Slide: Phase 3: Moving to a Web UI...")
    slide = prs.slides.add_slide(layout_two_content)
    slide.shapes.title.text = "Phase 3: Bypassing Streamlit for Chainlit"
    
    bullets = [
        ("Why Streamlit Fails here", "Streamlit is built for data analytics. For chat apps, it forces page-reloads, lacks async streaming support, and requires verbose session state hacks."),
        ("Chainlit Advantage", "Built specifically for AI agents, providing native collapsible runs, streaming chat, and simple event callbacks."),
        ("Async Lifecycle Events", "• @cl.on_chat_start: Sets prompts\n• @cl.on_message: Handles messages")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
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
    add_code_box(slide.placeholders[2], "main3_chainlit.py (Web Setup)", code)

    # ----------------------------------------------------
    # NEW SLIDE: Model Context Protocol (MCP)
    # ----------------------------------------------------
    print("✨ Creating Slide: Model Context Protocol...")
    slide = prs.slides.add_slide(layout_content)
    slide.shapes.title.text = "Model Context Protocol (MCP)"
    
    bullets = [
        ("The 'USB-C' for Artificial Intelligence", "Historically, connecting an LLM to external APIs required custom, brittle integration scripts that broke when endpoints updated. MCP standardizes client-server integrations."),
        ("MCP Server", "A separate lightweight microservice that exposes resources (file systems, dynamic data assets) and tools (python execution functions)."),
        ("Dynamic Schema Discovery", "The LLM acts as a universal client. At runtime, it queries the MCP server, dynamically learns the available tool parameters, and binds them to its reasoning engine.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)

    # ----------------------------------------------------
    # NEW SLIDE: Phase 4: Creating an Advanced MCP Server
    # ----------------------------------------------------
    print("✨ Creating Slide: Phase 4: Advanced MCP Server...")
    slide = prs.slides.add_slide(layout_two_content)
    slide.shapes.title.text = "Phase 4: Creating an Advanced MCP Server"
    
    bullets = [
        ("Realistic Tool Scope", "Rather than trivial math adders, we author a system-utility and research harvesting server using FastMCP."),
        ("Tool 1: search_workspace_code", "Recursively scans files in the directory for keywords and returns line snippets (local code analyst)."),
        ("Tool 2: harvest_web_data", "HTTP web scraper extracting text only from semantic HTML tags, avoiding junk elements."),
        ("Tool 3: write_audit_log", "Writes timed action events directly in assistant_audit.log, proving write capabilities.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
    code = (
        "from fastmcp import FastMCP\n"
        "import os\n\n"
        "mcp = FastMCP(\"WorkspaceHarvester\")\n\n"
        "@mcp.tool()\n"
        "def write_audit_log(event: str, outcome: str) -> str:\n"
        "    \"\"\"\n"
        "    Writes a structured action event into the file\n"
        "    'assistant_audit.log' with a timestamp.\n"
        "    \"\"\"\n"
        "    log_file = \"assistant_audit.log\"\n"
        "    timestamp = datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")\n"
        "    entry = f\"[{timestamp}] EVENT: {event} | {outcome}\\n\"\n"
        "    \n"
        "    with open(log_file, \"a\") as lf:\n"
        "        lf.write(entry)\n"
        "    return f\"Log written: {entry.strip()}\""
    )
    add_code_box(slide.placeholders[2], "mcpserver_advanced.py", code)

    # ----------------------------------------------------
    # NEW SLIDE: The Mechanics of the Agentic Loop
    # ----------------------------------------------------
    print("✨ Creating Slide: The Mechanics of the Agentic Loop...")
    slide = prs.slides.add_slide(layout_content)
    slide.shapes.title.text = "The Mechanics of the Agentic Loop"
    
    bullets = [
        ("1. Interception Protocol", "When the LLM determines it needs facts/system data, it responds with a structured list of tool calls containing arguments, halting verbal text rendering."),
        ("2. Local Python Execution", "The client-side runtime intercepts the list, halts output streaming, extracts the arguments, and executes the designated Python tools locally."),
        ("3. Grounding Context Feedback Loop", "The execution results are packaged into a list of ToolMessage objects, appended to the history, and the LLM is immediately re-invoked."),
        ("4. Final Verbalization", "The LLM uses this injected factual context to generate a correct, grounded final explanation, then streams it smoothly to the user.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)

    # ----------------------------------------------------
    # NEW SLIDE: Phase 5: Building a Resilient Parallel Agent
    # ----------------------------------------------------
    print("✨ Creating Slide: Phase 5: Resilient Parallel Agent...")
    slide = prs.slides.add_slide(layout_two_content)
    slide.shapes.title.text = "Phase 5: Resilient Parallel Agent"
    
    bullets = [
        ("Speed Offense: Asynchronous Concurrency", "Sequential execution is slow. We use asyncio.gather() to fire all requested tool calls concurrently, dropping latencies by 60%+."),
        ("Defensive Safety: Exception Feedback Loop", "If a tool fails, we wrap the call in a try-except, feeding the error back to the LLM. The LLM reads the error and self-corrects without crashing."),
        ("Collapsible Traces", "We use Chainlit's cl.Step class, which automatically maps tool runs beautifully under collapsible UI steps.")
    ]
    add_bullet_points(slide.placeholders[1], bullets)
    
    code = (
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
    add_code_box(slide.placeholders[2], "main4_agent_chainlit.py", code)

    # 3. Rearrange the XML elements: Move the "Thank You" slide (at index 19) to the very end of sldIdLst
    print("🏁 Moving 'Thank You' slide to the end of the deck...")
    thank_you_elem = sldIdLst[19]
    del sldIdLst[19]                # Remove from current index 19
    sldIdLst.append(thank_you_elem)  # Append back to the end!
    
    # 4. Save the expanded slide presentation
    prs.save(expanded_path)
    print(f"🎉 Expanded presentation saved successfully as '{expanded_path}'!")

if __name__ == "__main__":
    expand_presentation()
