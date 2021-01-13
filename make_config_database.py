# Gather all annotation configurations
import numpy as np
configurations = {}

f_in1 = open("filepath.../chr1_vectors.txt")
f_in2 = open("filepath.../chr2_vectors.txt")
f_in3 = open("filepath.../chr3_vectors.txt")
f_in4 = open("filepath.../chr4_vectors.txt")
f_in5 = open("filepath.../chr5_vectors.txt")
f_in6 = open("filepath.../chr6_vectors.txt")
f_in7 = open("filepath.../chr7_vectors.txt")
f_in8 = open("filepath.../chr8_vectors.txt")
f_in9 = open("filepath.../chr9_vectors.txt")
f_in10 = open("filepath.../chr10_vectors.txt")
f_in11 = open("filepath.../chr11_vectors.txt")
f_in12 = open("filepath.../chr12_vectors.txt")
f_in13 = open("filepath.../chr13_vectors.txt")
f_in14 = open("filepath.../chr14_vectors.txt")
f_in15 = open("filepath.../chr15_vectors.txt")
f_in16 = open("filepath.../chr16_vectors.txt")
f_in17 = open("filepath.../chr17_vectors.txt")
f_in18 = open("filepath.../chr18_vectors.txt")
f_in19 = open("filepath.../chr19_vectors.txt")
f_in20 = open("filepath.../chr20_vectors.txt")
f_in21 = open("filepath.../step1example-chr21_DHS_hotspot.vectors.head10000.txt")
f_in22 = open("filepath.../chr22_vectors.txt")

f_in_chroms = [f_in1,f_in2,f_in3,f_in4,f_in5,f_in6,f_in7,f_in8,f_in9,f_in10,f_in11,f_in12,f_in13,f_in14,f_in15,f_in16,f_in17,f_in18,f_in19,f_in20,f_in21,f_in22]

for i in f_in_chroms:
    for j in i:
        line = j.rstrip()
        words = j.split("\t")
        coordinate = words[0]
        configuration = words[1].rstrip()
        if configuration in configurations:
            configurations[configuration] += 1
        else:
            configurations[configuration] = 1    

print(len(configurations))


# Find total database frequency of an annotation
total_annotations = 0
total_positions = 0
for i,j in configurations.items():
    key = i
    value = j
    ann_count_config = key.count("1")
    total_ann_count = ann_count_config*value
    total_annotations += total_ann_count
    total_pos_config = len(key)*value
    total_positions += total_pos_config

database_freq = total_annotations/total_positions
print(database_freq)

totalsites = 0
for key,value in configurations.items():
    totalsites += value
f_out = open("step2example-DHS_hotspot-configurations_database.txt","w")
f_out.write(str("database-frequency=")+str(database_freq)+"\n")
f_out.write(str("totalsites=")+str(totalsites)+"\n")
for k,v in configurations.items():
    config = k
    number_config = v
    f_out.write(str(config)+"\t"+str(number_config)+"\n")
f_out.close()

