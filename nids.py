from scapy.all import sniff

print("🚀 Starting Real-Time Network Monitoring...\n")

ip_count = {}

def process_packet(pkt):
    if pkt.haslayer("IP"):
        ip = pkt["IP"].src

        ip_count[ip] = ip_count.get(ip, 0) + 1

        # Detection logic
        if ip_count[ip] > 20:
            print(f"⚠️ Suspicious IP: {ip} | Packets: {ip_count[ip]}")
        else:
            print(f"Normal: {ip} | Packets: {ip_count[ip]}")

# Start sniffing packets
sniff(prn=process_packet, store=False)