import simpy
from random import randint
from decimal import Decimal
import statistics


class Process:
    def __init__(self, id, memory, instructions):
        self.memory = memory
        self.instructions = instructions
        self.id = id


class System:
    def __init__(self, env, ram, cpu, processID, instructions):
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.instructions_per_cycle = instructions
        self.process_id = processID
        env.process(self.run())


def run(self):
    # Tiempo de inicio del proceso
    starTime = self._currentTime()

    # Creación de un nuevo proceso
    process = self.create_process()

    # Mostrar información del proceso
    print(f'➡ Minuto {self._currentTime()}: Proceso {process.id} (Nuevo)')

    # Solicitar memoria
    yield self.requestMemory(process)

    # Inicia la ejecucion de funciones
    yield self.executeInstructions(process)

    # Libera el espacio de memoria que estaba usando el proceso
    yield self.releaseMemory(process)

    # Registra el tiempo de ejecución del proceso
    endTime = self._currentTime()
    executionTime = Decimal(endTime) - Decimal(starTime)
    processTimes.append(executionTime)

def newProcess(self):
    # Genera valores aleatorios para la memoria y las instrucciones
    memory = randint(1, 10)
    instructions = randint(1, 10)
    # Creación de una variable Proceso
    process = Process(self.process_id, memory, instructions)
    return process

def requestMemory(self, process):
    # Espera a que haya suficiente espacio de memoria
    with self.ram.get(process.memory) as ramRequest:
        yield ramRequest
        print(f'  Minuto {self._currentTime()}: Proceso{process.id} (Ready)')

def executeInstructions(self, process):
    cycle_counter = 0
    # Ejecuta instrucciones hasta que finalice el proceso
    while process.instructions > 0:
        # Solicita CPU
        with self.cpu.request() as cpuRequest:
            yield cpuRequest
            cycle_counter += 1
            print(f'  Minuto {self._currentTime()}: Proceso {process.id} (Running Cycle {cycle_counter})')

            # Ejecuta el numero de intrucciones declarado en la variable instrucciones
            process.instructions -= self.instructions_per_cycle

            # Comprueba si el proceso ya terminó de ejecutarse
            if process.instructions <= 0:
                print(f'  Minuto {self._currentTime()}: Proceso {process.id} (Terminated)')
            else:
                # Decide next state
                next_state = randint(1, 2)

                if next_state == 1:
                    # Espera por el I/O
                    print(f'  Minuto {self._currentTime()}: Proceso {process.id} (Waiting I/O)')
                    waiting_time = randint(1, 5)
                    yield self.env.timeout(waiting_time)
                else:
                    # Lo devuelve al estado "ready"
                    print(f'  Time {self._currentTime()}: Process {process.id} (Ready)')

            # Liber CPU
            yield self.cpu.release(cpuRequest)

def releaseMemory(self, process):
    yield self.ram.put(process.memory)

processTimes = []

def showData():
    print('\n---ESTATISTICAS---\n')
    print(f'✓ Tiempo promedio de ejecución: {statistics.mean(processTimes)}')
    print(f'✓ Desviación estandar: {statistics.pstdev(processTimes)}')
