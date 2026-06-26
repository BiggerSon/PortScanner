import sys

def parse_ports(port_arg):
    ports = set()
    try:
        for part in port_arg.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part))
        return sorted(list(ports))
    except Exception:
        print("[!] Port formatı geçersiz! Örnek: 22,80 veya 1-1024")
        sys.exit(1)