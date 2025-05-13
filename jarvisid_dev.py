"""
Halo! Ini adalah AI Assistant yang bisa bantu kamu ngoding dan manajemen file.
Dibuat pake Groq API dan library Rich buat tampilan yang keren di terminal.

Fitur-fitur yang ada:
- Bikin dan edit file/folder
- Jalanin perintah sistem
- Tampilan yang keren pake Rich
- Support banyak bahasa termasuk Indonesia
- Bisa bantu coding dan debugging

Cara pakenya:
1. Ketik perintah yang kamu mau (misal: 'bikin web', 'edit file', dll)
2. AI bakal ngerti dan langsung eksekusi
3. Kalo bingung, ketik 'help' buat liat perintah yang ada

Library yang dipake:
- rich: Buat bikin tampilan terminal yang keren
- groq: Buat koneksi ke AI model
- os: Buat operasi sistem
- re: Buat pattern matching
- time: Buat delay dan timing
- sys: Buat sistem operasi
- shutil: Buat operasi file
- datetime: Buat format tanggal dan waktu

Tips:
- Pake Ctrl+C kalo mau keluar
- Ketik 'clear' buat bersihin layar
- Ketik 'help' kalo bingung
"""

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
API_KEY = "YOUR_GROQ_API_KEY_HERE"

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
    
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██████╗ ██████╗  ██████╗  ██████╗      █████╗ ██╗           ║
    ║  ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝    ██║  ██║██║           ║
    ║  ██╔════╝ ██╔══██╗██╔═══██╗██╔═══██╗    ██╔══██╗██║           ║
    ║  ██║  ███╗██████╔╝██║   ██║██║   ██║    ███████║██║           ║
    ║  ██║   ██║██╔══██╗██║   ██║██║▄▄ ██║    ██╔══██║██║           ║
    ║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══▀▀═╝     ╚═╝  ╚═╝╚═╝           ║
    ║                                                               ║
    ║             Terminal Assistant - Llama 3.3 70B                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    
    today = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    table = Table(box=box.ROUNDED, expand=False, width=width)
    table.add_column("Info", style="cyan")
    table.add_column("Detail", style="green")
    
    table.add_row("Dibuat Oleh", "Chandra")
    table.add_row("GitHub", "https://github.com/FANNYMU")
    table.add_row("WhatsApp", "08819538083")
    table.add_row("Model", "llama-3.3-70b-versatile")
    table.add_row("Versi", "1.0.0")
    table.add_row("Tanggal", today)
    
    console.print(Text(banner, style="bold blue"))
    console.print(table)
    console.print("\n[bold yellow]Ketik 'help' buat liat perintah yang ada, atau langsung aja tanya apa yang kamu butuhin![/bold yellow]\n")

def get_width(max_width=80, margin=10):
    """Ambil lebar terminal responsif dengan batas maksimum."""
    terminal_width = get_terminal_size((80, 20)).columns
    return min(max_width, terminal_width - margin)

def display_help():
    """Tampilkan informasi bantuan."""
    help_table = Table(title="Perintah yang Bisa Dipake", box=box.ROUNDED, title_style="bold magenta")
    help_table.add_column("Perintah", style="cyan")
    help_table.add_column("Fungsinya", style="green")
    
    help_table.add_row("help", "Liat daftar perintah yang ada")
    help_table.add_row("clear", "Bersihin layar terminal")
    help_table.add_row("exit", "Keluar dari program")
    help_table.add_row("info", "Liat info program")
    help_table.add_row("model", "Liat info model AI yang dipake")
    help_table.add_row("<prompt>", "Tanya apa aja ke AI")
    
    console.print(help_table)

