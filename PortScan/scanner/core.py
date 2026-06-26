import asyncio
import socket
from datetime import datetime
from scanner.grabber import BannerGrabber

class PortScannerEngine:
    """Linux epoll/Selector tabanlı, asenkron ve hız sınırlamalı ağ tarama motoru."""
    def __init__(self, target, ports, rate_limit, timeout):
        self.target = target
        self.ports = ports
        self.semaphore = asyncio.Semaphore(rate_limit)
        self.timeout = timeout
        self.results = []

    async def _scan_port(self, port, callback=None):
        async with self.semaphore:
            try:
                fut = asyncio.open_connection(self.target, port)
                reader, writer = await asyncio.wait_for(fut, timeout=self.timeout)
                grabber = BannerGrabber(reader, writer, port)
                banner, service = await grabber.analyze()
                
                self.results.append({
                    "port": port,
                    "status": "OPEN",
                    "service": service,
                    "banner": banner,
                    "timestamp": datetime.now().isoformat()
                })
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            finally:
                if callback:
                    callback()

    async def start(self, progress_callback=None):
        """Tüm port tarama görevlerini eszamanli baslatir."""
        tasks = [asyncio.create_task(self._scan_port(p, progress_callback)) for p in self.ports]
        await asyncio.gather(*tasks)
        return sorted(self.results, key=lambda x: x["port"])