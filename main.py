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

# ── pip install anthropic  (necessário para IA conversacional)
try:
    import anthropic
    IA_DISPONIVEL = True
except ImportError:
    IA_DISPONIVEL = False

# ══════════════════════════════════════════════════════════
#  CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════
ANTHROPIC_API_KEY = "sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXX"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COR_FUNDO    = "#0A0F1C"
COR_PAINEL   = "#111827"
COR_DESTAQUE = "#00D4FF"
COR_TEXTO    = "#E5E7EB"

# ══════════════════════════════════════════════════════════
#  BANCO DE DADOS — HISTÓRICO SQLite
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
    c.execute(
        "SELECT timestamp, usuario, jarvis FROM historico ORDER BY id DESC LIMIT ?",
        (limite,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ══════════════════════════════════════════════════════════
#  JANELA PRINCIPAL
# ══════════════════════════════════════════════════════════
app = ctk.CTk()
app.configure(fg_color=COR_FUNDO)
app.title("JARVIS-X")
app.geometry("1400x800")
app.minsize(1100, 650)

# ══════════════════════════════════════════════════════════
#  LAYOUT — DUAS COLUNAS
# ══════════════════════════════════════════════════════════
col_esq = ctk.CTkFrame(app, width=280, corner_radius=0, fg_color=COR_PAINEL)
col_esq.pack(side="left", fill="y")
col_esq.pack_propagate(False)

col_dir = ctk.CTkFrame(app, corner_radius=0, fg_color=COR_FUNDO)
col_dir.pack(side="left", fill="both", expand=True)

# ══════════════════════════════════════════════════════════
#  COLUNA ESQUERDA — AVATAR + STATUS
# ══════════════════════════════════════════════════════════
avatar = ctk.CTkLabel(
    col_esq,
    text="◉",
    font=("Arial", 70),
    text_color=COR_DESTAQUE
)
avatar.pack(pady=(25, 5))

nome_ia = ctk.CTkLabel(
    col_esq,
    text="JARVIS-X",
    font=("Consolas", 18, "bold"),
    text_color=COR_DESTAQUE
)
nome_ia.pack()

separador = ctk.CTkLabel(
    col_esq,
    text="─" * 22,
    font=("Consolas", 12),
    text_color="#2A3A4A"
)
separador.pack(pady=(10, 0))

status_titulo = ctk.CTkLabel(
    col_esq,
    text="SYSTEM STATUS",
    font=("Consolas", 18, "bold"),
    text_color=COR_DESTAQUE
)
status_titulo.pack(pady=(10, 10))

# CPU
cpu_frame = ctk.CTkFrame(col_esq, fg_color="#1A2333")
cpu_frame.pack(padx=15, pady=8, fill="x")
cpu_label = ctk.CTkLabel(cpu_frame, text="CPU: --%", font=("Consolas", 16))
cpu_label.pack(pady=(10, 5))
cpu_bar = ctk.CTkProgressBar(cpu_frame, width=200, progress_color=COR_DESTAQUE)
cpu_bar.set(0)
cpu_bar.pack(pady=(0, 10))

# RAM
ram_frame = ctk.CTkFrame(col_esq, fg_color="#1A2333")
ram_frame.pack(padx=15, pady=8, fill="x")
ram_label = ctk.CTkLabel(ram_frame, text="RAM: --%", font=("Consolas", 16))
ram_label.pack(pady=(10, 5))
ram_bar = ctk.CTkProgressBar(ram_frame, width=200, progress_color="#00FF9F")
ram_bar.set(0)
ram_bar.pack(pady=(0, 10))

# DISK
disk_frame = ctk.CTkFrame(col_esq, fg_color="#1A2333")
disk_frame.pack(padx=15, pady=8, fill="x")
disk_label = ctk.CTkLabel(disk_frame, text="DISK: --%", font=("Consolas", 16))
disk_label.pack(pady=(10, 5))
disk_bar = ctk.CTkProgressBar(disk_frame, width=200, progress_color="#FF6B35")
disk_bar.set(0)
disk_bar.pack(pady=(0, 10))

hora_sidebar = ctk.CTkLabel(
    col_esq,
    text="● ONLINE",
    font=("Consolas", 14),
    text_color="#00FF9F"
)
hora_sidebar.pack(pady=20)

# ══════════════════════════════════════════════════════════
#  COLUNA DIREITA — TERMINAL
# ══════════════════════════════════════════════════════════
topo = ctk.CTkFrame(col_dir, fg_color="transparent")
topo.pack(fill="x", padx=20, pady=(15, 0))

titulo = ctk.CTkLabel(
    topo,
    text="JARVIS",
    font=("Consolas", 48, "bold"),
    text_color=COR_DESTAQUE
)
titulo.pack(side="left")

relogio = ctk.CTkLabel(
    topo,
    text="",
    font=("Consolas", 20),
    text_color="#8FA3BF"
)
relogio.pack(side="right", pady=10)

subtitulo = ctk.CTkLabel(
    col_dir,
    text="Artificial Intelligence Operating System",
    font=("Consolas", 14),
    text_color="#8FA3BF"
)
subtitulo.pack(padx=20, anchor="w")

# Terminal de saída
saida = ctk.CTkTextbox(
    col_dir,
    font=("Consolas", 16),
    border_width=2,
    border_color=COR_DESTAQUE,
    corner_radius=12,
    wrap="word"
)
saida.pack(pady=(12, 8), padx=20, fill="both", expand=True)

saida.insert("end", "[JARVIS] Sistema inicializado.\n")
saida.insert("end", "[JARVIS] Monitoramento ativo.\n")
saida.insert("end", "[JARVIS] Aguardando comandos...\n\n")

# Linha de entrada + botão
linha_entrada = ctk.CTkFrame(col_dir, fg_color="transparent")
linha_entrada.pack(fill="x", padx=20, pady=(0, 8))

entrada = ctk.CTkEntry(
    linha_entrada,
    height=50,
    font=("Consolas", 17),
    border_width=2,
    border_color=COR_DESTAQUE,
    corner_radius=12,
    placeholder_text="Digite um comando ou uma pergunta..."
)
entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))

