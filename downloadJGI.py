import os

os.system('curl 'https://signon.jgi.doe.gov/signon/create' --data-urlencode 'login=lgozasht@ucsc.edu' --data-urlencode 'password=*******' -c cookies > /dev/null')
os.system('curl 'https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism=PerpolsubgrisePO_FD' -b cookies > files.xml')


with open('files.xml','r') as f:
    next(f)
    next(f)
    next(f)

    for line in f:
        sp = line.split(' ')
        for i in sp:
            if 'url' in i:
                filename = i.split('/')[-1]
                print("curl \'https://genome.jgi.doe.gov{0}\' -b cookies > {1}".format(i.replace('&amp;','&').split('\"')[1].strip('\"'),filename.strip('\"')))
                os.system("curl \'https://genome.jgi.doe.gov{0}\' -b cookies > {1}".format(i.replace('&amp;','&').split('\"')[1].strip('\"'),filename.strip('\"')))            
