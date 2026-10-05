import argparse
import sys
import socket
import concurrent.futures
import json
from datetime import datetime
from pathlib import Path

def parse_arguments():
    """
    Parses command-line arguments for the network scanner.
    """
    parser = argparse.ArgumentParser(
        description="A lightweight TCP network scanner.",
        epilog="Example usage: python3 scanner.py <ip> ..."
    )

    #Target IP (Defaults to localhost for safety)
    parser.add_argument(
        "target",
        nargs="?",
        default="127.0.0.1",
        help="Target IP address to scan (default: 127.0.0.1)"
    )

    #Flag : Start port
    parser.add_argument(
        "-s", "--start-port",
        type=int,
        default=1,
        help="Port to start scanning from (default: 1)"
    )

    #Flag : End port
    parser.add_argument(
        "-e", "--end-port",
        type=int,
        default=1024,
        help="Port to end scanning at (default: 1024)"
    )

    #Number of threads flag
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=4,
        help="Number of concurrent threads to use (default: 4)"
    )

    args = parser.parse_args()

    #Basic validation to ensure logical port ranges
    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        print("Error: Invalid port range specified.")
        sys.exit(1)

    return args

def scan_port(ip, port):
    """
    Attemps a full TCP connection to a specific port on the target IP.
    Returns a tuple: (is_open (bool), banner(str)).
    """
    #create an IPv4 and TCP socket
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #1sec timeout to prevent the script from hanging
            sock.settimeout(1.0)

            #connect_ex returns 0 upon successful connection
            result = sock.connect_ex((ip, port))

            if result == 0:
                banner = ""
                try:
                    #Port is open. Extend timeout slightly to wait for a banner.
                    sock.settimeout(1.5)

                    #Send a generic request to provoke a response from services (like HTTP)
                    #that wait for the client to speak first.
                    sock.sendall(b"HEAD / HTTP/1.0\n\r\n")

                    data = sock.recv(1024)
                    if data:
                        #Decode, ignore weird characters and grab the first line to keep terminal clean
                        banner = data.decode("utf-8", errors="ignore").splitlines()[0].strip()
                except socket.timeout:
                    banner = "No banner, only hulk (Timeout)"
                except Exception:
                    banner = "No banner, only hulk (Connection Reset/Error)"
                return True, banner
            return False, ""
    except Exception:
        print("An error occured, try again.")
        return False, ""

def worker_thread(target, port):
    """
    Worker function to be executed by the thread pool.
    Prints output immediately when an open port is found.
    """
    is_open, banner = scan_port(target, port)

    
    if is_open:
        #Format output for CLI
        display_banner = f" [{banner}]" if banner else ""
        print(f"[+] Port {port:<5} is OPEN{display_banner}")

        #return a tuple so the main thread can populate the dictionnary
        return port, banner        
    return None


if __name__ == "__main__":
    #Test argument parsing
    args = parse_arguments()

    print(f"[*] Starting multithreaded scan on {args.target}")
    print(f"[*] Port range: {args.start_port} to {args.end_port}")
    print(f"[*] Threads: {args.threads}\n")
    
    scan_results = {}
    
    #ThreadPoolExecutor for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Map the worker_thread function to every port in the range
        # We use list comprehension to pass the target IP along with each port
        futures = {
            executor.submit(worker_thread, args.target, port): port 
            for port in range(args.start_port, args.end_port + 1)
        }
        
        # as_completed yields futures as they finish, regardless of submission order
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                port_num, banner_text = result
                scan_results[port_num] = banner_text
            
    # Sort the ports for clean output, since threads return in random order
    print(f"\n[*] Scan complete. Found {len(scan_results)} open ports.")

#JSON export
if scan_results:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_ip = args.target.replace(".", "_")
    filename = f"scan_{safe_ip}_{timestamp}.json"

    log_dir = Path("logs")

    log_dir.mkdir(parents=True, exist_ok=True)
    filepath = log_dir / filename
    export_data = {
        "target": args.target,
        "scan_date": datetime.now().isoformat(),
        "total_open_ports": len(scan_results),
        "open_ports": scan_results
    }

    #write to file
    with open(filepath, "w") as f:
        json.dump(export_data, f, indent=4)

    print(f"\n[*] Results exported to a JSON file : {filepath.absolute()}")



    