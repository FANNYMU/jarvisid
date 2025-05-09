from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import box
from groq import Groq
import os
import re
import time
import sys
from shutil import get_terminal_size
from datetime import datetime

# Konfigurasi API key
API_KEY = "YOUR_API_KEY"

# Inisialisasi console dan client
console = Console()
client = None

def setup():
    """Persiapkan lingkungan dan instal dependensi yang diperlukan."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Menyiapkan lingkungan..."),
            console=console,
        ) as progress:
            task = progress.add_task("", total=3)
            
            # Instal dependensi
            os.system('pip install rich --quiet')
            progress.update(task, advance=1)
            
            os.system('pip install groq --quiet')
            progress.update(task, advance=1)
            
            # Bersihkan layar
            os.system('cls' if os.name == 'nt' else 'clear')
            progress.update(task, advance=1)
        
        # Inisialisasi client Groq
        global client
        client = Groq(api_key=API_KEY)
        
        # Tampilkan banner startup
        show_banner()
        return True
    except Exception as e:
        console.print(f"[bold red]Error saat setup: {str(e)}[/bold red]")
        return False

def show_banner():
    """Tampilkan banner selamat datang."""
    width = get_width(80)
    
    # Banner ASCII Art
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗ ██████╗  ██████╗  ██████╗      █████╗ ██╗          ║
    ║  ██╔════╝ ██╔══██╗██╔═══██╗██╔═══██╗    ██╔══██╗██║          ║
    ║  ██║  ███╗██████╔╝██║   ██║██║   ██║    ███████║██║          ║
    ║  ██║   ██║██╔══██╗██║   ██║██║▄▄ ██║    ██╔══██║██║          ║
    ║  ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝    ██║  ██║██║          ║
    ║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══▀▀═╝     ╚═╝  ╚═╝╚═╝          ║
    ║                                                               ║
    ║             Terminal Assistant - Llama 3.3 70B                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    
    # Tampilkan versi aplikasi dan tanggal
    today = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    # Buat tabel untuk informasi
    table = Table(box=box.ROUNDED, expand=False, width=width)
    table.add_column("Informasi", style="cyan")
    table.add_column("Detail", style="green")
    
    table.add_row("Dibuat Oleh", "Chandra")
    table.add_row("GitHub", "https://github.com/FANNYMU")
    table.add_row("WhatsApp", "08819538083")
    table.add_row("Model", "llama-3.3-70b-versatile")
    table.add_row("Versi", "1.0.0")
    table.add_row("Tanggal", today)
    
    # Tampilkan banner dan info
    console.print(Text(banner, style="bold blue"))
    console.print(table)
    console.print("\n[bold yellow]Ketik 'help' untuk melihat daftar perintah atau langsung masukkan prompt Anda.[/bold yellow]\n")

def get_width(max_width=80, margin=10):
    """Ambil lebar terminal responsif dengan batas maksimum."""
    terminal_width = get_terminal_size((80, 20)).columns
    return min(max_width, terminal_width - margin)

def display_help():
    """Tampilkan informasi bantuan."""
    help_table = Table(title="Perintah yang Tersedia", box=box.ROUNDED, title_style="bold magenta")
    help_table.add_column("Perintah", style="cyan")
    help_table.add_column("Deskripsi", style="green")
    
    help_table.add_row("help", "Menampilkan daftar perintah")
    help_table.add_row("clear", "Membersihkan layar terminal")
    help_table.add_row("exit", "Keluar dari aplikasi")
    help_table.add_row("info", "Menampilkan informasi aplikasi")
    help_table.add_row("model", "Menampilkan informasi model yang digunakan")
    help_table.add_row("<prompt>", "Masukkan prompt apapun untuk bertanya ke AI")
    
    console.print(help_table)

def display_model_info():
    """Tampilkan informasi tentang model."""
    model_info = Panel(
        "[bold]llama-3.3-70b-versatile[/bold]\n\n"
        "Model Llama 3.3 70B adalah model bahasa besar terbaru dari Meta AI, "
        "dengan kemampuan tinggi dalam memahami dan menghasilkan teks dalam berbagai bahasa. "
        "Model ini memiliki parameter sebanyak 70 miliar dan telah dilatih pada dataset yang luas.\n\n"
        "[italic]Keunggulan:[/italic]\n"
        "• Kemampuan pemahaman konteks yang lebih baik\n"
        "• Mendukung banyak bahasa termasuk Bahasa Indonesia\n"
        "• Lebih baik dalam instruksi kompleks dan penalaran\n"
        "• Pengetahuan general yang luas",
        title="Informasi Model",
        border_style="green",
        width=get_width(100)
    )
    console.print(model_info)

def groq_service(prompt: str):
    """Kirim permintaan ke API Groq dan ambil respons."""
    if not client:
        return "Error: Koneksi ke Groq belum tersedia."
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Memproses permintaan..."),
            console=console,
        ) as progress:
            task = progress.add_task("", total=None)
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. "
                            "If the user clearly requests to run a system command, "
                            "respond with the command wrapped in <command> tags. "
                            "Do NOT include <command> tags if no command is requested. "
                            "Always respond in Indonesian. "
                            "Format your responses using Markdown when appropriate."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=500,  # Ditingkatkan untuk respons yang lebih komprehensif
                temperature=0.7,
            )
            
            # Delay kecil untuk UX yang lebih baik
            time.sleep(0.5)
            
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def execute_if_command_present(response: str):
    """Periksa respons untuk perintah sistem dan jalankan jika ada."""
    match = re.search(r"<command>(.*?)</command>", response, re.DOTALL)
    if match:
        command = match.group(1).strip()
        
        # Tampilkan peringatan keamanan untuk perintah tertentu
        danger_commands = ["rm", "del", "format", "mkfs", ":(){", "sudo"]
        is_dangerous = any(cmd in command.lower() for cmd in danger_commands)
        
        if is_dangerous:
            console.print(Panel(
                f"[bold red]PERINGATAN:[/bold red] Perintah {command} berpotensi berbahaya.\n"
                "Apakah Anda yakin ingin menjalankannya?",
                border_style="red"
            ))
            
            confirm = Prompt.ask("[bold red]Lanjutkan (y/n)[/bold red]", choices=["y", "n"], default="n")
            if confirm.lower() != "y":
                console.print("[bold yellow]Eksekusi perintah dibatalkan.[/bold yellow]")
                return
        
        # Jalankan perintah dengan tampilan yang lebih baik
        console.print(Panel(
            f"Menjalankan perintah:\n[bold yellow]{command}[/bold yellow]",
            border_style="magenta",
            expand=False,
            width=get_width(70)
        ))
        
        console.print("[bold blue]Output:[/bold blue]")
        os.system(command)
        # console.print("\n[bold green]Perintah selesai dieksekusi[/bold green]")

def handle_command(input_text):
    """Tangani perintah khusus aplikasi."""
    if input_text.lower() == "exit":
        console.print("[bold green]Terima kasih telah menggunakan Groq AI Assistant![/bold green]")
        sys.exit(0)
    elif input_text.lower() == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
        show_banner()
        return True
    elif input_text.lower() == "help":
        display_help()
        return True
    elif input_text.lower() == "info":
        show_banner()
        return True
    elif input_text.lower() == "model":
        display_model_info()
        return True
    return False

def format_response(response):
    """Format respons AI dengan tampilan yang lebih baik."""
    # Hapus tag command jika ada untuk menampilkan secara terpisah
    cleaned_response = re.sub(r"<command>.*?</command>", "", response, flags=re.DOTALL).strip()
    
    # Coba render sebagai markdown jika memungkinkan
    try:
        return Markdown(cleaned_response)
    except:
        return cleaned_response

def main():
    """Fungsi utama aplikasi."""
    if not setup():
        console.print("[bold red]Gagal menginisialisasi aplikasi. Keluar...[/bold red]")
        return
    
    history = []
    history_index = 0
    
    while True:
        try:
            # Prompt user dengan styling yang lebih baik
            userPrompt = Prompt.ask("\n[bold cyan]❯[/bold cyan] [bold white]", 
                                  default="", 
                                  show_default=False)
            
            # Tangani perintah khusus aplikasi
            if handle_command(userPrompt):
                continue
            
            # Tambahkan ke history
            history.append(userPrompt)
            history_index = len(history)
            
            # Dapatkan respons dari Groq
            response = groq_service(userPrompt)
            
            # Tampilkan respons dengan format yang lebih baik
            console.rule("[bold green]AI Response[/bold green]")
            formatted_response = format_response(response)
            console.print(Panel(
                formatted_response, 
                width=get_width(100), 
                border_style="green", 
                title="🤖 Groq AI", 
                title_align="left"
            ))
            
            # Jalankan perintah jika ada
            execute_if_command_present(response)
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Keluar dengan Ctrl+C[/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")

if __name__ == "__main__":
    main()