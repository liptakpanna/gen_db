import csv
import random

def getBases():
    abc = ["A", "C", "G", "T"]
    n = random.randint(1,4)
    res = ""
    for _ in range(n):
        res += random.choice(abc)
    return res

var_csv = open("variant_call.csv", "w")
var_writer = csv.writer(var_csv, delimiter=',')

mut_csv = open("mutation.csv", "w")
mut_writer = csv.writer(mut_csv, delimiter=',')

map_csv = open("mapping.csv", "w")
map_writer = csv.writer(map_csv, delimiter=',')

vcid = 1
mid = 1

chrompos = []
refalt = []

for _ in range(500000):

    #chrom between 1,22
    chrom = str(random.randint(1,22))
    #post between 1,30000
    pos = str(random.randint(1,30000))
    #ref get random bases between 1,4 
    ref = getBases()
    alt = getBases()

    curr_vcid = vcid
    curr_mid = mid

    if chrom+","+pos not in chrompos:
        chrompos.append(chrom+","+pos)
        var_writer.writerow([curr_vcid,chrom,pos])
        vcid += 1
    else:
        curr_vcid = chrompos.index(chrom+","+pos)+1
    
    if ref+","+alt not in refalt:
        refalt.append(ref+","+alt)
        mut_writer.writerow([curr_mid,ref,alt])
        mid += 1
    else:
        curr_mid = refalt.index(ref+","+alt)+1

    map_writer.writerow([curr_vcid,curr_mid])
    

var_csv.close()
mut_csv.close()
map_csv.close()