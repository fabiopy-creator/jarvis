# 🤖 JARVIS-X

# <img src="https://raw.githubusercontent.com/fabiopy-creator/jarvis/main/assets/bot.png" width="50px"> JARVIS-X

<p align="center">
  <img src="Captura de tela 2026-06-04 182226" alt="Interface do JARVIS-X" width="800px">
</p>
Um assistente pessoal desenvolvido em Python com interface gráfica moderna usando CustomTkinter.
... (resto do seu README) ...

Um assistente pessoal desenvolvido em Python com interface gráfica moderna usando CustomTkinter.

O objetivo do projeto é simular um sistema operacional assistido por IA, oferecendo monitoramento do computador em tempo real, automação de tarefas e integração com inteligência artificial.

---

## 🔗 Repositório

https://github.com/fabiopy-creator/jarvis

---

## ✨ Funcionalidades

### 🖥️ Monitoramento do Sistema
- Uso de CPU em tempo real
- Uso de RAM em tempo real
- Uso de Disco em tempo real
- Relógio integrado

### 🌐 Automação Web
- Abrir Google
- Abrir YouTube
- Abrir GitHub
- Abrir ChatGPT
- Abrir Spotify
- Abrir Gmail
- Abrir LinkedIn
- Abrir Claude

### ⚙️ Automação do Windows
- Abrir Notepad
- Abrir Calculadora
- Abrir Explorer
- Abrir CMD
- Abrir Paint
- Abrir Gerenciador de Tarefas

### 📂 Organização de Arquivos
- Organiza automaticamente a pasta Downloads
- Separa arquivos por categoria:
  - Imagens
  - Vídeos
  - Documentos
  - Programas
  - Código
  - Compactados

### 🗃️ Histórico
- Armazenamento em SQLite
- Registro de comandos executados
- Consulta dos últimos comandos

### 🧠 Inteligência Artificial
- Integração com Anthropic Claude
- Respostas diretamente pela interface
- Execução assíncrona para não travar a aplicação

---

## 📸 Interface

O projeto possui uma interface inspirada em assistentes futuristas:

- Tema escuro
- Painel lateral de monitoramento
- Terminal integrado
- Status em tempo real
- Layout estilo JARVIS

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/fabiopy-creator/jarvis.git
```

### 2. Entre na pasta do projeto

```bash
cd jarvis
```

### 3. Instale as dependências

```bash
pip install customtkinter
pip install psutil
pip install anthropic
```

### 4. Execute o projeto

```bash
python main.py
```

---

## ⌨️ Comandos Disponíveis

### Abrir Sites

```text
abrir google
abrir youtube
abrir github
abrir chatgpt
abrir spotify
abrir gmail
abrir linkedin
abrir claude
```

### Abrir Programas

```text
abrir notepad
abrir calc
abrir explorer
abrir cmd
abrir paint
abrir taskmgr
abrir word
abrir excel
abrir powerpoint
```

### Utilidades

```text
status
historico
limpar
organizar downloads
criar pasta MeuProjeto
```

---

## 🔑 Configuração da IA

A funcionalidade de IA utiliza a API da Anthropic (Claude).

Por motivos de segurança, nenhuma chave de API é fornecida neste repositório.

Sem uma chave válida, o sistema continuará funcionando normalmente com:

✅ Interface gráfica  
✅ Monitoramento do sistema  
✅ Automação de sites  
✅ Automação do Windows  
✅ Organização de Downloads  
✅ Histórico SQLite  

A única funcionalidade indisponível será a conversa com IA.

Para habilitar a IA, substitua:

```python
ANTHROPIC_API_KEY = "SUA_CHAVE_AQUI"
```

por sua chave válida da Anthropic.

---

## 🛠️ Tecnologias Utilizadas

- Python
- CustomTkinter
- SQLite
- Psutil
- Anthropic API
- Threading

---

## 🎯 Objetivos do Projeto

Este projeto foi desenvolvido para praticar:

- Automação com Python
- Interfaces gráficas
- Banco de dados SQLite
- Integração com APIs
- Organização de código
- Desenvolvimento de aplicações desktop

---

## ⚠️ Aviso

Este projeto foi desenvolvido para fins de estudo e portfólio.

Algumas funcionalidades dependem de softwares instalados no Windows e da disponibilidade de uma chave válida da Anthropic.

---

## 📄 Licença

Este projeto é aberto para fins educacionais e aprendizado.
