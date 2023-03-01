import random;
import simpy;
import math;


def mesero (env):
    while True:
        print(f"Se toma la orden en el segundo: {env.now}", );
        tomaOrden = 5;
        yield env.timeout(tomaOrden);

        print(f"Los meseros dan la orden a los cocineros en el segundo {env.now}")
        daOrden = 2;
        yield env.timeout(daOrden);

        print(f"Los meseros sirven la comida a los comensales en el segundo {env.now}\n");
        sirveOrden = 5;
        yield env.timeout(sirveOrden);

env = simpy.Environment();
env.process(mesero(env));
env.run(30);





