import asyncio
import socket
import json
import argparse
import sys
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from rich.console import Console
from scanner.core import PortScannerEngine
from scanner.reporter import Reporter
from scanner.utils import parse_ports

console = Console()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.websocket("/ws/scan")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        config = json.loads(data)
        
        ports = parse_ports(config.get("ports", "1-1024"))
        target_ip = socket.gethostbyname(config.get("target"))
        rate_limit = int(config.get("rate_limit", 1000))
        timeout = float(config.get("timeout", 0.3))      


        semaphore = asyncio.Semaphore(rate_limit)
        total_ports = len(ports)
        current = 0

        async def scan_single_port(port):
            nonlocal current
            async with semaphore:
                try:
                    conn = asyncio.open_connection(target_ip, port)
                    reader, writer = await asyncio.wait_for(conn, timeout=timeout)
                    from scanner.grabber import BannerGrabber
                    grabber = BannerGrabber(reader, writer, port)
                    banner, service = await grabber.analyze()
                    
                    await websocket.send_json({
                        "type": "found",
                        "port": port,
                        "service": service,
                        "banner": banner
                    })
                    writer.close()
                    await writer.wait_closed()
                except:
                    pass
                finally:
                    current += 1
                    if current % 5 == 0 or current == total_ports:
                        try:
                            await websocket.send_json({"type": "progress", "progress": int((current/total_ports)*100)})
                        except:
                            pass

        await websocket.send_json({"type": "info", "message": f"🚀 {target_ip} üzerinde canavar motor başlatıldı..."})
        await asyncio.gather(*[scan_single_port(p) for p in ports])
        await websocket.send_json({"type": "completed"})

    except WebSocketDisconnect:
        pass
    finally:
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    print("[*] PortScanner C2 sunucusu başlatılıyor...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", loop="asyncio")