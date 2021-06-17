
from time import sleep
from multiprocessing import Process


def print_name(name):
    print("start processing")
    sleep(5)
    print(f'hello {name}')


names = ['Ross', 'Monica', 'Chandler', 'Joey', 'Phoebe', 'Rachel']

processes = []
for name in names:
    p = Process(target=print_name, args=[name])
    processes.append(p)
    p.start()

for p in processes:
    p.join()

print("finished")
