import asyncio

class BannerGrabber:
    def __init__(self, reader, writer, port):
        self.reader = reader
        self.writer = writer
        self.port = port

    async def analyze(self):
        service = "UNKNOWN"
        banner = "No Banner Response"
        fallback_services = {
            21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 3306: "MYSQL", 3389: "RDP", 8000: "HTTP-ALT"
        }

        try:
            if self.port in [80, 443, 8000, 8080]:
                self.writer.write(b"GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: PortScanner/1.0\r\n\r\n")
                await self.writer.drain()
            
            elif self.port == 3306:
                pass
                
            elif self.port == 21 or self.port == 22 or self.port == 25:
                pass
            data = await asyncio.wait_for(self.reader.read(1024), timeout=1.2)
            
            if data:
                raw_response = data.decode('utf-8', errors='ignore').strip()
                banner = " | ".join([line.strip() for line in raw_response.splitlines() if line.strip()][:2])
                
                
                lower_banner = raw_response.lower()
                
                if "ssh" in lower_banner:
                    service = "SSH"
                    if "-" in raw_response:
                        banner = raw_response.splitlines()[0]
                
                elif "http/" in lower_banner or "server:" in lower_banner or "html" in lower_banner:
                    service = "HTTP"
                    if "443" in str(self.port):
                        service = "HTTPS"
                    for line in raw_response.splitlines():
                        if line.lower().startswith("server:"):
                            banner = line.replace("Server:", "").strip()
                            break
                
                elif "ftp" in lower_banner or raw_response.startswith("220"):
                    service = "FTP"
                    
                elif "mysql" in lower_banner or data[4:9] == b'mysql':
                    service = "MySQL"
                    banner = f"MySQL Server v{data[5:15].decode('utf-8', errors='ignore').strip()}"
                    
                elif "smtp" in lower_banner or raw_response.startswith("220 ") and "mail" in lower_banner:
                    service = "SMTP"
                    
                else:
                    service = fallback_services.get(self.port, "UNKNOWN")
            else:
                service = fallback_services.get(self.port, "UNKNOWN")
                banner = "Port Açık (Veri Akışı Yok)"

        except Exception as e:
            service = fallback_services.get(self.port, "UNKNOWN")
            banner = "Zaman Aşımı (Banner Alınamadı)"

        return banner[:80], service