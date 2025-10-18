from bcc import BPF
import ctypes
from time import sleep
import sys

# eBPF program with configurable port in a BPF map
prog = """
#include <uapi/linux/bpf.h>
#include <linux/tcp.h>
#include <linux/ip.h>

BPF_ARRAY(port_map, u16, 1);

int drop_tcp_port(struct __sk_buff *skb) {
    u8 ip_proto = 0;
    u16 zero = 0;
    u16 *port;

    bpf_skb_load_bytes(skb, offsetof(struct iphdr, protocol), &ip_proto, 1);
    if (ip_proto != IPPROTO_TCP)
        return BPF_OK;

    port = port_map.lookup(&zero);
    if (!port)
        return BPF_OK;

    u16 dest_port = 0;
    bpf_skb_load_bytes(skb, offsetof(struct tcphdr, dest), &dest_port, 2);

    if (dest_port == htons(*port))
        return BPF_DROP;

    return BPF_OK;
}
"""

def main():
    # Default port
    default_port = 4040

    # Get port from command line argument if provided
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not (1 <= port <= 65535):
                print("Port must be between 1 and 65535. Using default 4040.")
                port = default_port
        except ValueError:
            print("Invalid port argument. Using default 4040.")
            port = default_port
    else:
        port = default_port

    b = BPF(text=prog)
    fn = b.load_func("drop_tcp_port", BPF.SOCKET_FILTER)
    b.attach_raw_socket(fn, "eth0")  # Change interface if needed

    port_map = b.get_table("port_map")
    key = ctypes.c_int(0)
    port_map[key] = ctypes.c_ushort(port)

    print(f"Dropping TCP packets on port {port}. Press Ctrl+C to stop.")

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
