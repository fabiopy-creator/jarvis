import customtkinter as ctk
from datetime import datetime
import webbrowser
import psutil
import subprocess
import os
import shutil
import sqlite3
import threading
from pathlib import Path

# ── pip install anthropic
try:
    import anthropic
    IA_DISPONIVEL = True
except ImportError:
    IA_DISPONIVEL = False

# ══════════════════════════════════════════════════════════
#  PALETA: MONOCROMÁTICA MELANCÓLICA (HOLLOW / THE VOID)
# ══════════════════════════════════════════════════════════
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

ctk.set_appearance_mode("dark")

# Tons do Abismo
COR_FUNDO        = "#030304"  # Escuridão quase absoluta
COR_PAINEL       = "#0A0A0C"  # Painel carvão profundo
COR_BORDA        = "#1F1F24"  # Linhas finas
COR_BRANCO_OSSO  = "#D8D8D8"  # Branco pálido/osso
COR_TEXTO_MUTED  = "#4A4A52"  # Cinza opaco

FONTE_MONO       = ("Consolas", 12)
FONTE_MONO_BOLD  = ("Consolas", 12, "bold")
FONTE_TITULO     = ("Consolas", 18, "bold")

# ══════════════════════════════════════════════════════════
#  BANCO DE DADOS — HISTÓRICO
# ══════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect("jarvis_historico.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            usuario   TEXT,
            jarvis    TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_historico(usuario, jarvis):
    conn = sqlite3.connect("jarvis_historico.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO historico (timestamp, usuario, jarvis) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usuario, jarvis)
    )
    conn.commit()
    conn.close()

def buscar_historico(limite=10):
    conn = sqlite3.connect("jarvis_historico.db")
    c = conn.cursor()
    c.execute("SELECT timestamp, usuario, jarvis FROM historico ORDER BY id DESC LIMIT ?", (limite,))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ══════════════════════════════════════════════════════════
#  INTERFACE (CANTOS RETOS = 0 / RETRÔ GÓTICO)
# ══════════════════════════════════════════════════════════
app = ctk.CTk()
app.configure(fg_color=COR_FUNDO)
app.title("JARVIS-X // VOID")
app.geometry("1300x750")
app.minsize(1000, 600)

# Layout de colunas sem arredondamento
col_esq = ctk.CTkFrame(app, width=280, corner_radius=0, fg_color=COR_PAINEL, border_width=1, border_color=COR_BORDA)
col_esq.pack(side="left", fill="y")
col_esq.pack_propagate(False)

col_dir = ctk.CTkFrame(app, corner_radius=0, fg_color=COR_FUNDO)
col_dir.pack(side="left", fill="both", expand=True)

# ══════════════════════════════════════════════════════════
#  PAINEL LATERAL (CPU, RAM, DISK SIMPLIFICADOS)
# ══════════════════════════════════════════════════════════
avatar = ctk.CTkLabel(col_esq, text="🕱", font=("Consolas", 38), text_color=COR_BRANCO_OSSO)
avatar.pack(pady=(35, 0))

nome_ia = ctk.CTkLabel(col_esq, text="JARVIS-X", font=FONTE_TITULO, text_color=COR_BRANCO_OSSO)
nome_ia.pack(pady=(0, 2))

sub_ia = ctk.CTkLabel(col_esq, text="...no voice to cry suffering", font=("Consolas", 10, "italic"), text_color=COR_TEXTO_MUTED)
sub_ia.pack(pady=(0, 35))

# Status simplificados
cpu_title = ctk.CTkLabel(col_esq, text="CPU", font=FONTE_MONO_BOLD, text_color=COR_BRANCO_OSSO, anchor="w")
cpu_title.pack(padx=25, fill="x")
cpu_label = ctk.CTkLabel(col_esq, text="🖤 0%", font=FONTE_MONO, text_color=COR_TEXTO_MUTED, anchor="w")
cpu_label.pack(padx=25, pady=(0, 20), fill="x")

ram_title = ctk.CTkLabel(col_esq, text="RAM", font=FONTE_MONO_BOLD, text_color=COR_BRANCO_OSSO, anchor="w")
ram_title.pack(padx=25, fill="x")
ram_label = ctk.CTkLabel(col_esq, text="🖤 0%", font=FONTE_MONO, text_color=COR_TEXTO_MUTED, anchor="w")
ram_label.pack(padx=25, pady=(0, 20), fill="x")

disk_title = ctk.CTkLabel(col_esq, text="DISK", font=FONTE_MONO_BOLD, text_color=COR_BRANCO_OSSO, anchor="w")
disk_title.pack(padx=25, fill="x")
disk_label = ctk.CTkLabel(col_esq, text="🖤 0%", font=FONTE_MONO, text_color=COR_TEXTO_MUTED, anchor="w")
disk_label.pack(padx=25, pady=(0, 20), fill="x")

# Linha divisória fina
sep = ctk.CTkFrame(col_esq, height=1, fg_color=COR_BORDA)
sep.pack(fill="x", padx=25, pady=10)

status_txt = ctk.CTkLabel(col_esq, text="● RESTING AT BENCH", font=FONTE_MONO, text_color=COR_TEXTO_MUTED)
status_txt.pack(pady=10)

# ══════════════════════════════════════════════════════════
#  TERMINAL
# ══════════════════════════════════════════════════════════
topo = ctk.CTkFrame(col_dir, fg_color="transparent")
topo.pack(fill="x", padx=30, pady=(25, 0))

titulo = ctk.CTkLabel(topo, text="JARVIS ESTÁ A SEU DISPOR", font=FONTE_TITULO, text_color=COR_BRANCO_OSSO)
titulo.pack(side="left")

