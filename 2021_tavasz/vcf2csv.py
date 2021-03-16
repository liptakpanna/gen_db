import csv

def readVCF(filename, mid, refalt, sampleId):
    f = open(filename, "r")

    lines = f.readlines()
    for line in lines:
            if line[0] != '#':
                data = line.split("\t")
                chrom = data[0]
                pos = data[1]
                ref = data[3]
                alt = data[4]
                qual = data[5]
                curr_vcid = int(pos)
                curr_mid = mid
                info = data[7].split(";")
                dp = info[0].split('=')[-1]
                af = info[1].split('=')[-1]
                
                if ref+","+alt not in refalt:
                    refalt.append(ref+","+alt)
                    mut_writer.writerow([curr_mid,ref,alt])
                    mid += 1
                else:
                    curr_mid = refalt.index(ref+","+alt)+1

                map_writer.writerow([sampleId, curr_vcid,curr_mid, qual, dp, af])
                #print(chrom + "," + pos + "," + ref + "," + alt + "," + qual + "," + dp + "," + af)
    f.close()
    return mid, refalt

var_csv = open("variant_call2.csv", "w")
var_writer = csv.writer(var_csv, delimiter=',')

mut_csv = open("mutation2.csv", "w")
mut_writer = csv.writer(mut_csv, delimiter=',')

map_csv = open("mapping2.csv", "w")
map_writer = csv.writer(map_csv, delimiter=',')

sampleCov_csv = open("sampleCov2.csv", "w")
sampleCov_writer = csv.writer(sampleCov_csv, delimiter=',')

vcid = 1
with open("ERR5380263.coverage", "r") as covFile:
    lines = covFile.readlines()
    for line in lines:
        data = line.split(",")
        chrom = "NC_045512"
        pos = data[0].rstrip()
        ref = data[1].rstrip()
        cov = data[2].rstrip()
        var_writer.writerow([vcid,chrom,pos])
        sampleCov_writer.writerow(['1',vcid,ref,cov])
        vcid += 1

vcid = 1
with open("ERR5380268.coverage", "r") as covFile:
    lines = covFile.readlines()
    for line in lines:
        data = line.split(",")
        chrom = "NC_045512"
        pos = data[0].rstrip()
        ref = data[1].rstrip()
        cov = data[2].rstrip()
        sampleCov_writer.writerow(['2',vcid,ref,cov])
        vcid += 1

mid = 1
refalt = []

mid, refalt = readVCF("ERR5380263.annot.vcf", mid, refalt, '1')
readVCF("ERR5380268.annot.vcf", mid, refalt, '2')

var_csv.close()
mut_csv.close()
map_csv.close()
sampleCov_csv.close()