botao = ctk.CTkButton(
    linha_entrada,
    text="EXECUTAR",
    width=160,
    height=50,
    font=("Consolas", 16, "bold"),
    fg_color=COR_DESTAQUE,
    text_color="black",
    corner_radius=12,
    command=lambda: executar()
)
botao.pack(side="left")

# Rodapé de ajuda
ajuda = ctk.CTkLabel(
    col_dir,
    text="comandos: abrir [site/app]  •  criar pasta [nome]  •  organizar downloads  •  status  •  historico",
    font=("Consolas", 11),
    text_color="#3A5068"
)
ajuda.pack(pady=(0, 10))

# ══════════════════════════════════════════════════════════
#  RELÓGIO
# ══════════════════════════════════════════════════════════
def atualizar_relogio():
    agora = datetime.now()
    relogio.configure(text=agora.strftime("%H:%M:%S"))
    app.after(1000, atualizar_relogio)

atualizar_relogio()

# ══════════════════════════════════════════════════════════
#  MONITORAMENTO DO SISTEMA
# ══════════════════════════════════════════════════════════
def atualizar_sistema():
    cpu   = psutil.cpu_percent()
    ram   = psutil.virtual_memory().percent
    disco = psutil.disk_usage("/").percent
    cpu_label.configure(
        text=f"CPU: {cpu}%"
    )
    ram_label.configure(
        text=f"RAM: {ram}%"
    )
    disk_label.configure(
        text=f"DISK: {disco}%"
    )
    cpu_bar.set(cpu / 100)
    ram_bar.set(ram / 100)
    disk_bar.set(disco / 100)
    app.after(
        1000,
        atualizar_sistema
    )

atualizar_sistema()

# ══════════════════════════════════════════════════════════
#  UTILITÁRIOS
# ══════════════════════════════════════════════════════════
def responder(texto):
    saida.insert("end", f"{texto}\n")
    saida.see("end")

