import argparse
import sys
import socket
import concurrent.futures

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
    Returns True if the port is open, False otherwise.
    """
    #create an IPv4 and TCP socket
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #1sec timeout to prevent the script from hanging
            sock.settimeout(1.0)

            #connect_ex returns 0 upon successful connection
            result = sock.connect_ex((ip, port))

            if result == 0:
                return True
            return False
    except Exception:
        print("An error occured during the port scan.")
        return False

def worker_thread(target, port):
    """
    Worker function to be executed by the thread pool.
    Prints output immediately when an open port is found.
    """
    open_port = scan_port(target, port)
    if open_port:
        print(f"[+] Port {port} is OPEN.")
        return port
    return None


if __name__ == "__main__":
    #Test argument parsing
    args = parse_arguments()

    print(f"[*] Starting multithreaded scan on {args.target}")
    print(f"[*] Port range: {args.start_port} to {args.end_port}")
    print(f"[*] Threads: {args.threads}\n")
    
    open_ports = []
    
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
                open_ports.append(result)
            
    # Sort the ports for clean output, since threads return in random order
    open_ports.sort()
    print(f"\n[*] Scan complete. Found {len(open_ports)} open ports: {open_ports}")