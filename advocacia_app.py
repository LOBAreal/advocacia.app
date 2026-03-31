import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import shutil
import datetime
import subprocess
from spellchecker import SpellChecker
import sys
# ================================================
# ==================== CONFIGURAÇÃO ==============
# ================================================

ADVOCACIA_DIR = os.path.expanduser(r"~\Advocacia")
os.makedirs(ADVOCACIA_DIR, exist_ok=True)

def inicializar_corretor():
    # Detecta se está rodando como .exe (PyInstaller) ou script normal
    if hasattr(sys, '_MEIPASS'):
        # Caminho onde o PyInstaller extrai os arquivos temporários
        dict_path = os.path.join(sys._MEIPASS, "spellchecker", "resources")
    else:
        # Caminho no ambiente de desenvolvimento (VS Code/Terminal)
        try:
            import spellchecker
            dict_path = os.path.join(os.path.dirname(spellchecker.__file__), "resources")
        except ImportError:
            dict_path = None

    try:
        # Tenta iniciar com o idioma padrão (isso busca na pasta resources)
        # Se os arquivos estiverem no lugar certo, ele funciona direto.
        return SpellChecker(language='pt', distance=2)
    except ValueError:
        # Se falhar (erro do print que você mandou), criamos um objeto limpo 
        # e tentamos carregar o arquivo manualmente para não travar o app.
        sc = SpellChecker(language=None, distance=2)
        if dict_path:
            pt_json = os.path.join(dict_path, "pt.json")
            if os.path.exists(pt_json):
                sc.word_frequency.load_dictionary(pt_json)
        return sc

# Inicializa globalmente com segurança
spell = inicializar_corretor()
# ================================================
# ==================== FUNÇÕES ===================
# ================================================

