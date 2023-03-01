import simpy
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


class Proceso:
    def __init__(self, env, id, mem_req, instrucciones_totales):
        self.env = env
        self.id = id
        self.mem_req = mem_req
        self.instrucciones_totales = instrucciones_totales
        self.instrucciones_restantes = instrucciones_totales

        self.estado = 'new'
        self.memoria = None
        self.cpu = None

        self.eventos = {
            'new': env.event(),
            'ready': env.event(),
            'running': env.event(),
            'terminated': env.event(),
            'waiting': env.event()
        }


def llegada_proceso(env, memoria, cpu):
    global proceso_id
    while True:
        # Generar nuevo proceso
        instrucciones_totales = random.randint(1, 10)
        mem_req = random.randint(1, 10)
        proceso = Proceso(env, proceso_id, mem_req, instrucciones_totales)
        proceso_id += 1

        # Esperar por memoria RAM
        with memoria.get(proceso.mem_req) as req:
            yield req
            proceso.memoria = req.value
            proceso.estado = 'ready'
            proceso.eventos['ready'].succeed()

        # Añadir proceso a la cola de listos para correr
        with cpu.request() as req:
            yield req
            proceso.cpu = req
            proceso.estado = 'running'
            proceso.eventos['running'].succeed()
            # Ejecutar instrucciones
            instrucciones_ejecutadas = min(proceso.instrucciones_restantes, 3)
            proceso.instrucciones_restantes -= instrucciones_ejecutadas

            # Esperar un tiempo para la simulación del procesador
            yield env.timeout(1)

            # Verificar si se ha terminado el proceso
            if proceso.instrucciones_restantes == 0:
                proceso.estado = 'terminated'
                memoria.put(proceso.memoria)
                proceso.eventos['terminated'].succeed()
            else:
                # Si no ha terminado, se generará un número aleatorio para determinar el próximo estado
                random_num = random.randint(1, 21)
                if random_num == 1:
                    proceso.estado = 'waiting'
                    proceso.eventos['waiting'].succeed()
                else:
                    proceso.estado = 'ready'
                    proceso.eventos['ready'].succeed()


