# 👹 PortScanner - Ultra Fast Async Network Engine

A high-performance network reconnaissance and service identification tool built with a modern **Python `asyncio` architecture** and a **`FastAPI` WebSocket backend**. 

Unlike traditional multi-threaded or sequential scanners, this engine handles thousands of concurrent socket connections flawlessly, streaming discovered ports and deep banner intelligence directly to a sleek, real-time web dashboard.

---

## ⚠️ LEGAL DISCLAIMER & TERMS OF USE

**Please read this section carefully before deploying or utilizing the software:**

1. **Educational & Authorized Testing Only:** This tool is strictly developed for educational purposes, academic research, and authorized security auditing (Penetration Testing / Ethical Hacking) by network administrators or security professionals on systems they own or have explicit written permission to test.
2. **User Responsibility:** Unauthorized scanning of third-party networks, hosts, or infrastructure without explicit prior consent is **ILLEGAL** and constitutes a cybercrime in most jurisdictions.
3. **No Developer Liability:** The developer (author) assumes absolutely no liability and is not responsible for any misuse, malicious exploitation, legal consequences, data loss, or infrastructure damage caused by this software. All risks and liabilities remain entirely with the end-user.
4. **Compliance:** By running this software, you agree to comply with your local computer misuse acts, cyber security regulations, and international tech laws.

---

## 🛠️ Installation & Execution

Setting up and launching the control panel is straightforward:

1. **Install Dependencies:** Open your terminal, navigate to the project directory, and run:
   ```bash
   pip install -r requirements.txt
Launch the Engine: Start the application server by executing:

Bash
python main.py
Access the Web UI: Open your preferred browser (Chrome, Edge, Firefox, etc.) and navigate to:

Plaintext
[http://127.0.0.1:8000](http://127.0.0.1:8000)
Input your target host, configure your parameters, and hit the ROKETLE! button to begin.

⚙️ Tactical Parameters (Mechanics & Impacts)
Adjusting the sidebar configuration alters the socket layer behavior. Understanding these thresholds is critical for successful discovery:

1. Speed (Rate Limit / Concurrency)
Determines how many distinct ports the engine attempts to probe simultaneously within the exact same millisecond.

🚀 Increasing the value (e.g., 1000+): Triggers hyper-speed scanning, tearing through thousands of ports in seconds. The Catch: When probing external WAN targets, aggressive concurrency patterns look exactly like a DDoS attack. Downstream Firewalls, IDS, or IPS devices will instantly flag and block your IP, resulting in false negatives (all remaining ports showing up as closed).

🐢 Decreasing the value (e.g., 50 - 100): Slows down the process significantly but keeps the traffic stealthy and highly stable, quietly passing under firewall thresholds.

2. Timeout (Seconds)
Specifies the maximum duration the engine will wait for a response packet from a requested socket before abandoning it.

🚀 Increasing the value (e.g., 1.5 - 2.0): Mandatory when scanning remote internet targets across wide networks. Since network packets experience physical latency (Ping), a loose timeout ensures slow or heavily loaded remote daemons are not accidentally skipped. The Trade-off: Closed ports will force the script to wait out the entire timeout duration, increasing total scan times.

🐢 Decreasing the value (e.g., 0.2 - 0.3): Highly optimized for Localhost (127.0.0.1) discovery. Because packets never leave your machine's network stack, responses are instantaneous. The Catch: Setting this too low on an external network will cause the engine to falsely report open ports as closed because the response packets didn't make it back in time.

📊 Optimal Configuration Matrix
Local Scans (Self-Testing / Localhost):

Concurrency (Speed): 1000 | Timeout: 0.2 - 0.3 (Instantaneous, maximum speed)

Remote WAN Scans (Internet / Domains):

Concurrency (Speed): 50 - 100 | Timeout: 1.2 - 1.5 (Firewall evasion, reliable fingerprinting)

📂 Project Architecture & Modules
main.py: Core controller orchestrating the FastAPI application, static template rendering, and full-duplex WebSocket communication streams.

scanner/core.py: The low-level asynchronous processing engine managing worker pools, rate-limit semaphores, and socket tasks.

scanner/grabber.py: Active Layer-7 protocol scanner. Interacts with open ports (sending precise HTTP probes, catching raw banners) to extract server versioning data (e.g., uvicorn, OpenSSH).

scanner/utils.py: Text parser converting mixed user inputs (ranges like 1-1000, commas like 80,443) into neat iterable arrays.

templates/index.html: Dark-themed responsive dashboard styled with TailwindCSS, displaying real-time responsive progress bars and real-time log injections.
