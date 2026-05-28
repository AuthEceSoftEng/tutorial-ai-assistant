"""
Phase 4: Creating an Advanced MCP Server
----------------------------------------
This file implements a Model Context Protocol (MCP) server named 'WorkspaceHarvester' 
using FastMCP. 

This server exposes a highly practical, advanced developer suite of tools:
1. `web_search_duckduckgo`: Performs a real-time web search for any query to fetch live data.
2. `git_workspace_copilot`: Runs git commands to check status, fetch diffs, or auto-commit changes.
3. `analyze_code_quality`: Static AST analysis of Python files, generating graded reviews.
4. `generate_project_documentation`: Automatically parses python docstrings/functions to build README.md.

To run this server:
  python mcpserver_advanced.py
"""

import os
import requests
import re
import ast
import subprocess
from datetime import datetime
from html.parser import HTMLParser
from fastmcp import FastMCP

# Initialize the FastMCP Server
mcp = FastMCP("WorkspaceHarvester")

# --- DUCKDUCKGO HTML RESULTS PARSER ---
class DDGParser(HTMLParser):
    """
    A robust, zero-dependency HTML parser for parsing DuckDuckGo search results.
    Identifies target result classes and extracts titles, links, and snippets safely.
    """
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_snippet = False
        self.in_title = False
        self.current_result = None
        self.snippet_accum = []
        self.title_accum = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        
        # Check class names regardless of HTML tag element
        if "result__url" in cls:
            self.current_result = {
                "title": "",
                "link": attrs_dict.get("href", ""),
                "snippet": ""
            }
            self.in_title = True
            self.title_accum = []
        elif "result__snippet" in cls:
            self.in_snippet = True
            self.snippet_accum = []

    def handle_endtag(self, tag):
        if self.in_title:
            if self.current_result:
                self.current_result["title"] = "".join(self.title_accum).strip()
            self.in_title = False
        elif self.in_snippet:
            if self.current_result:
                self.current_result["snippet"] = "".join(self.snippet_accum).strip()
                # Clean redirection link
                link = self.current_result["link"]
                if "uddg=" in link:
                    from urllib.parse import unquote
                    match = re.search(r"uddg=([^&]+)", link)
                    if match:
                        link = unquote(match.group(1))
                self.current_result["link"] = link
                
                # Verify and append result
                if self.current_result["title"] and self.current_result["link"]:
                    self.results.append(self.current_result)
                self.current_result = None
            self.in_snippet = False

    def handle_data(self, data):
        if self.in_title:
            self.title_accum.append(data)
        elif self.in_snippet:
            self.snippet_accum.append(data)


# --- TOOL 1: WEB SEARCH ---
@mcp.tool()
def web_search_duckduckgo(query: str) -> str:
    """
    Performs a real-time web search for any query using DuckDuckGo HTML search.
    Returns the top 5 search result titles, secure URLs, and content snippets.
    Allows the AI assistant to answer questions using live web data!
    """
    import urllib.parse
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"❌ Web search failed. Service returned HTTP Status Code: {response.status_code}"
            
        parser = DDGParser()
        parser.feed(response.text)
        
        if not parser.results:
            return "🔍 Search completed, but no web results were returned. Try phrasing your query differently."
            
        formatted_results = []
        formatted_results.append(f"🌐 **Web Search Results for:** *\"{query}\"*\n")
        
        for idx, res in enumerate(parser.results[:5], 1):
            title = res["title"]
            link = res["link"]
            snippet = res["snippet"]
            formatted_results.append(f"{idx}. **[{title}]({link})**")
            formatted_results.append(f"   *{snippet}*\n")
            
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"❌ Search error: {str(e)}"


