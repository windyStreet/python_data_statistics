tasks = []
x = []
for value in range(21,24):
    del x[:]
    x.append(value)
    task={"yy":x.copy(),
          "xx":x.copy()}
    tasks.append(task)

x = ["123"]
task={"yy":x,"xx":x}
tasks = []
tasks.append(task)

for task in tasks:
    print(task)
print("xxxxxxxxxxx")
print(tasks)