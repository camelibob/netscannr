import argparse
import sys

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

    #Number of threads ?

    args = parser.parse_args()

    #Basic validation to ensure logical port ranges
    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        print("Error: Invalid port range specified.")
        sys.exit(1)

    return args

if __name__ == "__main__":
    #Test argument parsing
    args = parse_arguments()

    print("--- Scanner Configuration ---")
    print(f"Target:       {args.target}")
    print(f"Port Range:   {args.start_port} to {args.end_port}")
    #print(f"Threads:      {args.threads}")
    print("-----------------------------")
    print("Ready to implement scanning logic.")