# --- TOOL 2: GIT WORKSPACE COPILOT ---
@mcp.tool()
def git_workspace_copilot(action: str, commit_message: str = None) -> str:
    """
    Interacts with the Git repository in the current workspace.
    Supported actions:
    - 'status': Returns the active git status (unstaged/untracked files).
    - 'diff': Returns the git diff of unstaged/staged changes.
    - 'commit': Stages all changes (git add .) and commits them with a beautiful commit_message.
    """
    action = action.lower().strip()
    if action not in ["status", "diff", "commit"]:
        return "❌ Invalid action. Supported actions: 'status', 'diff', 'commit'"
        
    try:
        # Check if git is initialized
        if not os.path.exists(".git"):
            # Try to run git init if not exists
            try:
                subprocess.run(["git", "init"], check=True, stdout=subprocess.DEVNULL)
                # Create a git config if not set (for Colab environments)
                subprocess.run(["git", "config", "--global", "user.email", "workshop@student.com"], check=False)
                subprocess.run(["git", "config", "--global", "user.name", "AI Workshop Student"], check=False)
            except:
                return "⚠️ Git is not initialized in this directory and initialization failed."
            
        if action == "status":
            res = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            return f"📂 **Git Status Output:**\n\n{output if output else '✅ No changes. Workspace is clean!'}"
            
        elif action == "diff":
            res = subprocess.run(["git", "diff"], capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            if not output:
                # Also check staged changes
                res = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, check=True)
                output = res.stdout.strip()
            return f"📝 **Git Diff Output:**\n\n```diff\n{output if output else '✅ No unstaged or staged changes to show.'}\n```"
            
        elif action == "commit":
            if not commit_message:
                return "❌ Commit action requires a 'commit_message'."
            # Stage all files
            subprocess.run(["git", "add", "."], check=True)
            # Commit changes
            res = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True, check=True)
            return f"🚀 **Git Commit Successful!**\n\n```\n{res.stdout.strip()}\n```"
            
    except Exception as e:
        return f"❌ Git command failed: {str(e)}"


# --- TOOL 3: PYTHON AST CODE QUALITY ANALYZER ---
@mcp.tool()
def analyze_code_quality(file_path: str) -> str:
    """
    Parses and checks any local Python file for code quality, syntax correctness, and best practices.
    Uses AST (Abstract Syntax Trees) to perform static analysis and returns a scored, detailed review.
    """
    if not file_path.endswith(".py"):
        return "❌ Code quality check is only supported for Python (.py) files."
        
    if not os.path.exists(file_path):
        return f"❌ File '{file_path}' not found in workspace."
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        # Syntax check using AST parsing
        try:
            tree = ast.parse(code)
        except SyntaxError as se:
            return (
                f"❌ **Syntax Error Detected in {file_path}!**\n\n"
                f"⚠️ **Line {se.lineno}, Col {se.offset}**: {se.msg}\n"
                f"```python\n{se.text.strip() if se.text else ''}\n```"
            )
            
        score = 10.0
        deductions = []
        info = {
            "functions": 0,
            "classes": 0,
            "nested_loops": 0,
            "missing_docstrings": 0,
            "print_statements": 0,
            "silent_exceptions": 0
        }
        
        # Analyze AST node tree
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                info["functions"] += 1
                # Check for docstrings
                if not ast.get_docstring(node):
                    info["missing_docstrings"] += 1
                    deductions.append(f"• Function `{node.name}()` is missing a docstring (-0.5)")
                    score -= 0.5
                # Check for argument count
                arg_count = len(node.args.args)
                if arg_count > 5:
                    deductions.append(f"• Function `{node.name}()` has too many arguments ({arg_count} > 5) (-0.5)")
                    score -= 0.5
                    
            elif isinstance(node, ast.ClassDef):
                info["classes"] += 1
                if not ast.get_docstring(node):
                    deductions.append(f"• Class `{node.name}` is missing a docstring (-0.5)")
                    score -= 0.5
                    
            elif isinstance(node, (ast.For, ast.While)):
                # Search for nested loops
                for child in ast.walk(node):
                    if child is not node and isinstance(child, (ast.For, ast.While)):
                        info["nested_loops"] += 1
                        deductions.append(f"• Nested loop detected inside line {node.lineno} (Complexity risk) (-0.5)")
                        score -= 0.5
                        break
                        
            elif isinstance(node, ast.Call):
                # Check for print() instead of logging
                if isinstance(node.func, ast.Name) and node.func.id == "print":
                    info["print_statements"] += 1
                    
            elif isinstance(node, ast.ExceptHandler):
                # Check for silent exception handling
                is_silent = True
                for stmt in node.body:
                    if not isinstance(stmt, ast.Pass):
                        is_silent = False
                if is_silent:
                    info["silent_exceptions"] += 1
                    deductions.append(f"• Silent/empty exception handler at line {node.lineno} (-1.0)")
                    score -= 1.0
                    
        # Apply print statement deduction once
        if info["print_statements"] > 0:
            deductions.append(f"• Found {info['print_statements']} print() statements. Suggest using standard `logging` library (-0.5)")
            score -= 0.5
            
        score = max(0.0, score)
        
        # Build Markdown Report
        report = []
        report.append(f"## 📊 Code Quality Report: `{file_path}`")
        
        # Color score indicator
        if score >= 9.0:
            badge = "🟢 Excellent"
        elif score >= 7.0:
            badge = "🟡 Good"
        else:
            badge = "🔴 Action Required"
            
        report.append(f"**Overall Score:** {score:.1f} / 10.0 ({badge})\n")
        report.append(f"### 🔍 Metrics Summary:")
        report.append(f"- 📁 Functions Analysed: {info['functions']}")
        report.append(f"- 🏛️ Classes Analysed: {info['classes']}")
        report.append(f"- 🔄 Nested Loops Found: {info['nested_loops']}")
        report.append(f"- 🖨️ print() Statements: {info['print_statements']}")
        report.append(f"- 🤫 Silent Exception Blocks: {info['silent_exceptions']}\n")
        
        report.append("### 📝 Detailed Findings:")
        if deductions:
            report.extend(deductions)
        else:
            report.append("✅ No quality violations found! Beautiful code!")
            
        return "\n".join(report)
        
    except Exception as e:
        return f"❌ Failed to parse code for review: {str(e)}"


