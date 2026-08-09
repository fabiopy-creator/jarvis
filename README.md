# 🤖 JARVIS-X

## 🖼️ Demonstração do Sistema

![Interface do JARVIS-X](jarvis.png)

Um assistente pessoal desenvolvido em Python com interface gráfica moderna e minimalista usando CustomTkinter.

O objetivo do projeto é simular um sistema operacional assistido por IA, oferecendo monitoramento do computador em tempo real, automação de tarefas e suporte a inteligência artificial (mediante chave do usuário).

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

### 📂 Organização Dinâmica de Arquivos
- Função genérica `organizar_pasta()` aplicável a múltiplos diretórios
- Organiza automaticamente as pastas **Downloads** e **Área de Trabalho (Desktop)**
- Separa os arquivos por categoria criando subpastas:
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

### 🧠 Inteligência Artificial (Opcional)
- **Suporte para integração com Anthropic Claude (Requer API Key do próprio usuário)**
- Respostas personalizadas diretamente na interface gráfica
- Execução assíncrona (threading) para não travar a aplicação

---

## 📸 Interface

O projeto possui uma interface inspirada em uma estética monocromática e melancólica (Void / Hollow Knight):

- Tema escuro e minimalista em preto e branco osso
- Painel lateral de monitoramento direto (CPU, RAM, DISK)
- Terminal integrado limpo
- Status em tempo real
- Layout retilíneo sem cantos arredondados


🔑 Configuração da IA
A funcionalidade de IA utiliza a API da Anthropic (Claude).

Por motivos de segurança e custos, nenhuma chave de API é fornecida neste repositório.

Sem uma chave configurada, o assistente funcionará perfeitamente e 100% offline em todas as automações.

🛠️ Tecnologias Utilizadas
Python

CustomTkinter

SQLite

Psutil

Anthropic API

Threading

Pathlib / Shutil

🎯 Objetivos do Projeto
Este projeto foi desenvolvido para praticar:

Automação e manipulação de arquivos do sistema com Python

Interfaces gráficas modernas com CustomTkinter

Banco de dados SQLite

Integração com APIs externas

Programação assíncrona (Threading)

Organização e arquitetura de código


⚠️ Aviso
Este projeto foi desenvolvido para fins de estudo e portfólio.

Algumas automações dependem de softwares instalados nativamente no ecossistema Windows e da inclusão de uma chave própria da Anthropic para respostas via Claude.

📄 Licença
Este projeto é aberto para fins educacionais e aprendizado.
---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone [https://github.com/fabiopy-creator/jarvis.git](https://github.com/fabiopy-creator/jarvis.git)
