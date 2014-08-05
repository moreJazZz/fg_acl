from sys import argv, exit

script, filename = argv

if len(argv) != 2:
    exit('''
Usage: fortigate_acl.py ip_address_file.txt

where "ip_address_file.txt" should consists of:
  ip address and hostname

Bye!''')


def yes_no(q):  #Ask yes or no question
    answer = raw_input(q).lower()
    while answer not in ["y","n"]:
        print("\nInvalid response!\n")
        answer = raw_input(q).lower()
    if "y" in answer:
        return 1
    else:
        return 0

interface = raw_input("What interface you would like to use for hosts? ")

# Put our data here!
hosts = []

with open(filename, 'r') as f:
    for line in f:
        splited_line = line.split()

        if len(splited_line) != 2:
            exit("Check your %s!\nError line: %s" % (filename, line))

        ip = splited_line[0].strip()
        host = splited_line[1].strip().lower()

        if ip == host:
            host = host + "_block"

        hosts.append((ip, host))

print 'And we have:\n%r' % hosts


with open('result.txt', 'w') as target:

    for i in hosts:
        ip = i[0]
        host = i[1]

        target.write ( 'edit %s\n' % host)
        target.write ( 'set associated-interface %s\n' % interface)
        target.write ( 'set subnet %s 255.255.255.255\n' % ip)
        target.write ( 'next\n' )
        target.write ( '!\n' )

with open('result.txt', 'a') as target:
    choice = yes_no("\nDo you want to create a group? [y/n]: ")
    if choice == 1:
        hostnameset =  ' '.join(['"' + i[1] + '"' for i in hosts])
        groupname = raw_input("What group do you want to create for hosts? ")

        target.write ( '!\n'*5 )
        target.write ( 'config firewall addrgrp\n' )
        target.write ( 'edit "%s"\n' % groupname)
        target.write ( 'set member %s\n' % hostnameset)
        target.write ( 'next\n' )
        target.close()
    else:
        print("\nExiting now")
        exit()


print 'Access rules and group created!'



#print "".join(('"',host,'"'))

#print ' '.join(['"' + i[1] + '"' for i in hosts])

#tmp =[]
#for i in hosts:
#    tmp.append('"' + i[1] + '"')
#print ' '.join(tmp)

#with open('result.txt', 'w') as target:
#
#    for i in hosts:
#        ip = i[0]
#        host = i[1]
#