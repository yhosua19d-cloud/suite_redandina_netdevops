import json
import xml.etree.ElementTree as ET

tree = ET.parse("datos/inventario_regional.xml")
root = tree.getroot()

equipos = []
for nodo in root.findall("router"):
    total_lo = int(nodo.find("total_loopbacks").text)
    if total_lo != 3:
        raise ValueError(f"Error en {nodo.find('hostname').text}: se esperaban 3 loopbacks")
    equipos.append({
        "hostname": nodo.find("hostname").text,
        "ip_gestion": nodo.find("ip_gestion").text,
        "sede": nodo.find("sede").text,
        "modelo": nodo.find("modelo").text,
        "total_loopbacks": total_lo,
    })

resultado = {"empresa": "Red-Andina Telecom", "total_equipos": len(equipos), "routers": equipos}
with open("datos/inventario_regional.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("[OK] datos/inventario_regional.json generado y validado.")
