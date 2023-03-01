#Codigo que hace una simulacion de procesos
#Irving Acosta - 22781

import random
import simpy
import numpy

# Referencias de https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html

print("\n\n--------------------Simulación en curso--------------------\n\n")

arr = []
# init = 100
capacity = 100  # ram memory capacity (100 y 200)
timeIni = 0
rango = 10  # Intervalos (1, 5, 10)
inst = 3  # instrucciones del ciclo (3, 6)
operacion = 1  # operaciones por ciclo
procesosCant = 50  # numero de procesos (25,50,100,150 y 200)
cantprocesadores = 1


def proceso(env, cantRam, cantInstrucciones, idProceso, inst, operacion, memoriaDisponible, accesoProcesador,
            tiempoinicio):
    # El código muestra información del proceso nuevo en cola con la cantidad de RAM requerida y disponible
    global timeIni  # variable global

    yield env.timeout(tiempoinicio)
    tiempoInicioIndividual = env.now
    # Utilizando f-strings
    print(
        f" {idProceso}, en cola [NEW]. Tiempo: {env.now:.1f}. Cantidad de RAM requerida: {cantRam}. Cantidad de RAM disponible: {memoriaDisponible.level}")  # Representa la memoria RAM disponible para ser utilizada por los procesos en la simulación
    yield memoriaDisponible.get(cantRam)
    print(
        f" {idProceso}, en cola [READY] en tiempo {env.now:.1f}. Cantidad de instrucciones pendientes: {cantInstrucciones}")

    # Se ejecuta mientras la cantidad de instrucciones pendientes sea mayor a cero
    while cantInstrucciones > 0:
        # procesamiento de instrucciones en un procesador
        with accesoProcesador.request() as solicitud:
            yield solicitud
            cantInstrucciones -= inst
            yield env.timeout(operacion)  # tiempo en cada operación
            print(
                f" {idProceso}, proceso en cola [READY] en tiempo {env.now:.1f}. Cantidad de instrucciones pendientes {cantInstrucciones}")  # Utilizando f-strings

        # representación lógica para mover los procesos a la cola de espera si quedan instrucciones pendientes
        if cantInstrucciones > 0 and random.randint(1, 2) == 1:
            # si quedan instrucciones pendientes, mover a la cola de espera
            print(f" {idProceso}, ha ingresado a la cola [WAITING]")  # Utilizando f-strings
            yield env.timeout(random.randint(1, 5))  # espera un tiempo aleatorio (entre 1 y 5 unidades de tiempo)

    # Encargado de llevar un registro del tiempo en que un proceso es eliminado y devuelve la cantidad de memoria que se liberó
    yield memoriaDisponible.put(cantRam)
    arr.append(tiempoInicioIndividual)
    print(
        f" {idProceso}, proceso [TERMINATED] en tiempo {env.now:.1f}. Cantidad de RAM devuelta: {cantRam}. Cantidad de memoria disponible: {memoriaDisponible.level}")


# nuevo objeto de la clase Environment
env = simpy.Environment()  # entorno de simulación
# cantidad de memoria disponible en la simulación
memoriaDisponible = simpy.Container(env, capacity, capacity)
accesoProcesador = simpy.Resource(env, cantprocesadores)

# Cada proceso se genera con una cantidad random de instrucciones y RAM requerida
for c in range(procesosCant):  # (25,50,100,150 y 200)

    # representa el tiempo de llegada del siguiente proceso a la simulación.
    # https://www.geeksforgeeks.org/random-expovariate-function-in-python/
    tiempo_inicio = random.expovariate(
        1.0 / rango)  # valor random que representa el tiempo de inicio random de un proceso
    cantInstrucciones = random.randint(1, 10)  # genera una cantidad random de instrucciones
    cantRam = random.randint(1, 10)  # genera una cantidad random de RAM
    env.process(
        proceso(env=env, cantRam=cantRam, cantInstrucciones=cantInstrucciones, idProceso=f"Proceso {c}", inst=inst,
                operacion=operacion, memoriaDisponible=memoriaDisponible, accesoProcesador=accesoProcesador,
                tiempoinicio=tiempo_inicio))  # crea un nuevo proceso en la simulación y se agrega a env

# Ejecutar la simulación
# Calcula y muestra el tiempo promedio
env.run()
promed = numpy.mean(arr)
desviacion = numpy.std(arr)
print(
    f"\nEl tiempo promedio de finalización de los procesos es de {promed} segundos con una desviacion estandar de {desviacion}\n")