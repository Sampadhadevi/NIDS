import tkinter as tk
from scapy.all import sniff
import threading
import winsound

# Window
root = tk.Tk()
root.title("Real-Time NIDS")
root.geometry("700x500")
root.configure(bg="black")

# Title
title = tk.Label(root, text="☠️ CYBER INTRUSION DETECTION SYSTEM ☠️",
                 fg="lime", bg="black", font=("Consolas", 14, "bold"))
title.pack(pady=10)

# Output box
output = tk.Text(root, height=25, width=80, bg="black", fg="lime",
                 insertbackground="lime", font=("Consolas", 10))
output.pack(pady=10)

# Highlight tag
output.tag_config("alert", foreground="red")

# Scrollbar
scroll = tk.Scrollbar(root, command=output.yview)
output.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

ip_count = {}
running = False  # control flag

def process_packet(pkt):
    global running

    if not running:
        return

    if pkt.haslayer("IP"):
        ip = pkt["IP"].src
        ip_count[ip] = ip_count.get(ip, 0) + 1

        if ip_count[ip] % 10 == 0:
            if ip_count[ip] > 20:
                msg = f"⚠️ Suspicious: {ip} ({ip_count[ip]})\n"
                output.insert(tk.END, msg, "alert")
                winsound.Beep(1000, 200)
            else:
                msg = f"Normal: {ip} ({ip_count[ip]})\n"
                output.insert(tk.END, msg)

            output.see(tk.END)

def sniff_packets():
    sniff(prn=process_packet, store=False, filter="ip")

def start_monitoring():
    global running
    running = True
    thread = threading.Thread(target=sniff_packets)
    thread.daemon = True
    thread.start()
    output.insert(tk.END, "\n[+] Monitoring Started...\n\n")

def stop_monitoring():
    global running
    running = False
    output.insert(tk.END, "\n[!] Monitoring Stopped.\n\n")

# Buttons
btn_frame = tk.Frame(root, bg="black")
btn_frame.pack(pady=5)

start_btn = tk.Button(btn_frame, text="Start", command=start_monitoring,
                      bg="black", fg="lime", font=("Consolas", 12))
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = tk.Button(btn_frame, text="Stop", command=stop_monitoring,
                     bg="black", fg="red", font=("Consolas", 12))
stop_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()