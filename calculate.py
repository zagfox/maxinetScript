import numpy

def calculate(workerNum):
    data = []
    file = open('log.txt')
    for line in file:
        if 'c' not in line:
	    continue
	data.append(float(line.split(' ')[1]))
    print data

    result = []
    for i in range(0, workerNum):
        result.append(0)
        for j in range(0, len(data), workerNum):
	    result[i] += data[j+i]
	    
    print result	

calculate(2)
