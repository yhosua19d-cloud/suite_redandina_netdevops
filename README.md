# Suite NetDevOps - Red-Andina Telecom (Áncash)

## Topología e Inventario
- **RTR-CORE-HUARAZ**: `192.168.1.1` (Loopbacks: `10.1.10.1`, `10.1.20.1`, `10.1.30.1`)
- **RTR-SUC-CARAZ**: `192.168.1.2` (Loopbacks: `10.2.10.1`, `10.2.20.1`, `10.2.30.1`)
- **RTR-SUC-CARHUAZ**: `192.168.1.3` (Loopbacks: `10.3.10.1`, `10.3.20.1`, `10.3.30.1`)
- **RTR-SUC-YUNGAY**: `192.168.1.4` (Loopbacks: `10.4.10.1`, `10.4.20.1`, `10.4.30.1`)
- **RTR-SUC-CHIMBOTE**: `192.168.1.5` (Loopbacks: `10.5.10.1`, `10.5.20.1`, `10.5.30.1`)
- **Nodo-Automatizacion**: `192.168.1.100`

## Ejecución
1. Copiar `.env.example` a `.env` y completar credenciales.
2. `python3 scripts/01_aprovisionar_red.py`
3. `python3 scripts/02_backup_masivo.py`
4. `python3 scripts/03_vigilante_triggers.py`
5. `python3 scripts/04_etl_inventario.py`
6. `python3 scripts/05_enviar_reporte_api.py`
