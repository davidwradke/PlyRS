import sys

config_range_highest = sys.argv[1]
bottom_range = int(config_range_highest) - 10000 #batch in chunks of 10000
top_range = int(config_range_highest)

filename = "step2example-DHS_hotspot-configurations_database.txt"
f_in = open(filename)

configurations = {}

for i in f_in:
    line = i.rstrip()
    if line.startswith("database"):
        words = line.split("=")
        database_freq = float(words[1])
        continue
    if line.startswith("totalsites"):
        words = line.split("=")
        totalsites = int(words[1])
        continue
    words = line.split("\t")
    config = words[0]
    occurrences = int(words[1])
    configurations[config] = occurrences
f_in.close()

specific_configurations = {}

f_in2 = open(filename)

counter = 0
for i in f_in2:
    line = i.rstrip()
    if line.startswith("database"):
        continue
    if line.startswith("totalsites"):
        continue
    counter += 1
    if (counter > bottom_range and counter <= top_range): #break up configurations scored into smaller chunks
        words = line.split("\t")
        config = words[0]
        occurrences = int(words[1])
        specific_configurations[config] = occurrences
    else: continue


# Define shared tissues value for each configuration

def vect_prepare(input_vector):
    count = -1
    tissue_shared = set()
    tissue_notshared = set()
    for i in range(0,len(input_vector),1):
        count += 1
        if input_vector[i] == "1":
            tissue_shared.add(count)
        if input_vector[i] == "0":
            tissue_notshared.add(count)
    results = [tissue_shared,tissue_notshared] #this is a list of two sets
    return results

configurations_shared = {}

configurations_notshared = {}

for key,value in configurations.items():
    vector = str(key)
    vect_shared = vect_prepare(vector)[0] #this is a set of reg elem-based annotations from the vector
    vect_notshared = vect_prepare(vector)[1] #this is a set of non reg elem-based annotations from the vector
    configurations_shared[vector] = vect_shared
    configurations_notshared[vector] = vect_notshared

share_sites_dict = {}

notshare_sites_dict = {}

def share_sites_count(vector):
    shared_sites = 0
    shared_site_tissues = configurations_shared[vector] #this is a set
    for key,config_set in configurations_shared.items():
        if shared_site_tissues <= config_set: #sites that minimally share all in the given vector
            shared_sites += configurations[key]
        else: continue
    share_sites_dict[vector] = shared_sites

def notshare_sites_count(vector):
    notshared_sites = 0
    notshared_site_tissues = configurations_notshared[vector] #this is a set
    for key,config_set in configurations_notshared.items():
        if notshared_site_tissues <= config_set: #sites that minimally don't share all in the given vector
            notshared_sites += configurations[key]
        else: continue
    notshare_sites_dict[vector] = notshared_sites

for key in specific_configurations.keys(): #only examine the configurations in the reduced chunk specified earlier
    share_sites_count(key)
    notshare_sites_count(key)

n_eff_share_dict = {}

n_eff_notshare_dict = {}

def n_eff_share_calc():
    for key,value in share_sites_dict.items():
        numerator = value-1 #subtract 1 to remove the observation site
        denominator = totalsites-1 #subtract 1 to remove the observation site
        fraction = numerator/denominator
        n_eff = np.log10(fraction)/np.log10(database_freq) #using mathematical relation to solve for n_eff
        n_eff_share_dict[key] = n_eff

def n_eff_notshare_calc():
    for key,value in notshare_sites_dict.items():
        numerator = value-1 #subtract 1 to remove the observation site
        denominator = totalsites-1 #subtract 1 to remove the observation site
        fraction = numerator/denominator
        n_eff = np.log10(fraction)/np.log10(1-database_freq) #using mathematical relation to solve for n_eff
        n_eff_notshare_dict[key] = n_eff

import numpy as np

n_eff_share_calc()
n_eff_notshare_calc()

f_out_share_notshare_filename = "neff_share_notshare_DHS_hotspot-group"+str(top_range)+".txt"
f_out_share_notshare = open(f_out_share_notshare_filename,"w")

for k in share_sites_dict.keys():
#     if (k in n_eff_share_dict) and (k in n_eff_notshare_dict):
    n_share = n_eff_share_dict[k]
    n_notshare = n_eff_notshare_dict[k]
    n_ratio = n_share/(n_share+n_notshare) #divide by total, so ratio is always between 0 and 1
    f_out_share_notshare.write(str(k)+"\t"+str(n_share)+"\t"+str(n_notshare)+"\t"+str(n_ratio)+"\n")

f_out_share_notshare.close()