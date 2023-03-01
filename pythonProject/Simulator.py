import random
import simpy

# Declaracion de variables
ramSize = 100  # Capacidad de la memoria RAM
numInstructions = 3  # Capacidad de instrucciones que se pueden ejecutar por ciclo

env = simpy.Environment()
memory = simpy.Container(env, ramSize, ramSize)
cpu = simpy.Resource(env, 1)


def process(env, memory, cpu):
    print(f"Ha iniciado un nuevo proceso en el segundo {env.now:.2f}")
    # Solicita memoria RAM
    req_size = random.randint(1, 10)  # Se genera el tamaño aleatorio de memoria que solicita el proceso
    with memory.request() as req:
        yield req
        print(f"El proceso ocupa {req_size} MB de memoria en el segundo {env.now:.2f}")

        # Una vez asignada la memoria, el proceso pasa a estado ready
        env.process(ready_process(env, req_size, cpu))


def ready_process(env, req_size, cpu):
    memory = req_size
    # El proceso tiene un contador con la cantidad de instrucciones totales a realizar
    instructions = random.randint(1, 10)
    print(f"El proceso está en la fase <ready> en el minuto {env.now:.2f} con {instructions} instrucciones restantes")
    while instructions > 0:
        # Espera para ser atendido por el CPU
        with cpu.request() as req:
            yield req
            #print(f"{name} starts running on CPU at {env.now:.2f}") tal vez despues la pongo
            # El CPU atiende al proceso por un tiempo limitado
            yield env.timeout(min(1, instructions))
            # Se actualiza el contador de instrucciones restantes
            instructions -= 1
            print(f"El proceso tiene {instructions} instructions pendientes en el segundo {env.now:.2f}")
            # El proceso puede pasar a terminated o waiting según las condiciones
            if instructions == 0:
                env.process(terminated_process(env, memory))
            elif random.randint(1, 2) == 1:
                env.process(waiting_process(env, memory, cpu))
    # Si aún quedan instrucciones por realizar, el proceso vuelve a estado ready
    env.process(ready_process(env, memory, cpu))


def waiting_process(env, memory, cpu):
    print(f"El proceso está en la fase <waiting> en el segundo {env.now:.2f}")
    # Espera para ser atendido por el CPU nuevamente
    yield env.timeout(1) #esto creo que tengo que cambiarlo
    #print(f"{name} returns from I/O waiting at {env.now:.2f}")
    # El proceso vuelve a estado ready
    env.process(ready_process(env, memory, cpu))


def terminated_process(env, memory):
    print(f"El proceso terminó en el segundo {env.now:.2f}")
    # Devuelve la cantidad de memoria utilizada
    memory.put(memory.capacity - memory.level)


def process_generator(env, memory, cpu, interval):
    # Genera procesos con una distribución exponencial
    while True:
        yield env.timeout(random.expovariate(1.0 / interval))
        env.process(process(env, memory, cpu))


env.run(50)
