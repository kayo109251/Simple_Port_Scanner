import socket
import threading
import argparse

# Function to scan a single port
def scan_port(target, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    banner = s.recv(1024).decode().strip()
                except:
                    banner = "Unknown service"
                print(f"[+] Port {port} is OPEN - {banner}")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Function to scan a range of ports using threads
def scan_range(target, start_port, end_port, threads, timeout):
    print(f"\nScanning {target} from port {start_port} to {end_port} using {threads} threads...\n")
    
    thread_list = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port, timeout))
        t.start()
        thread_list.append(t)

        # Ensure we don't exceed the max thread limit
        if len(thread_list) >= threads:
            for thread in thread_list:
                thread.join()  # Wait for all threads to complete
            thread_list.clear()  # Clear completed threads

    # Ensure all remaining threads finish
    for thread in thread_list:
        thread.join()

# Main function to handle arguments
def main():
    parser = argparse.ArgumentParser(description="Advanced Multi-threaded Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-sp", "--start_port", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-ep", "--end_port", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads (default: 50)")
    parser.add_argument("-to", "--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1s)")
    
    args = parser.parse_args()
    scan_range(args.target, args.start_port, args.end_port, args.threads, args.timeout)

if __name__ == "__main__":
    main()
