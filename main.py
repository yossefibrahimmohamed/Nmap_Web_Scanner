import re
from flask import Flask, request, render_template, jsonify, send_file
import subprocess
import socket
import tempfile
import threading
import time
import os

app = Flask(__name__)  # ← هنا التغيير

def is_valid_target(target):
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    hostname_pattern = r'^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$'
    return bool(re.match(ip_pattern, target) or re.match(hostname_pattern, target))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form.get("target")
    if not is_valid_target(target):
        return jsonify({"error": "Invalid target"}), 400
    try:
        ip_target = socket.gethostbyname(target)
        # الأمر المبسط ليشتغل بدون صلاحيات root
        result = subprocess.check_output(
            ["nmap", "-Pn", "-p", "1-1000", target],
            stderr=subprocess.STDOUT,
            text=True
        )
        scan_file = os.path.join(tempfile.gettempdir(), f"scan_result_{target}.txt")
        with open(scan_file, "w", encoding="utf-8") as f:
            f.write(result)
        ip_found = None
        for line in result.splitlines():
            if 'Nmap scan report for' in line:
                parts = line.split()
                if len(parts) >= 5:
                    ip_found = parts[-1]
                    break
        if ip_found:
            ip_target = ip_found
    except subprocess.CalledProcessError as e:
        result = e.output if e.output else "Error running nmap."

    return render_template("result_real.html", target=target, ip_target=ip_target, result=result)
    
@app.route('/download/<target>')
def download_report(target):
    scan_file = os.path.join(tempfile.gettempdir(), f"scan_result_{target}.txt")
    if os.path.exists(scan_file):
        return send_file(scan_file, as_attachment=True)
    else:
        return "Scan result file not found.", 404

def keep_alive():
    while True:
        try:
            # هنا تستدعي رابط السيرفر (localhost مع المنفذ الموجود)
            port = int(os.environ.get("PORT", 5000))
            url = f"http://localhost:{port}/"
            requests.get(url)
            print("Ping sent to self to keep alive.")
        except Exception as e:
            print(f"Error in keep_alive ping: {e}")
        time.sleep(60)  # انتظر 4 دقائق قبل المرة القادمة

if __name__ == "__main__":
    t = threading.Thread(target=keep_alive)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

