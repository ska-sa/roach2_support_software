import csv

txtfile = 'edit_msr000a.txt' #name of txt file to be read
f = open(txtfile, 'r') #open for read, use r+w for read and write
csv_read = csv.reader(f, delimiter = ',' )

spl = []
tms = []
tdi = []
tdo = []
cstate = []
fstate = []

for line in csv_read: #read file to an array (will be strings because of header)
  if len(line) == 6:
    spl.append(line[0])
    tms.append(line[1])
    tdi.append(line[2])
    tdo.append(line[3])
    cstate.append(line[4])
    fstate.append(line[5])

f.close() #close file

for i in range (1, len(tms)): #convert all except header to integers
  spl[i] = int(spl[i])
  tms[i] = int(tms[i])
  tdi[i] = int(tdi[i])
  tdo[i] = int(tdo[i])

for i in range (0, len(tms)): #print tab delimited to screen
  print spl[i],'\t', tms[i],'\t', tdi[i],'\t', tdo[i],'\t',cstate[i],'\t',fstate[i]

for i in range (1, len(tms)): #pattern search
  if (tms[i] == 0)and(tms[i+1] == 0)and(tms[i+2] == 1):
    print 'Sample', spl[i], 'State', fstate[i]