def novo_processo():
    numero = entry_numero.get().strip()
    cliente = entry_cliente.get().strip()
    if not numero or not cliente:
        messagebox.showerror("Erro", "Número do processo e nome do cliente são obrigatórios!")
        return
    
    num_processo = numero.replace(" ", "_").replace("/", "-")
    nome_cliente = cliente.replace(" ", "_")
    
    pasta = os.path.join(ADVOCACIA_DIR, nome_cliente, num_processo)
    
    subpastas = ["Documentos", "Peticoes", "Prazos", "Andamentos", "Provas", "Contratos", "Notas"]
    for sub in subpastas:
        os.makedirs(os.path.join(pasta, sub), exist_ok=True)
    
    resumo_path = os.path.join(pasta, "RESUMO.txt")
    with open(resumo_path, "w", encoding="utf-8") as f:
        f.write(f"Processo: {numero}\n")
        f.write(f"Cliente: {cliente}\n")
        f.write(f"Data de criação: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    open(os.path.join(pasta, "PRAZOS.txt"), "w", encoding="utf-8").close()
    
    messagebox.showinfo("Sucesso", f"✅ Processo criado com sucesso!\n\nLocal:\n{pasta}")
    
    entry_numero.delete(0, tk.END)
    entry_cliente.delete(0, tk.END)


def listar_processos():
    if not os.path.exists(ADVOCACIA_DIR) or not os.listdir(ADVOCACIA_DIR):
        messagebox.showinfo("Lista", "Nenhum processo encontrado ainda.")
        return
    subprocess.Popen(f'explorer "{ADVOCACIA_DIR}"')


def buscar_processo():
    termo = entry_busca.get().strip()
    if not termo:
        messagebox.showwarning("Aviso", "Digite algo para buscar.")
        return
    
    resultados = []
    for root_dir, dirs, files in os.walk(ADVOCACIA_DIR):
        for item in dirs + files:
            if termo.lower() in item.lower():
                resultados.append(os.path.join(root_dir, item))
    
    if resultados:
        msg = "✅ Resultados encontrados:\n\n" + "\n".join(resultados[:20])
        if len(resultados) > 20:
            msg += f"\n\n... e mais {len(resultados)-20} resultados."
        messagebox.showinfo("Busca", msg)
        subprocess.Popen(f'explorer "{os.path.dirname(resultados[0])}"')
    else:
        messagebox.showinfo("Busca", f"Nenhum resultado encontrado para: {termo}")


def abrir_pasta():
    termo = entry_abrir.get().strip()
    if not termo:
        messagebox.showwarning("Aviso", "Digite parte do número ou nome do cliente.")
        return
    
    encontrado = False
    for root_dir, dirs, files in os.walk(ADVOCACIA_DIR):
        for d in dirs:
            if termo.lower() in d.lower():
                pasta_completa = os.path.join(root_dir, d)
                subprocess.Popen(f'explorer "{pasta_completa}"')
                encontrado = True
                break
        if encontrado:
            break
    
    if not encontrado:
        messagebox.showinfo("Não encontrado", f"Nenhuma pasta encontrada com '{termo}'.")


def fazer_backup():
    data = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    backup_file = os.path.expanduser(f"~/Backup_Advocacia_{data}.zip")
    
    try:
        shutil.make_archive(backup_file.replace(".zip", ""), 'zip', ADVOCACIA_DIR)
        messagebox.showinfo("Backup", f"✅ Backup criado com sucesso!\n\nArquivo:\n{backup_file}")
        subprocess.Popen(f'explorer /select,"{backup_file}"')
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar backup:\n{str(e)}")


# ==================== CORRETOR ORTOGRÁFICO ====================
def abrir_corretor_ortografico():
    janela = tk.Toplevel(root)
    janela.title("📝 Corretor Ortográfico - Português")
    janela.geometry("950x680")
    janela.resizable(True, True)
    janela.configure(bg="#1e1e1e")

    tk.Label(janela, text="Digite ou cole seu texto abaixo.\nPalavras com erro aparecerão em vermelho.",
             font=("Arial", 11, "bold"), bg="#1e1e1e", fg="#ffffff").pack(pady=10)

    texto_area = scrolledtext.ScrolledText(janela, font=("Arial", 11), wrap=tk.WORD, undo=True, height=28,
                                           bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff")
    texto_area.pack(fill="both", expand=True, padx=15, pady=10)

    def verificar_ortografia(event=None):
        content = texto_area.get("1.0", tk.END).strip()
        if not content:
            return
        texto_area.tag_remove("erro", "1.0", tk.END)
        palavras = content.split()
        for palavra in palavras:
            palavra_limpa = palavra.strip('.,;:!?()[]{}"\'').lower()
            if palavra_limpa and palavra_limpa not in spell:
                idx = content.lower().find(palavra_limpa)
                if idx != -1:
                    start = f"1.0 + {idx} chars"
                    end = f"1.0 + {idx + len(palavra_limpa)} chars"
                    texto_area.tag_add("erro", start, end)
        texto_area.tag_config("erro", foreground="#ff6666", underline=True)

    texto_area.bind("<KeyRelease>", verificar_ortografia)

    def corrigir_texto():
        content = texto_area.get("1.0", tk.END).strip()
        if not content:
            return
        palavras = content.split()
        texto_corrigido = []
        for palavra in palavras:
            palavra_limpa = palavra.strip('.,;:!?()[]{}"\'')
            if palavra_limpa and palavra_limpa.lower() not in spell:
                correcao = spell.correction(palavra_limpa.lower())
                if correcao:
                    if palavra and palavra[0].isupper():
                        correcao = correcao.capitalize()
                    texto_corrigido.append(correcao)
                else:
                    texto_corrigido.append(palavra)
            else:
                texto_corrigido.append(palavra)
        
        texto_area.delete("1.0", tk.END)
        texto_area.insert("1.0", " ".join(texto_corrigido))
        verificar_ortografia()

    ttk.Button(janela, text="🔧 Corrigir Todo o Texto Automaticamente", 
               command=corrigir_texto).pack(pady=10)

    tk.Label(janela, text="Dica: Erros aparecem em vermelho. Use o botão para corrigir automaticamente.",
             font=("Arial", 9), bg="#1e1e1e", fg="#aaaaaa").pack(pady=5)


# ================================================
# ============= INTERFACE GRÁFICA COM SCROLL =====
# ================================================

root = tk.Tk()
root.title("Advocacia App - Gerenciador de Processos")
root.geometry("820x760")
root.resizable(True, True)

# ==================== CANVAS + SCROLL ====================
main_canvas = tk.Canvas(root, highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = ttk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=5)
scrollbar.pack(side="right", fill="y")

# Scroll com roda do mouse
def on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", on_mousewheel)
main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))
main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))

# ==================== CONTROLE DE TEMA ====================
tema_escuro = tk.BooleanVar(value=False)   # Inicia em Claro (branco)

style = ttk.Style()
style.theme_use("clam")

def aplicar_tema():
    if tema_escuro.get():  # === TEMA ESCURO ===
        root.configure(bg="#1e1e1e")
        main_canvas.configure(bg="#1e1e1e")
        
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
        style.configure("TLabelframe", background="#1e1e1e", foreground="#ffffff")
        style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#ffffff")
        style.configure("TButton", background="#2d2d2d", foreground="#ffffff")
        style.configure("TEntry", fieldbackground="#2d2d2d", foreground="#ffffff")
        
        btn_config.configure(bg="#1e1e1e", fg="#ffffff")
        
        # Atualiza labels soltas dentro do frame scrollável
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg="#1e1e1e", fg="#ffffff")
                
    else:  # === TEMA CLARO ===
        root.configure(bg="#f0f0f0")
        main_canvas.configure(bg="#f0f0f0")
        
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#000000")
        style.configure("TLabelframe", background="#f0f0f0", foreground="#000000")
        style.configure("TLabelframe.Label", background="#f0f0f0", foreground="#000000")
        style.configure("TButton", background="#e0e0e0", foreground="#000000")
        style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")
        
        btn_config.configure(bg="#f0f0f0", fg="#000000")
    
    root.update()

