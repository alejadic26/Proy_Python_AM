import time
#from time import time
import logging

#Configurar logger

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def timeit(func):
    def wrapper(*args,**kwargs):
        start_time=time.time()
        resultado=func(*args,**kwargs)
        end_time=time.time()
        elapsed_time=end_time - start_time
        logging.info(f"{func.__name__} ,ejecutada en {elapsed_time:.4f} segundos")
        return resultado
    return wrapper

def logit(func):
    def wrapper(*args,**kwargs):
        logging.info(f"Corriendo {func.__name__}")
        resultado=func(*args,**kwargs)
        logging.info(f"Completado {func.__name__}")
        return resultado
    return wrapper