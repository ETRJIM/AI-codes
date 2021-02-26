import numpy
import matplotlib.pyplot as plt
from csv import reader
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for column in csv_reader:
            if not column:
                continue
            dataset.append(column)
    return dataset

def total_dist(locations):
    distance = 0
    for i in range(0,len(locations)):
        distance += ((locations[i-1][0] - locations[i][0])**2 + (locations[i-1][1] - locations[i][1])**2)**0.5
    return distance

def sim_ani(locations_coordinates,T = 1000,factor = 0.99):
    cost_initial = total_dist(locations_coordinates)
    for i in range(5000):
        print(i, "cost = ", cost_initial)
        T = T * factor
        for j in range(200):
            r1, r2 = numpy.random.randint(0, len(locations_coordinates), size=2)
            locations_coordinates[r1], locations_coordinates[r2] = locations_coordinates[r2], locations_coordinates[r1]
            cost_new = total_dist(locations_coordinates)

            if cost_new < cost_initial:
                cost_initial = cost_new
            else:
                x = numpy.random.uniform()
                if x < numpy.exp((cost_initial - cost_new) / T):
                    cost_initial = cost_new
                else:
                    locations_coordinates[r1], locations_coordinates[r2] = locations_coordinates[r2], locations_coordinates[r1]
    return cost_initial

filename = r'pbn423.csv'
df = load_csv(filename)
print(df)
locations_coordinates = []
for i in range(1, len(df)):
    locations_coordinates.append((float(df[i][1]), float(df[i][2])))

#locations_coordinates = [[0,0],[1,2],[3,4],[4,7],[8,9],[0,1],[2,0],[2,2],[1,0],[0,2],[1,1],[2,1],[5,6],[6,4],[3,5],[6,2],[2,7],[1,8],[0,9],[7,0]]
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
for i in range(0,len(locations_coordinates)):
    ax1.plot([locations_coordinates[i][0],locations_coordinates[i-1][0]],[locations_coordinates[i][1],locations_coordinates[i-1][1]],'b')
for c in locations_coordinates:
    ax1.plot(c[0], c[1], 'ro')

sim_ani(locations_coordinates)

for i in range(0,len(locations_coordinates)):
    ax2.plot([locations_coordinates[i][0],locations_coordinates[i-1][0]],[locations_coordinates[i][1],locations_coordinates[i-1][1]],'b')
for c in locations_coordinates:
    ax2.plot(c[0], c[1], 'ro')
plt.show()