relogio = ctk.CTkLabel(topo, text="", font=FONTE_MONO, text_color=COR_TEXTO_MUTED)
relogio.pack(side="right")

saida = ctk.CTkTextbox(
    col_dir,
    font=FONTE_MONO,
    border_width=1,
    border_color=COR_BORDA,
    fg_color="#020202",
    text_color=COR_BRANCO_OSSO,
    corner_radius=0,
    wrap="word"
)
saida.pack(pady=20, padx=30, fill="both", expand=True)

saida.insert("end", "> O ar está calmo e em silêncio...\n")
saida.insert("end", "> Aguardando suas ordens.\n\n")

# Entrada minimalista
linha_entrada = ctk.CTkFrame(col_dir, fg_color="transparent")
linha_entrada.pack(fill="x", padx=30, pady=(0, 25))

entrada = ctk.CTkEntry(
    linha_entrada,
    height=45,
    font=FONTE_MONO,
    border_width=1,
    border_color=COR_BORDA,
    fg_color="#060608",
    text_color=COR_BRANCO_OSSO,
    corner_radius=0,
    placeholder_text="Digite seu comando..."
)
entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))

botao = ctk.CTkButton(
    linha_entrada,
    text="FOCUS 🕱",
    width=120,
    height=45,
    font=FONTE_MONO_BOLD,
    fg_color=COR_BRANCO_OSSO,
    hover_color="#A8A8A8",
    text_color="#000000",
    corner_radius=0,
    command=lambda: executar()
)
botao.pack(side="left")

# ══════════════════════════════════════════════════════════
#  LÓGICA E REFRESH
# ══════════════════════════════════════════════════════════
def atualizar_relogio():
    relogio.configure(text=datetime.now().strftime("%H:%M:%S"))
    app.after(1000, atualizar_relogio)

def atualizar_sistema():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent
    
    cpu_label.configure(text=f"🖤 {cpu}%")
    ram_label.configure(text=f"🖤 {ram}%")
    disk_label.configure(text=f"🖤 {disco}%")
    
    app.after(2000, atualizar_sistema)

atualizar_relogio()
atualizar_sistema()

def responder(texto):
    saida.insert("end", f"{texto}\n")
    saida.see("end")

def organizar_downloads():
    path_downloads = Path.home() / "Downloads"
    
    categorias = {
        "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
        "Vídeos": [".mp4", ".mkv", ".avi", ".mov"],
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
        "Programas": [".exe", ".msi"],
        "Código": [".py", ".html", ".css", ".js", ".json"],
        "Compactados": [".zip", ".rar", ".7z"]
    }
    
    arquivos_movidos = 0
    
    for item in path_downloads.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            for pasta, extensoes in categorias.items():
                if ext in extensoes:
                    pasta_destino = path_downloads / pasta
                    pasta_destino.mkdir(exist_ok=True)
                    try:
                        shutil.move(str(item), str(pasta_destino / item.name))
                        arquivos_movidos += 1
                    except Exception:
                        pass
                    break

    responder(f"[JARVIS] Downloads organizados. {arquivos_movidos} arquivos movidos.")

def perguntar_ia(pergunta):
    if not IA_DISPONIVEL:
        return "[JARVIS] 'anthropic' não encontrada no sistema."
    if not ANTHROPIC_API_KEY:
        return "[JARVIS] Nenhuma chave API configurada."
    try:
        cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        msg = cliente.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=600,
            system=(
                "Você é o JARVIS. Responda de forma solene, respeitosa, levemente melancólica e direta, "
                "inspirado no estilo de Hollow Knight. Respostas contidas e sem exageros em português do Brasil."
            ),
            messages=[{"role": "user", "content": pergunta}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"[ERRO] {str(e)}"

def perguntar_ia_async(pergunta):
    responder("[JARVIS] Processando...")
    def _tarefa():
        resposta = perguntar_ia(pergunta)
        def atualizar_ui():
            saida.insert("end", f"[JARVIS] {resposta}\n")
            saida.see("end")
            salvar_historico(pergunta, resposta)
        app.after(0, atualizar_ui)
    threading.Thread(target=_tarefa, daemon=True).start()

PROGRAMAS_WINDOWS = {
    "abrir notepad": "notepad.exe", "abrir calc": "calc.exe", 
    "abrir explorer": "explorer.exe", "abrir cmd": "cmd.exe"
}

SITES = {
    "abrir google": "https://www.google.com", "abrir youtube": "https://www.youtube.com",
    "abrir github": "https://github.com"
}

def executar():
    comando = entrada.get().strip()
    cmd_low = comando.lower()
    entrada.delete(0, "end")

    if not comando:
        return

    saida.insert("end", f"> {comando}\n")

    if cmd_low in ("organizar downloads", "organizar pasta downloads"):
        organizar_downloads()
    elif cmd_low in SITES:
        webbrowser.open(SITES[cmd_low])
        responder(f"[JARVIS] Abrindo: {cmd_low.replace('abrir ', '')}")
    elif cmd_low in PROGRAMAS_WINDOWS:
        try:
            subprocess.Popen(PROGRAMAS_WINDOWS[cmd_low])
            responder(f"[JARVIS] Iniciando: {cmd_low.replace('abrir ', '')}")
        except FileNotFoundError:
            responder("[JARVIS] Aplicação não encontrada.")
    elif cmd_low in ("limpar", "cls", "clear"):
        saida.delete("1.0", "end")
    else:
        perguntar_ia_async(comando)

entrada.bind("<Return>", lambda e: executar())

app.mainloop()
