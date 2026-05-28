import subprocess, time, select, re, os

# 1. Check if cloudflared is already running persistently
tunnel_file = "tunnel_url.txt"
is_running = False
try:
    pgrep_proc = subprocess.run(["pgrep", "-f", "cloudflared tunnel"], capture_output=True, text=True)
    if pgrep_proc.stdout.strip():
        is_running = True
except Exception:
    pass

if is_running and os.path.exists(tunnel_file):
    with open(tunnel_file, "r") as f:
        cf_url = f.read().strip()
    print("=======================================================")
    print(f"🎉 TUNNEL IS ALREADY ACTIVE! Reuse your existing link:\n🔗 {cf_url}")
    print("=======================================================")
else:
    # Clean up any potential dead/zombie processes first
    subprocess.run(["pkill", "-f", "cloudflared"], capture_output=True)
    time.sleep(1)

    print("🚀 Starting Global Cloudflare Tunnel on Port 8000 in a detached session...")
    # Use os.setsid to completely detach the process group so stopping other cells won't kill the tunnel!
    cf_proc = subprocess.Popen(
        ["./cloudflared", "tunnel", "--url", "http://127.0.0.1:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        preexec_fn=os.setsid
    )

    # Parse URL non-blockingly
    cf_url = "Connecting..."
    start_cf = time.time()
    while time.time() - start_cf < 15:
        rlist, _, _ = select.select([cf_proc.stdout], [], [], 0.1)
        if rlist:
            line = cf_proc.stdout.readline()
            if line:
                match = re.search(r"https://[a-zA-Z0-9-]+.trycloudflare.com", line)
                if match:
                    cf_url = match.group(0)
                    break
        else:
            time.sleep(0.1)

    if "trycloudflare.com" in cf_url:
        with open(tunnel_file, "w") as f:
            f.write(cf_url)

        print("⏳ Waiting 5 seconds for global DNS propagation...")
        time.sleep(5)

        print("\n=======================================================")
        print(f"🎉 SUCCESS! Click the link below to keep it open in your browser:\n🔗 {cf_url}")
        print("=======================================================")
    else:
        print("❌ Failed to parse Cloudflare Tunnel URL. Please re-run this cell.")