# --- TOOL 4: AUTO PROJECT README GENERATOR ---
@mcp.tool()
def generate_project_documentation() -> str:
    """
    Scans the current directory for Python files, parses their purpose, classes, and tools,
    and automatically generates a beautifully formatted README.md document that explains the project.
    Writes the README.md directly to the project root.
    """
    python_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "venv", "__pycache__", "node_modules"}]
        for file in files:
            if file.endswith(".py") and not file.startswith("~$"):
                python_files.append(os.path.join(root, file))
                
    if not python_files:
        return "⚠️ No Python (.py) files found in the directory to generate documentation for."
        
    doc_sections = []
    doc_sections.append("# 🤖 AI-Assistant Tutorial Project Documentation")
    doc_sections.append("Welcome to the automatically generated workspace documentation. This workspace contains a fully functional 5-phase interactive AI assistant tutorial stack.\n")
    
    doc_sections.append("## 📁 File Structure & Modules Summary\n")
    
    for fp in sorted(python_files):
        rel_path = os.path.relpath(fp, ".")
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            module_doc = ast.get_docstring(tree) or "*No module-level description provided.*"
            
            doc_sections.append(f"### 📄 `{rel_path}`")
            doc_sections.append(f"{module_doc.strip()}\n")
            
            # Find classes and functions
            funcs = []
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    funcs.append(f"`{node.name}()`")
                elif isinstance(node, ast.ClassDef):
                    classes.append(f"`{node.name}`")
                    
            if classes:
                doc_sections.append(f"- **Classes defined**: {', '.join(classes)}")
            if funcs:
                doc_sections.append(f"- **Key functions/handlers**: {', '.join(funcs)}")
            doc_sections.append("")
        except:
            continue
            
    doc_sections.append("## 🚀 Quick Execution Guide")
    doc_sections.append("To start the advanced workshop stack:\n")
    doc_sections.append("1. **Start the Advanced Tool Server (Port 8001)**:\n   ```bash\n   python mcpserver_advanced.py\n   ```")
    doc_sections.append("2. **Launch the Resilient Parallel Chainlit UI (Port 8000)**:\n   ```bash\n   chainlit run main4_agent_chainlit.py\n   ```")
    
    readme_content = "\n".join(doc_sections)
    
    try:
        with open("README.md", "w", encoding="utf-8") as rf:
            rf.write(readme_content)
        return "📝 **README.md Successfully Generated & Saved!**\n\nReview of generated contents:\n\n" + readme_content[:1500] + "\n... [Remaining content written successfully] ..."
    except Exception as e:
        return f"❌ Failed to write README.md: {str(e)}"


if __name__ == "__main__":
    # Runs the server over HTTP on local interface
    print("🚀 Starting WorkspaceHarvester MCP Server on http://127.0.0.1:8001/mcp ...")
    mcp.run(transport="http", host="127.0.0.1", port=8001)
