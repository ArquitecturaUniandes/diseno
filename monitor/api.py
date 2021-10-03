#!/usr/bin/env python3
import logging
import asyncio
import itertools as it
import os
from pathlib import Path
import csv
import random
import time
import traceback
import requests
from base import Servicio


logger = logging.getLogger(__file__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODIGO_FALLA_CONEXION = 550
CODIGO_FALLA_INESPERADA = 999


def archivo_log_monitoreo(servicio: Servicio) -> str:
    log_dir = os.path.join(BASE_DIR, "logs")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    return os.path.join(log_dir, f"{servicio.name}.csv")


async def escribe_log_monitoreo(servicio: Servicio, tiempo_inicio_monitoreo: float, codigo_de_respuesta: int) -> None:
    nombre_archivo_log = archivo_log_monitoreo(servicio)
    print(nombre_archivo_log)
    # hacer algo con el mensaje de salud??
    with open(nombre_archivo_log, 'a+') as f:
        writer = csv.writer(f)
        elapsed = time.perf_counter() - tiempo_inicio_monitoreo
        writer.writerow([elapsed, codigo_de_respuesta])


async def verificar_salud_microservicios() -> None:
    # get data from DB
    servicios = Servicio.query.all()
    for servicio in servicios:
        response = None
        tiempo_inicio_monitoreo = time.perf_counter()
        try:
            response = requests.get(f"https://{servicio.name}:5000/{servicio.health_check_uri}", verify=False)
            if response.status_code == 200:
                print("\033[36m" + f"Monitor verifico la salud de {servicio.name} con status_code {response.status_code}, Estado Correcto!")
                await escribe_log_monitoreo(servicio, tiempo_inicio_monitoreo, response.status_code)
            else:
                print("\033[36m" + f"Monitor verifico la salud de {servicio.name} con status_code {response.status_code}, Estado con fallas!")
                await escribe_log_monitoreo(servicio, tiempo_inicio_monitoreo, response.status_code)

        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:

            if response:
                print("\033[36m" + f"Monitor verifico la salud de {servicio.name} con status_code {response.status_code}, Estado con fallas!")
                await escribe_log_monitoreo(servicio, tiempo_inicio_monitoreo, response.status_code)
            else:
                print(str(err))
                await escribe_log_monitoreo(servicio, tiempo_inicio_monitoreo, CODIGO_FALLA_CONEXION)
        except Exception:
            traceback.print_exc()
            print("\033[91m" + f"Monitor no pudo verificar correctamente la salud de {servicio.name}, es probable que el microservicio tenga fallas")
            await escribe_log_monitoreo(servicio, tiempo_inicio_monitoreo, CODIGO_FALLA_INESPERADA)


async def domir_sengundos_aleatorios(caller=None) -> None:
    i = 5
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def crear_instancia_de_monitor(name: int) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        while True:
            await domir_sengundos_aleatorios(caller=f"Monitor {name}")
            tiempo_inicio_monitoreo = time.perf_counter()
            await verificar_salud_microservicios()
            elapsed = time.perf_counter() - tiempo_inicio_monitoreo
            print(f"Monitoreo fue completado en {elapsed:0.5f} segundos.")
        

async def main(numero_instancias: int):
    instancias_de_monitor = [asyncio.create_task(crear_instancia_de_monitor(n)) for n in range(numero_instancias)]
    await asyncio.gather(*instancias_de_monitor)


if __name__ == "__main__":
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--numero_instancias", type=int, default=1)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
