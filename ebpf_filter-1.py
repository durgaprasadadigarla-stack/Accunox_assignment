import sys
import time
import psutil
from bcc import BPF

def get_pid_by_name(name):
    """Find PID by process name"""
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        if proc.info["name"] == name:
            return proc.info["pid"]
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python3 filter_process_port.py <process_name> [port]")
        sys.exit(1)

    process_name = sys.argv[1]
    port = 4040  # Default port
    if len(sys.argv) == 3:
        port = int(sys.argv[2])

    # Get the process PID
    pid = get_pid_by_name(process_name)
    if not pid:
        print(f"❌ Process '{process_name}' not found.")
        sys.exit(1)

    print(f"✅ Found process '{process_name}' (PID={pid}). Allowing only TCP port {port}.")

    # Load eBPF program
    b = BPF(text=prog)
    fn = b.load_func("filter", BPF.SOCKET_FILTER)
    b.attach_raw_socket(fn, "eth0")  # Change to your interface if needed (use 'ip link show')

    # Store the target PID in the map
    pid_key = b["target_pid"].Key(pid)
    pid_val = b["target_pid"].Leaf(1)
    b["target_pid"][pid_key] = pid_val

    print("\n🚀 eBPF socket filter loaded.")
    print(f"Only TCP port {port} traffic will be allowed for '{process_name}'.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Exiting and cleaning up...")
        b.remove_xdp("eth0", 0)


if __name__ == "__main__":
    main()