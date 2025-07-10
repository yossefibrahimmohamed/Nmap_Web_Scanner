import re
from flask import Flask, request, render_template, jsonify, send_file
import subprocess
import socket
import tempfile
import os

main = Flask(__name__)

def is_valid_target(target):
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    hostname_pattern = r'^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$'
    return bool(re.match(ip_pattern, target) or re.match(hostname_pattern, target))

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/scan", methods=["POST"])
def scan():
    target = request.form.get("target")
    if not is_valid_target(target):
        return jsonify({"error": "Invalid target"}), 400  # Return JSON error for front-end
    try:
        ip_target = socket.gethostbyname(target)
        # Run nmap and get output as string
        result = subprocess.check_output(
            ["nmap", "-sS", "-sV", "-O", "-A", target],
            stderr=subprocess.STDOUT,
            text=True  # Directly get str, no need to decode
        )
        # Save to file (result is already string)
        scan_file = os.path.join(tempfile.gettempdir(), f"scan_result_{target}.txt")
        with open(scan_file, "w", encoding="utf-8") as f:
            f.write(result)
        # Extract IP from nmap output, fallback to socket IP if not found
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
        result = e.output.decode() if e.output else "Error running nmap."

    return render_template("result_real.html", target=target, ip_target=ip_target, result=result)
@main.route('/download/<target>')

def download_report(target):
    scan_file = os.path.join(tempfile.gettempdir(), f"scan_result_{target}.txt")
    if os.path.exists(scan_file):
        return send_file(scan_file, as_attachment=True)
    else:
        return "Scan result file not found.", 404

if __name__ == "__main__":
    main.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