def display_model_info():
    """Tampilkan informasi tentang model."""
    model_info = Panel(
        "[bold]llama-3.3-70b-versatile[/bold]\n\n"
        "Model Llama 3.3 70B ini keren banget! Dia bisa ngerti dan ngejawab "
        "dalam berbagai bahasa. Dilatih pake data yang banyak banget, "
        "jadi pengetahuannya luas.\n\n"
        "[italic]Kenapa model ini keren:[/italic]\n"
        "• Lebih pinter dalam memahami konteks\n"
        "• Bisa pake bahasa Indonesia\n"
        "• Jago ngerjain tugas yang rumit\n"
        "• Punya pengetahuan yang luas",
        title="Info Model",
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
            
            # Cek apakah ada file yang disebutkan dalam prompt
            file_mention = re.search(r'edit file (\S+)', prompt, re.IGNORECASE)
            file_content = ""
            if file_mention:
                filename = file_mention.group(1)
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except:
                    file_content = "File tidak ditemukan"

            system_prompt = f"""Hai! Aku AI Assistant yang bisa bantu kamu:

1. Bikin folder:
<folder>nama_folder</folder>

2. Bikin file dengan isi:
<file>nama_file.extension|isi file di sini</file>

3. Edit file yang udah ada:
<edit>nama_file.extension|isi baru di sini</edit>

4. Liat isi folder:
<list>path</list>

PENTING! Kalo kamu diminta edit file:
- Aku akan SELALU mempertahankan struktur HTML yang udah ada
- Aku akan SELALU mempertahankan semua class dan styling yang udah ada
- Aku akan CUMA mengubah bagian yang diminta user
- Aku akan SELALU memberikan penjelasan perubahan yang aku lakukan

Kalo ada file yang mau diedit, ini isi filenya:
{file_content}

Aku selalu pake bahasa Indonesia yang santai dan format Markdown kalo perlu.
Aku juga bakal jelasin apa yang aku lakuin biar kamu paham!
"""
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=2000,
                temperature=0.7,
            )
            
            time.sleep(0.5)
            
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def create_file(filename: str, content: str = ""):
    """Membuat file baru dengan konten yang diberikan."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        console.print(f"[bold green]Berhasil membuat file: {filename}[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saat membuat file: {str(e)}[/bold red]")
        return False

def create_folder(foldername: str):
    """Membuat folder baru."""
    try:
        os.makedirs(foldername, exist_ok=True)
        console.print(f"[bold green]Berhasil membuat folder: {foldername}[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saat membuat folder: {str(e)}[/bold red]")
        return False

def edit_file_content(filename: str, new_content: str):
    """Mengedit konten file yang sudah ada."""
    try:
        if not os.path.exists(filename):
            console.print(f"[bold red]File tidak ditemukan: {filename}[/bold red]")
            return False
        
        # Baca konten file yang ada
        original_content = ""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except:
            pass
        
        # Jika file HTML dan sudah ada kontennya, pertahankan struktur
        if filename.endswith('.html') and original_content and '<!DOCTYPE html>' in original_content:
            # Parse konten original untuk mendapatkan struktur
            match = re.search(r'<body[^>]*>(.*?)</body>', original_content, re.DOTALL)
            if match and '<body' in new_content:
                # Ambil atribut body dari konten baru jika ada
                new_body_match = re.search(r'<body([^>]*)>', new_content)
                body_attrs = new_body_match.group(1) if new_body_match else ''
                
                # Gabungkan atribut body yang ada dengan yang baru
                original_body_match = re.search(r'<body([^>]*)>', original_content)
                original_attrs = original_body_match.group(1) if original_body_match else ''
                
                # Gabungkan atribut, hilangkan duplikat
                all_attrs = ' '.join(set((original_attrs + ' ' + body_attrs).split()))
                
                # Ganti konten dalam body saja
                new_body_content = re.search(r'<body[^>]*>(.*?)</body>', new_content, re.DOTALL)
                if new_body_content:
                    modified_content = re.sub(
                        r'<body[^>]*>.*?</body>',
                        f'<body {all_attrs}>{new_body_content.group(1)}</body>',
                        original_content,
                        flags=re.DOTALL
                    )
                    new_content = modified_content
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        console.print(f"[bold green]Berhasil mengedit file: {filename}[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saat mengedit file: {str(e)}[/bold red]")
        return False

def read_file_content(filename: str):
    """Membaca konten dari file."""
    try:
        if not os.path.exists(filename):
            console.print(f"[bold red]File tidak ditemukan: {filename}[/bold red]")
            return None
            
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        console.print(f"[bold red]Error saat membaca file: {str(e)}[/bold red]")
        return None

def list_directory(path: str = "."):
    """Menampilkan isi direktori."""
    try:
        items = os.listdir(path)
        
        # Buat tabel untuk menampilkan hasil
        table = Table(title=f"Isi Direktori: {path}", box=box.ROUNDED)
        table.add_column("Nama", style="cyan")
        table.add_column("Tipe", style="magenta")
        table.add_column("Ukuran", style="green")
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                table.add_row(item, "File", f"{size:,} bytes")
            else:
                table.add_row(item, "Folder", "-")
        
        console.print(table)
        return True
    except Exception as e:
        console.print(f"[bold red]Error saat membaca direktori: {str(e)}[/bold red]")
        return False

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

def process_ai_response(response: str):
    folder_matches = re.finditer(r"<folder>(.*?)</folder>", response)
    for match in folder_matches:
        foldername = match.group(1).strip()
        create_folder(foldername)
    
    file_matches = re.finditer(r"<file>(.*?)\|(.*?)</file>", response, re.DOTALL)
    for match in file_matches:
        filename, content = match.groups()
        directory = os.path.dirname(filename.strip())
        if directory and not os.path.exists(directory):
            create_folder(directory)
        create_file(filename.strip(), content.strip())
    
    edit_matches = re.finditer(r"<edit>(.*?)\|(.*?)</edit>", response, re.DOTALL)
    for match in edit_matches:
        filename, new_content = match.groups()
        edit_file_content(filename.strip(), new_content.strip())
    
    list_matches = re.finditer(r"<list>(.*?)</list>", response)
    for match in list_matches:
        path = match.group(1).strip()
        list_directory(path)
    
    execute_if_command_present(response)

def format_response(response):
    process_ai_response(response)
    
    cleaned_response = re.sub(r"<(file|folder|edit|list|command)>.*?</\1>", "", response, flags=re.DOTALL).strip()
    
    try:
        return Markdown(cleaned_response)
    except:
        return cleaned_response

def main():
    if not setup():
        console.print("[bold red]Waduh, ada masalah nih pas setup. Program harus berhenti...[/bold red]")
        return
    
    history = []
    history_index = 0
    
    while True:
        try:
            userPrompt = Prompt.ask("\n[bold cyan]❯[/bold cyan] [bold white]", 
                                  default="", 
                                  show_default=False)
            
            if handle_command(userPrompt):
                continue
            
            history.append(userPrompt)
            history_index = len(history)
            
            response = groq_service(userPrompt)
            
            console.rule("[bold green]Jawaban AI[/bold green]")
            formatted_response = format_response(response)
            console.print(Panel(
                formatted_response, 
                width=get_width(100), 
                border_style="green", 
                title="🤖 Groq AI", 
                title_align="left"
            ))
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Dadah! Makasih udah pake program ini ya![/bold yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Ups, error nih: {str(e)}[/bold red]")

if __name__ == "__main__":
    main()