# ==================== CONTEÚDO ====================

tk.Label(scrollable_frame, text="Advocacia App", font=("Arial", 22, "bold")).pack(pady=20)

# Novo Processo
frame_novo = ttk.LabelFrame(scrollable_frame, text=" Novo Processo ", padding=15)
frame_novo.pack(fill="x", padx=25, pady=10)

tk.Label(frame_novo, text="Número do Processo:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
entry_numero = ttk.Entry(frame_novo, width=60, font=("Arial", 10))
entry_numero.grid(row=0, column=1, pady=8, padx=10)

tk.Label(frame_novo, text="Nome do Cliente:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
entry_cliente = ttk.Entry(frame_novo, width=60, font=("Arial", 10))
entry_cliente.grid(row=1, column=1, pady=8, padx=10)

ttk.Button(frame_novo, text="✅ Criar Novo Processo", command=novo_processo).grid(row=2, column=1, pady=15, sticky="e")

# Ações Rápidas
frame_acoes = ttk.LabelFrame(scrollable_frame, text=" Ações Rápidas ", padding=15)
frame_acoes.pack(fill="x", padx=25, pady=10)

ttk.Button(frame_acoes, text="📋 Listar Todos os Processos", command=listar_processos).pack(fill="x", pady=6)
ttk.Button(frame_acoes, text="🔍 Buscar Processo", command=buscar_processo).pack(fill="x", pady=6)
ttk.Button(frame_acoes, text="📂 Abrir Pasta do Processo", command=abrir_pasta).pack(fill="x", pady=6)
ttk.Button(frame_acoes, text="💾 Fazer Backup Completo", command=fazer_backup).pack(fill="x", pady=6)
ttk.Button(frame_acoes, text="📝 Corretor Ortográfico", 
           command=abrir_corretor_ortografico).pack(fill="x", pady=8)

tk.Label(frame_acoes, text="Termo para buscar:", font=("Arial", 9)).pack(anchor="w", pady=(10,2))
entry_busca = ttk.Entry(frame_acoes, width=75, font=("Arial", 10))
entry_busca.pack(fill="x", pady=5)

tk.Label(frame_acoes, text="Termo (cliente ou número):", font=("Arial", 9)).pack(anchor="w", pady=(8,2))
entry_abrir = ttk.Entry(frame_acoes, width=75, font=("Arial", 10))
entry_abrir.pack(fill="x", pady=5)

# Botão Alternar Tema
btn_tema = ttk.Button(scrollable_frame, text="🌙 Alternar Tema Escuro / Claro",
                     command=lambda: [tema_escuro.set(not tema_escuro.get()), aplicar_tema()])
btn_tema.pack(pady=20)

# Menu Superior
menu_barra = tk.Menu(root)
root.config(menu=menu_barra)
menu_opcoes = tk.Menu(menu_barra, tearoff=0)
menu_barra.add_cascade(label="Configurações", menu=menu_opcoes)
menu_opcoes.add_command(label="🌙 Alternar Tema",
                       command=lambda: [tema_escuro.set(not tema_escuro.get()), aplicar_tema()])
menu_opcoes.add_separator()
menu_opcoes.add_command(label="Sobre o App",
                       command=lambda: messagebox.showinfo("Sobre",
                       "Advocacia App\nGerenciador de Processos\nVersão 1.0"))

# Botão Engrenagem
def mostrar_menu_config():
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="🌙 Alternar Tema",
                    command=lambda: [tema_escuro.set(not tema_escuro.get()), aplicar_tema()])
    menu.add_separator()
    menu.add_command(label="Sobre o App",
                    command=lambda: messagebox.showinfo("Sobre",
                    "Advocacia App\nGerenciador de Processos\nVersão 1.0"))
    menu.post(root.winfo_pointerx(), root.winfo_pointery())

btn_config = tk.Button(root, text="⚙️", font=("Arial", 18), bd=0, relief="flat", cursor="hand2",
                       command=mostrar_menu_config)
btn_config.place(relx=1.0, x=-25, y=18, anchor="ne")

# ==================== INICIALIZAÇÃO ====================
aplicar_tema()          # Inicia no tema claro (branco)

# Rodapé
tk.Label(scrollable_frame, text=f"Diretório dos processos: {ADVOCACIA_DIR}",
         font=("Arial", 9), fg="#666666").pack(pady=30)

root.mainloop()