import os
from dotenv import load_dotenv
from netmiko import ConnectHandler

load_dotenv()
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")

routers = [
    {"hostname": "RTR-CORE-HUARAZ",  "ip": "192.168.1.1", "sede": "Huaraz-Core", "oct": 1},
    {"hostname": "RTR-SUC-CARAZ",    "ip": "192.168.1.2", "sede": "Caraz",       "oct": 2},
    {"hostname": "RTR-SUC-CARHUAZ",  "ip": "192.168.1.3", "sede": "Carhuaz",     "oct": 3},
    {"hostname": "RTR-SUC-YUNGAY",   "ip": "192.168.1.4", "sede": "Yungay",      "oct": 4},
    {"hostname": "RTR-SUC-CHIMBOTE", "ip": "192.168.1.5", "sede": "Chimbote",    "oct": 5},
]

for r in routers:
    print(f"[*] Aprovisionando {r['hostname']} ({r['ip']})...")
    dev = {
        "device_type": "cisco_ios",
        "host": r["ip"],
        "username": SSH_USER,
        "password": SSH_PASS,
        "secret": SSH_PASS,
        "conn_timeout": 30, "global_delay_factor": 2,
    }
    o = r["oct"]
    comandos = [
        "interface Loopback10",
        f"description Gestion_{r['sede']}",
        f"ip address 10.{o}.10.1 255.255.255.255",
        "no shutdown",
        "interface Loopback20",
        f"description Clientes_{r['sede']}",
        f"ip address 10.{o}.20.1 255.255.255.255",
        "no shutdown",
        "interface Loopback30",
        f"description Servicios_{r['sede']}",
        f"ip address 10.{o}.30.1 255.255.255.255",
        "no shutdown",
        "router ospf 1",
        f"router-id {o}.{o}.{o}.{o}",
        "network 192.168.1.0 0.0.0.255 area 0",
        f"network 10.{o}.10.1 0.0.0.0 area 0",
        f"network 10.{o}.20.1 0.0.0.0 area 0",
        f"network 10.{o}.30.1 0.0.0.0 area 0",
    ]
    conn = ConnectHandler(**dev)
    conn.enable()
    conn.send_config_set(comandos)
    conn.save_config()
    conn.disconnect()
    print(f"[OK] {r['hostname']} aprovisionado con Loopbacks y OSPF.")
