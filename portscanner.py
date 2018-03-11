import optparse
import socket
from threading import *
from socket import *


screeLock = Semaphore(value=1)
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send(b'Ping')
        results = connSkt.recv(100)
        screeLock.acquire()
        print("[+] %d/TCP OPEN"%(tgtPort))
        print(str(results.decode()))
    except Exception as e:
        screeLock.acquire()
        print(e)
    finally:
        screeLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except Exception as e:
        print("[!] Cannot resolve: " + str(tgtHost))
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan results for: " + tgtName[0])
    except Exception as e:
        print("\r\n[+} Scan results for: " + tgtIP)
        setdefaulttimeout(1)

    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()
        print("Scanning port " + tgtPort)
        connScan(tgtHost, int(tgtPort))

def main():
    parser = optparse.OptionParser(usage=' usage %prog -H' + ' <target host> -p <target port> ')
    parser.add_option("-x", dest="tgtHost", default=False, help="target host", type="string")
    parser.add_option("-p", dest="tgtPort", default="80", help="target ports")
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPort = str(options.tgtPort).split(',')
    print(tgtPort)

    if tgtHost == None or tgtPort == None:
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPort)


if __name__ == '__main__':
    main()
