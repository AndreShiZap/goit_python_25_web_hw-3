from multiprocessing import Process, Queue, cpu_count
from time import time


# синхронна версія
def factorize(*number):
    result = list()
    for x in number:
        dividers = []
        for y in range(1, x + 1):
            if x % y == 0:
                dividers.append(y)
        result.append(dividers)
    return result


# мультипроцесорна версія
def factor(x, queue):
    dividers = []
    for y in range(1, x + 1):
        if x % y == 0:
            dividers.append(y)
    queue.put(dividers)


def factorize_proc(*numbers):
    processes = []
    queue = Queue()
    n = cpu_count()
    # припущення: кількість вхідних значень дорівнює кількості ядер процесора
    for i in range(n):
        process = Process(target=factor, args=(numbers[i], queue))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    results = []
    while not queue.empty():
        results.append(queue.get())
    return results


if __name__ == "__main__":
    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"час виконання (синхронна версія): {round(time() - timer, 4)}")

    timer = time()
    a, b, c, d = factorize_proc(128, 255, 99999, 10651060)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"час виконання (мультипроцесорна версія): {round(time() - timer, 4)}")
