import os
import sys
import datetime

# Read IP address of niping server:
ni_server = '192.168.216.35'
if len(sys.argv) > 1:
    ni_server = sys.argv[1]

iter = 300
if len(sys.argv) > 2:
    if int(sys.argv[2]) > 0:
        iter = int(sys.argv[2])

# Issue dummy niping call because first niping is slow:
os.popen("./niping -c -H " + ni_server + " -L 1").read()

# Periodically invoke niping:
latencies = []
sum_lat = 0
for i in range(0,iter):
    result = os.popen("./niping -c -H " + ni_server + " -L 1").read()
    substr_ix = result.find("avg") + 3 
    substr_end = result.find("ms", substr_ix) + 2
    rel_string = "Single niping at " + str(datetime.datetime.now()) \
      + ':' + result[substr_ix: substr_end]
    sum_lat += float(result[substr_ix: substr_end - 2])
    latencies.append(rel_string)

# Write captured times into a file:
file = open("niping_output_" + str(datetime.datetime.now())[:10] + "_" \
            + str(datetime.datetime.now())[11:16] + ".txt", "w") 
for line in latencies:
    file.write(line + '\n')
file.write("--> Average latency:    " + str(round((sum_lat / iter), 3)) +  ' ms\n')
file.close()
