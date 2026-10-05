## **netscannr**

A lightweight, multithreaded TCP network scanner written in pure Python.

NetScannr is designed to operate in restricted user environments where root/administrator privileges are not available. By relying on standard OS-level TCP Connect scans (full 3-way handshake) rather than raw sockets, it provides fast, concurrent port scanning and banner grabbing without the need for external dependencies like Nmap or Scapy.

#### **Features**

No Root Required: Safely executes full TCP Connect scans in unprivileged environments.

Zero External Dependencies: Built entirely using Python's standard library (socket, argparse, concurrent.futures).

High Concurrency: Utilizes ThreadPoolExecutor to scan thousands of ports in seconds.

Service Identification: Includes built-in banner grabbing with HTTP-compliant probes to identify running services.

Automated Logging: Automatically sorts results and exports them to timestamped JSON files in a dedicated log/ directory, making it perfect for CI/CD pipelines or dashboard integrations.

#### **Project Structure**

netscannr/
├── src/
│   └── scanner.py      # Main scanner script
├── log/                # Auto-generated directory for JSON scan
└── README.md


#### **Usage**

netscannr is run directly from the command line. If no arguments are provided, it safely defaults to scanning ports 1-1024 on 127.0.0.1 using 4 concurrent threads.

#### **Syntax**

`python3 src/scanner.py [target] [-s START_PORT] [-e END_PORT] [-t THREADS]`


#### **Arguments**

target : Target IP address to scan (Default: 127.0.0.1)

`-s, --start-port :` Port to start scanning from (Default: 1)

`-e, --end-port :` Port to end scanning at (Default: 1024)

`-t, --threads :` Number of concurrent threads to use (Default: 4)

#### **Examples**

1. Basic Local Scan:

`python3 src/scanner.py`


2. Targeted Service Scan (Fast):
Scan common web and SSH ports on a specific IP using 20 threads.

`python3 src/scanner.py 192.168.1.50 -s 20 -e 100 -t 20`


3. Comprehensive Network Scan:
Scan all 65,535 ports on a remote server with high concurrency. (Note: Adjust thread count based on your host OS and network capabilities).

`python3 src/scanner.py 100.124.149.109 -s 1 -e 65535 -t 100`


#### **Output (JSON Export)**

Upon completion, netscannr displays a summary in the terminal and generates a JSON artifact in the log/ directory.

Example output (log/scan_100_124_149_109_20261005_120500.json):
```json
{
    "target": "100.124.149.109",
    "scan_date": "2026-10-05T12:05:00.123456",
    "total_open_ports": 2,
    "open_ports": {
        "22": "SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u1",
        "80": "HTTP/1.0 302 Found"
    }
}
```

### **Disclaimer**

This tool is intended for educational purposes and authorized auditing only. Do not use this tool to scan networks, servers, or devices that you do not own or do not have explicit, written permission to test. The author is not responsible for any misuse or damage caused by this program.
