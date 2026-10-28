## **netscannr**

A lightweight, multithreaded TCP network scanner written in pure Python.

**netscannr** is designed to operate in restricted user environments where root/administrator privileges are not available. By relying on standard OS-level TCP Connect scans (full 3-way handshake) rather than raw sockets, it provides concurrent port scanning and banner grabbing without the need for external dependencies like Nmap or Scapy.

### **Features**

- No Root Required: Safely executes full TCP Connect scans in unprivileged environments.
- Zero External Dependencies: Built entirely using Python's standard library (socket, argparse, concurrent.futures).
- Service Identification: Includes built-in banner grabbing with HTTP-compliant probes to identify running services.
- Automated Logging: Automatically sorts results and exports them to timestamped JSON files in a dedicated logs/ directory which are suitable for further processing.

#### **Project Structure**
```
netscannr/
├── src/
│   └── scanner.py      # Main scanner script
├── logs/               # Auto-generated directory for JSON scan
└── README.md
```

### **Usage**

netscannr is run directly from the command line. If no arguments are provided, it safely defaults to scanning ports 1-1024 on 127.0.0.1 using 4 concurrent threads.

### **Syntax**

`python3 src/scanner.py [target] [-s START_PORT] [-e END_PORT] [-t THREADS]`


### **Arguments**

`target :` Target IP address to scan (Default: 127.0.0.1)

`-s, --start-port :` Port to start scanning from (Default: 1)

`-e, --end-port :` Port to end scanning at (Default: 1024)

`-t, --threads :` Number of concurrent threads to use (Default: 4)

### **Examples**

1. Basic Local Scan:

`python3 src/scanner.py`


2. Targeted Service Scan:
Scan common web and SSH ports on a specific IP using 20 threads.

`python3 src/scanner.py 192.0.2.10 -s 20 -e 100 -t 20`


3. Full Port Scan:
Scan all 65,535 ports on a single host. (Note: Adjust thread count based on your host OS and network capabilities).

`python3 src/scanner.py 192.0.2.10 -s 1 -e 65535 -t 100`


### **Output (JSON Export)**

Upon completion, netscannr displays a summary in the terminal and generates a JSON artifact in the logs/ directory.

Example output (illustrative; `192.0.2.10` is a documentation address reserved by RFC 5737):

```json
{
    "target": "192.0.2.10",
    "scan_date": "2026-10-12T11:42:17.384912",
    "total_open_ports": 2,
    "open_ports": {
        "22": "SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13",
        "80": "HTTP/1.1 301 Moved Permanently"
    }
}
```

### Limitations

- TCP only (no UDP scanning).
- TCP Connect scans complete the full handshake, so they are logged by target hosts and easily detected by IDS; this tool is not designed for stealth.
- Banner grabbing is basic: services that do not send a banner or respond to the HTTP probe are reported without identification.

## **Disclaimer**

This tool is intended for educational purposes and authorized auditing only. Do not use this tool to scan networks, servers, or devices that you do not own or do not have explicit, written permission to test. The author is not responsible for any misuse or damage caused by this program.
