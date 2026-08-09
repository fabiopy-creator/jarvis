# 🤖 JARVIS-X

## 🖼️ Demonstração do Sistema

![Interface do JARVIS-X](jarvis.png)

Um assistente pessoal desenvolvido em Python com interface gráfica moderna e minimalista usando **CustomTkinter**.

O objetivo do projeto é simular um sistema operacional assistido por IA, oferecendo monitoramento do computador em tempo real, automação de tarefas e suporte a inteligência artificial (mediante chave do usuário).

---

## 🔗 Repositório

[https://github.com/fabiopy-creator/jarvis](https://github.com/fabiopy-creator/jarvis)

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

O projeto possui uma interface inspirada em uma estética monocromática e melancólica (*Void / Hollow Knight*):

- Tema escuro e minimalista em preto e branco osso
- Painel lateral de monitoramento direto (CPU, RAM, DISK)
- Terminal integrado limpo
- Status em tempo real
- Layout retilíneo sem cantos arredondados

---

## 🔑 Configuração da IA

A funcionalidade de IA utiliza a API da Anthropic (Claude).

Por motivos de segurança e custos, **nenhuma chave de API é fornecida neste repositório**.

Sem uma chave configurada, o assistente funcionará perfeitamente e 100% offline em todas as automações:

✅ Interface gráfica  
✅ Monitoramento do sistema em tempo real  
✅ Automação de sites  
✅ Automação de aplicativos Windows  
✅ Organização de arquivos (Downloads e Área de Trabalho)  
✅ Banco de Dados e Histórico SQLite  

A única função desabilitada será o chat generativo com a IA. Para ativar a IA, defina a variável de ambiente no seu sistema ou configure no código:

```python
ANTHROPIC_API_KEY = "SUA_CHAVE_AQUI"
