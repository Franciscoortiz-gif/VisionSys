import cython
import time

def primes(num):
    num = [2,3,67,4,8,34,2,65,7,3,4,6,7,645,33,2,7,655,45,445,53,3]
    inicio = time.time()
    for n in range(2, num):
        if num % n == 0:
            print("No es primo", n, "es divisor")
            return False
    print("Es primo")
    
    final = time.time()
    
    tiempofinal = final - inicio
    print(tiempofinal)
    return True


def primos(num: cython.int[22]):
    num = [2,3,67,4,8,34,2,65,7,3,4,6,7,645,33,2,7,655,45,445,53,3]