import os
import time
from datetime import datetime
from dotenv import load_dotenv
from netmiko import ConnectHandler, NetmikoTimeoutException

load_dotenv()
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")

routers = [
    {"hostname": "RTR-CORE-HUARAZ",  "ip": "192.168.1.1"},
    {"hostname": "RTR-SUC-CARAZ",    "ip": "192.168.1.2"},
    {"hostname": "RTR-SUC-CARHUAZ",  "ip": "192.168.1.3"},
    {"hostname": "RTR-SUC-YUNGAY",   "ip": "192.168.1.4"},
    {"hostname": "RTR-SUC-CHIMBOTE", "ip": "192.168.1.5"},
]

os.makedirs("logs", exist_ok=True)

def registrar_log(mensaje):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ts}] {mensaje}"
    print(linea)
    with open("logs/auditoria_noc.log", "a") as f:
        f.write(linea + "\n")

for ronda in range(1, 4):
    print(f"\n--- RONDA DE VIGILANCIA {ronda}/3 ---")
    for r in routers:
        dev = {
            "device_type": "cisco_ios",
            "host": r["ip"],
            "username": SSH_USER,
            "password": SSH_PASS,
            "secret": SSH_PASS,
            "conn_timeout": 15,
            "global_delay_factor": 2,
        }
        try:
            conn = ConnectHandler(**dev)
            conn.enable()

            # Trigger 1: Autoreparacion de interfaces
            salida_if = conn.send_command("show ip interface brief")
            for linea in salida_if.splitlines():
                if any(iface in linea for iface in ["FastEthernet0/0", "Loopback10", "Loopback20", "Loopback30"]):
                    if "down" in linea.lower():
                        interfaz = linea.split()[0]
                        conn.send_config_set([f"interface {interfaz}", "no shutdown"])
                        registrar_log(f"TRIGGER-1 REPARACION: {interfaz} levantada en {r['hostname']}")

            # Trigger 2: Vecindad OSPF en Core
            if r["hostname"] == "RTR-CORE-HUARAZ":
                vecinos_raw = conn.send_command("show ip ospf neighbor")
                vecinos = [l for l in vecinos_raw.splitlines() if "FULL" in l]
                if len(vecinos) < 4:
                    registrar_log(f"TRIGGER-2 ALERTA CRITICA OSPF: Solo {len(vecinos)}/4 vecinos activos en {r['hostname']}")

            conn.disconnect()
        except (NetmikoTimeoutException, Exception) as e:
            registrar_log(f"EXCEPCION CAIDA: Router {r['hostname']} ({r['ip']}) inalcanzable -> {type(e).__name__}")

    if ronda < 3:
        time.sleep(15)
