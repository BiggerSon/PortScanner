from rich.console import Console
from rich.table import Table

console = Console()

class Reporter:
    @staticmethod
    def to_cli(results):
        table = Table(title="🛡️ PORTSCANNER SIZMA TESTİ RAPORU", title_style="bold red", show_lines=True)
        table.add_column("PORT", justify="center", style="cyan")
        table.add_column("DURUM", justify="center", style="green")
        table.add_column("TAHMİNİ SERVİS", justify="center", style="yellow")
        table.add_column("BANNER İSTİHBARATI", justify="left", style="white")

        for r in results:
            table.add_row(str(r["port"]), r["status"], r["service"], r["banner"])
        
        console.print("\n")
        console.print(table)