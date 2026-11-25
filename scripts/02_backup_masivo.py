import os
from datetime import datetime
from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")
ANIO = datetime.now().strftime("%Y")

routers = [
    {"hostname": "RTR-CORE-HUARAZ",  "ip": "192.168.1.1"},
    {"hostname": "RTR-SUC-CARAZ",    "ip": "192.168.1.2"},
    {"hostname": "RTR-SUC-CARHUAZ",  "ip": "192.168.1.3"},
    {"hostname": "RTR-SUC-YUNGAY",   "ip": "192.168.1.4"},
    {"hostname": "RTR-SUC-CHIMBOTE", "ip": "192.168.1.5"},
]

os.makedirs("backups", exist_ok=True)

for r in routers:
    print(f"[*] Respaldando {r['hostname']}...")
    dev = {
        "device_type": "cisco_ios",
        "host": r["ip"],
        "username": SSH_USER,
        "password": SSH_PASS,
        "secret": SSH_PASS,
        "conn_timeout": 15,
    }
    conn = ConnectHandler(**dev)
    conn.enable()
    running = conn.send_command("show running-config")
    rutas = conn.send_command("show ip route")
    conn.disconnect()

    with open(f"backups/running_{r['hostname']}_{ANIO}.txt", "w") as f:
        f.write(running)
    with open(f"backups/rutas_{r['hostname']}_{ANIO}.txt", "w") as f:
        f.write(rutas)
    print(f"[OK] Backups generados para {r['hostname']}.")
