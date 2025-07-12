# Nmap Web Scanner - Flask-based

A simple web application built with **Flask** that allows users to perform basic **Nmap scans** on domains or IP addresses and view the results via a web interface.

---

## Features

- Input domain or IP address to scan.
- Runs Nmap scan on common ports (1-1000) without requiring root privileges.
- Displays scan results with open ports, services, OS info (basic), HTTP response codes, and traceroute.
- Save scan report as a downloadable text file.
- Lightweight and easy to deploy on platforms like Replit or any VPS.

---

## Demo

![Screenshot]![Screenshot 2025-07-12 060955](https://github.com/user-attachments/assets/6cfac141-5ded-45c9-888c-4b2166754b86)
![Screenshot 2025-07-12 060930](https://github.com/user-attachments/assets/2d97de9e-7f56-4b2c-affb-508a7858ccc7)
![Screenshot 2025-07-12 060900](https://github.com/user-attachments/assets/c24a50c6-2fb5-466b-a7ae-057a5aad4dc5)


Try live demo on [Link](https://c01378ea-e2ef-49fc-a5ea-189adcdf11a0-00-21gdtq58c01lg.riker.replit.dev/)

---

## Installation & Setup

### Prerequisites

- Python 3.x
- Nmap installed on your system (scan tool)
- Pip packages: Flask

### Install Dependencies

```bash
pip install flask
```

Install Nmap (Linux)

```bash
sudo apt update
sudo apt install nmap
```

    Note: If running on Replit or restricted environments, use simplified Nmap scan options (no root required).

Usage

    Clone the repository:
```
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

    Run the Flask app:
```
python main.py
```
    Open your browser and go to:
```
http://localhost:5000/
```

Enter domain or IP and hit Scan.

Project Structure

```
/project_root
│
├── main.py          # Flask application
├── templates/
│   ├── index.html   # Home page with scan form
│   └── result_real.html  # Scan result page
├── static/
│   ├── css/
│   └── js/
├── requirements.txt # Python dependencies
└── README.md        # This file
```