def organizar_downloads():
    pasta = str(Path.home() / "Downloads")
    categorias = {
        "Imagens":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Videos":      [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Musicas":     [".mp3", ".wav", ".flac", ".aac", ".ogg"],
        "Documentos":  [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt"],
        "Programas":   [".exe", ".msi"],
        "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Codigo":      [".py", ".js", ".html", ".css", ".json", ".xml"],
    }
    movidos = 0
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            ext = os.path.splitext(arquivo)[1].lower()
            for categoria, extensoes in categorias.items():
                if ext in extensoes:
                    destino = os.path.join(pasta, categoria)
                    os.makedirs(destino, exist_ok=True)
                    shutil.move(caminho, os.path.join(destino, arquivo))
                    movidos += 1
                    break
    return movidos

# ══════════════════════════════════════════════════════════
#  IA CONVERSACIONAL — Anthropic Claude
# ══════════════════════════════════════════════════════════
def perguntar_ia(pergunta):
    if not IA_DISPONIVEL:
        return "[JARVIS] Biblioteca 'anthropic' não instalada. Execute: pip install anthropic"
    if ANTHROPIC_API_KEY == "SUA_CHAVE_AQUI":
        return "[JARVIS] Configure sua ANTHROPIC_API_KEY no topo do arquivo ou como variável de ambiente."
    try:
        cliente = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        msg = cliente.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=(
                "Você é JARVIS, uma IA assistente pessoal integrada a um sistema operacional. "
                "Responda de forma direta, inteligente e em português do Brasil. "
                "Seja conciso e útil."
            ),
            messages=[{"role": "user", "content": pergunta}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"[ERRO IA] {str(e)}"

def perguntar_ia_async(pergunta):
    """Chama a IA em thread separada para não travar a interface."""
    responder("[JARVIS] Consultando IA...")
    app.update()

    def _tarefa():
        resposta = perguntar_ia(pergunta)
        saida.insert("end", f"[JARVIS] {resposta}\n")
        saida.see("end")
        salvar_historico(pergunta, resposta)

    threading.Thread(target=_tarefa, daemon=True).start()

# ══════════════════════════════════════════════════════════
#  COMANDO PRINCIPAL
# ══════════════════════════════════════════════════════════
PROGRAMAS_WINDOWS = {
    "abrir notepad":   "notepad.exe",
    "abrir calc":      "calc.exe",
    "abrir explorer":  "explorer.exe",
    "abrir paint":     "mspaint.exe",
    "abrir cmd":       "cmd.exe",
    "abrir taskmgr":   "taskmgr.exe",
    "abrir word":      "winword.exe",
    "abrir excel":     "excel.exe",
    "abrir powerpoint":"powerpnt.exe",
}

SITES = {
    "abrir google":   "https://www.google.com",
    "abrir youtube":  "https://www.youtube.com",
    "abrir github":   "https://github.com",
    "abrir chatgpt":  "https://chatgpt.com",
    "abrir spotify":  "https://open.spotify.com",
    "abrir claude":   "https://claude.ai",
    "abrir gmail":    "https://mail.google.com",
    "abrir linkedin": "https://www.linkedin.com",
}

def executar():
    comando  = entrada.get().strip()
    cmd_low  = comando.lower()
    resposta = None

    saida.insert("end", f"\n[USUÁRIO] > {comando}\n")
    entrada.delete(0, "end")

    # ── Sites ──────────────────────────────────────────────
    if cmd_low in SITES:
        webbrowser.open(SITES[cmd_low])
        nome = cmd_low.replace("abrir ", "").capitalize()
        resposta = f"[JARVIS] {nome} aberto com sucesso."

    # ── Programas Windows ──────────────────────────────────
    elif cmd_low in PROGRAMAS_WINDOWS:
        try:
            subprocess.Popen(PROGRAMAS_WINDOWS[cmd_low])
            nome = cmd_low.replace("abrir ", "").capitalize()
            resposta = f"[JARVIS] {nome} aberto com sucesso."
        except FileNotFoundError:
            resposta = f"[JARVIS] Programa não encontrado neste sistema."

    # ── Criar pasta ────────────────────────────────────────
    elif cmd_low.startswith("criar pasta "):
        nome_pasta = comando[12:].strip()
        if nome_pasta:
            caminho = os.path.join(os.getcwd(), nome_pasta)
            os.makedirs(caminho, exist_ok=True)
            resposta = f"[JARVIS] Pasta '{nome_pasta}' criada em {caminho}"
        else:
            resposta = "[JARVIS] Informe o nome da pasta. Ex: criar pasta Projetos"

    # ── Organizar Downloads ────────────────────────────────
    elif cmd_low == "organizar downloads":
        responder("[JARVIS] Organizando Downloads...")
        app.update()
        try:
            movidos = organizar_downloads()
            resposta = f"[JARVIS] Downloads organizado. {movidos} arquivo(s) movido(s)."
        except Exception as e:
            resposta = f"[JARVIS] Erro ao organizar: {e}"

    # ── Status ─────────────────────────────────────────────
    elif cmd_low == "status":
        cpu   = psutil.cpu_percent()
        ram   = psutil.virtual_memory().percent
        disco = psutil.disk_usage("/").percent
        saida.insert("end", "\n[JARVIS] STATUS DO SISTEMA\n\n")
        saida.insert("end", f"CPU:    {cpu}%\n")
        saida.insert("end", f"RAM:    {ram}%\n")
        saida.insert("end", f"DISCO:  {disco}%\n\n")
        resposta = "STATUS: ONLINE"

    # ── Histórico ──────────────────────────────────────────
    elif cmd_low == "historico":
        rows = buscar_historico(10)
        saida.insert("end", "\n[JARVIS] ÚLTIMOS 10 COMANDOS:\n\n")
        for row in rows:
            saida.insert("end", f"  [{row[0]}] {row[1]}\n")
            saida.insert("end", f"           → {row[2]}\n")
        saida.insert("end", "\n")
        resposta = None  # já imprimiu tudo acima

    # ── Limpar terminal ────────────────────────────────────
    elif cmd_low in ("limpar", "cls", "clear"):
        saida.delete("1.0", "end")
        saida.insert("end", "[JARVIS] Terminal limpo.\n\n")
        resposta = None

    # ── IA Conversacional ──────────────────────────────────
    else:
        perguntar_ia_async(comando)
        salvar_historico(comando, "(resposta IA em processamento)")
        return  # já salva dentro da thread

    if resposta:
        responder(resposta)

    salvar_historico(comando, resposta or "(sem resposta de texto)")

# Tecla Enter executa
entrada.bind("<Return>", lambda e: executar())

# ══════════════════════════════════════════════════════════
app.mainloop()