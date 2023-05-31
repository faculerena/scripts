import os
import re

# pattern to match lines
pattern = re.compile(r"\[Stats #\d+\] run time: (.*?), clients: \d+, corpus: \d+, objectives: \d+, executions: (\d+), exec/sec: (\d+)")

# target hours
target_hours = ["{}h-0m-0s".format(i) for i in range(1, 25)]

output = []

prefixName = "run"

extension = ".txt"

# assuming all files are in the same directory as the script
for filename in os.listdir():
    if filename.startswith(prefixName) and filename.endswith(extension):
        print(f'Processing {filename}')
        with open(filename, 'r') as file:
            run_data = []
            seen_hours = set()
            for line in file.readlines():
                match = pattern.match(line.strip())
                if match:
                    runtime = match.group(1)
                    executions = match.group(2)
                    exec_sec = match.group(3)
                    if runtime in target_hours and runtime not in seen_hours:
                        seen_hours.add(runtime)
                        run_data.append(f"{runtime}, {executions}, {exec_sec}")
            if run_data:
                output.append(f"{filename[:-4]}")  # remove .txt from the filename
                output.extend(run_data)

# writing to the output file
with open('output.txt', 'w') as file:
    for line in output:
        file.write(line + '\n')



# this was made to read all the log files called "run[date].txt" and extract the lines that match the pattern