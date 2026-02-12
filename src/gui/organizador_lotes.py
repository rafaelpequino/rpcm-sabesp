"""
Módulo de Organização de Lotes
Transfere e organiza arquivos PDF por lote
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
import shutil

from src.gui.styles import COLORS, FONTS, SPACING


class OrganizadorLotesFrame(ctk.CTkScrollableFrame):
    """Frame para organizar RPCMs por lote"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent",
            scrollbar_button_color=COLORS['primary'],
            scrollbar_button_hover_color=COLORS['hover']
        )
        
        # Configurar scroll suave
        self._parent_canvas.configure(yscrollincrement=20)
        self._configurar_scroll_suave()
        
        # Variáveis
        self.pasta_origem = None
        self.pasta_destino = None
        
        self._criar_interface()
    
    def _configurar_scroll_suave(self):
        """Configura scroll suave com mouse wheel"""
        def _on_mousewheel(event):
            # Scroll mais suave e rápido
            self._parent_canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")
        
        # Bind para o canvas
        self._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Unbind quando sair da janela para não conflitar
        def _unbind_mousewheel(event):
            self._parent_canvas.unbind_all("<MouseWheel>")
        
        def _bind_mousewheel(event):
            self._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self._parent_canvas.bind("<Leave>", _unbind_mousewheel)
        self._parent_canvas.bind("<Enter>", _bind_mousewheel)
    
    def _criar_interface(self):
        """Cria a interface do organizador"""
        
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📁 Organizador de Lotes",
            font=FONTS['title']
        )
        titulo.pack(pady=(10, 20))
        
        subtitulo = ctk.CTkLabel(
            self,
            text="Organize arquivos PDF por lote - Copie do banco para a pasta do lote",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        subtitulo.pack(pady=(0, 20))
        
        # ===== PASTA DE ORIGEM (BANCO) =====
        frame_origem = ctk.CTkFrame(self)
        frame_origem.pack(fill="x", padx=20, pady=10)
        
        label_origem = ctk.CTkLabel(
            frame_origem,
            text="📂 Pasta de Origem (Banco):",
            font=FONTS['label']
        )
        label_origem.pack(anchor="w", padx=10, pady=(10, 5))
        
        container_origem = ctk.CTkFrame(frame_origem)
        container_origem.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry_origem = ctk.CTkEntry(
            container_origem,
            placeholder_text="Selecione a pasta do banco...",
            height=35,
            font=FONTS['input']
        )
        self.entry_origem.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_origem = ctk.CTkButton(
            container_origem,
            text="📂 Selecionar",
            command=self._selecionar_origem,
            width=150,
            height=35,
            fg_color=COLORS['success'],
            hover_color="#218838"
        )
        btn_origem.pack(side="left")
        
        # ===== PASTA DE DESTINO (LOTE) =====
        frame_destino = ctk.CTkFrame(self)
        frame_destino.pack(fill="x", padx=20, pady=10)
        
        label_destino = ctk.CTkLabel(
            frame_destino,
            text="📁 Pasta de Destino (Lote):",
            font=FONTS['label']
        )
        label_destino.pack(anchor="w", padx=10, pady=(10, 5))
        
        container_destino = ctk.CTkFrame(frame_destino)
        container_destino.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry_destino = ctk.CTkEntry(
            container_destino,
            placeholder_text="Selecione a pasta do lote...",
            height=35,
            font=FONTS['input']
        )
        self.entry_destino.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_destino = ctk.CTkButton(
            container_destino,
            text="📂 Selecionar",
            command=self._selecionar_destino,
            width=150,
            height=35,
            fg_color=COLORS['success'],
            hover_color="#218838"
        )
        btn_destino.pack(side="left")
        
        # ===== LISTA DE NÚMEROS =====
        frame_numeros = ctk.CTkFrame(self)
        frame_numeros.pack(fill="x", padx=20, pady=10)
        
        label_numeros = ctk.CTkLabel(
            frame_numeros,
            text="📝 Lista de Números das RPCMs:",
            font=FONTS['label']
        )
        label_numeros.pack(anchor="w", padx=10, pady=(10, 5))
        
        info_label = ctk.CTkLabel(
            frame_numeros,
            text="Insira os números separados por vírgula, espaço ou quebra de linha\nExemplo: 400006, 400009, 400010 ou cada um em uma linha",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        info_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        self.text_numeros = ctk.CTkTextbox(
            frame_numeros,
            height=120,
            font=FONTS['input']
        )
        self.text_numeros.pack(fill="x", padx=10, pady=(0, 10))
        
        # ===== BOTÕES DE AÇÃO =====
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(fill="x", padx=20, pady=10)
        
        container_botoes = ctk.CTkFrame(frame_botoes)
        container_botoes.pack(pady=10)
        
        btn_limpar_hist = ctk.CTkButton(
            container_botoes,
            text="🧹 Limpar Histórico",
            command=self._limpar_historico,
            width=150,
            height=40,
            fg_color="#6c757d",
            hover_color="#5a6268",
            text_color="white"
        )
        btn_limpar_hist.pack(side="left", padx=5)
        
        btn_limpar = ctk.CTkButton(
            container_botoes,
            text="🧹 Limpar Tudo",
            command=self._limpar_tudo,
            width=150,
            height=40,
            fg_color="#6c757d",
            hover_color="#5a6268",
            text_color="white"
        )
        btn_limpar.pack(side="left", padx=5)
        
        btn_verificar = ctk.CTkButton(
            container_botoes,
            text="✓ Verificar Destino",
            command=self._verificar_destino,
            width=150,
            height=40,
            fg_color=COLORS['primary'],
            hover_color=COLORS['hover'],
            text_color="white"
        )
        btn_verificar.pack(side="left", padx=5)
        
        self.btn_organizar = ctk.CTkButton(
            container_botoes,
            text="🚀 Organizar Lote",
            command=self._organizar_lote,
            width=150,
            height=40,
            fg_color=COLORS['info'],
            hover_color="#138496"
        )
        self.btn_organizar.pack(side="left", padx=5)
        
        # ===== ÁREA DE LOG =====
        frame_log = ctk.CTkFrame(self)
        frame_log.pack(fill="x", padx=20, pady=(0, 20))
        
        label_log = ctk.CTkLabel(
            frame_log,
            text="📊 Histórico:",
            font=FONTS['label']
        )
        label_log.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.log_textbox = ctk.CTkTextbox(
            frame_log,
            height=250,
            font=("Courier New", 11),
            fg_color="#1a1a1a",
            text_color="#00FF00"
        )
        self.log_textbox.pack(fill="x", padx=10, pady=(0, 10))
    
    def _selecionar_origem(self):
        """Seleciona pasta de origem (banco)"""
        pasta = filedialog.askdirectory(title="Selecione a pasta do banco")
        if pasta:
            self.pasta_origem = Path(pasta)
            self.entry_origem.delete(0, 'end')
            self.entry_origem.insert(0, str(pasta))
            self._adicionar_log(f"✅ Pasta de origem selecionada: {pasta}", "info")
    
    def _selecionar_destino(self):
        """Seleciona pasta de destino (lote)"""
        pasta = filedialog.askdirectory(title="Selecione a pasta do lote")
        if pasta:
            self.pasta_destino = Path(pasta)
            self.entry_destino.delete(0, 'end')
            self.entry_destino.insert(0, str(pasta))
            self._adicionar_log(f"✅ Pasta de destino selecionada: {pasta}", "info")
    
    def _obter_lista_numeros(self):
        """Obtém e processa a lista de números"""
        texto_numeros = self.text_numeros.get("1.0", "end").strip()
        if not texto_numeros:
            return None
        
        lista_numeros = []
        for item in texto_numeros.replace(',', '\n').split('\n'):
            item = item.strip()
            if item:
                lista_numeros.append(item)
        
        return lista_numeros if lista_numeros else None
    
    def _extrair_numero_arquivo(self, nome_arquivo):
        """Extrai os primeiros dígitos do nome do arquivo"""
        numero = ""
        for char in nome_arquivo:
            if char.isdigit():
                numero += char
            else:
                break
        return numero
    
    def _limpar_historico(self):
        """Limpa apenas o histórico"""
        self.log_textbox.delete("1.0", "end")
        self._adicionar_log("✨ Histórico limpo!", "info")
    
    def _limpar_tudo(self):
        """Limpa todos os campos"""
        self.entry_origem.delete(0, 'end')
        self.entry_destino.delete(0, 'end')
        self.text_numeros.delete("1.0", "end")
        self.log_textbox.delete("1.0", "end")
        self.pasta_origem = None
        self.pasta_destino = None
        self._adicionar_log("✨ Campos e histórico limpos!", "info")
    
    def _adicionar_log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log com cor"""
        cores = {
            "info": "#00AAFF",
            "sucesso": "#00FF00",
            "erro": "#FF4444",
            "aviso": "#FFAA00"
        }
        
        self.log_textbox.insert("end", mensagem + "\n")
        self.log_textbox.see("end")
        self.update()
    
    def _verificar_destino(self):
        """Verifica se todos os números existem na pasta de destino"""
        if not self.pasta_destino:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de destino (lote)!")
            return
        
        lista_numeros = self._obter_lista_numeros()
        if not lista_numeros:
            messagebox.showerror("Erro", "Por favor, insira números para verificar!")
            return
        
        # Limpar log
        self.log_textbox.delete("1.0", "end")
        
        # Executar em thread
        thread = threading.Thread(
            target=self._thread_verificar,
            args=(self.pasta_destino, lista_numeros)
        )
        thread.start()
    
    def _thread_verificar(self, pasta_destino, lista_numeros):
        """Thread para verificar números na pasta de destino"""
        try:
            self._adicionar_log("🔍 Iniciando Verificação...\n", "info")
            self._adicionar_log(f"📂 Pasta de Destino (Lote): {pasta_destino}\n", "info")
            self._adicionar_log("-" * 80 + "\n", "info")
            
            if not pasta_destino.exists():
                self._adicionar_log("❌ Pasta de destino não existe!\n", "erro")
                return
            
            # Obter todos os PDFs
            arquivos_encontrados = list(pasta_destino.glob("*.[pP][dD][fF]"))
            numeros_encontrados = set()
            mapa_numeros_arquivos = {}
            
            for arquivo in arquivos_encontrados:
                numero = self._extrair_numero_arquivo(arquivo.stem)
                if numero:
                    numeros_encontrados.add(numero)
                    if numero not in mapa_numeros_arquivos:
                        mapa_numeros_arquivos[numero] = []
                    mapa_numeros_arquivos[numero].append(arquivo.name)
            
            # Converter lista para conjunto
            lista_numeros_str = {str(num).strip() for num in lista_numeros}
            
            # Calcular categorias
            conformes = sorted(lista_numeros_str & numeros_encontrados)
            ausentes = sorted(lista_numeros_str - numeros_encontrados)
            excedentes = sorted(numeros_encontrados - lista_numeros_str)
            
            # Exibir resultado no log
            self._adicionar_log(f"📊 RESULTADO DA VERIFICAÇÃO:\n", "info")
            self._adicionar_log(f"\n1️⃣  Total de arquivos na pasta de Destino (Lote): {len(arquivos_encontrados)}", "sucesso")
            self._adicionar_log(f"2️⃣  Números ÚNICOS encontrados no Destino (Lote): {len(numeros_encontrados)}", "sucesso")
            self._adicionar_log(f"3️⃣  Total de números solicitados: {len(lista_numeros_str)}", "info")
            self._adicionar_log(f"4️⃣  Conformes (solicitados encontrados): {len(conformes)}", "sucesso")
            
            if ausentes:
                self._adicionar_log(f"\n5️⃣  ❌ Ausentes (não encontrados): {len(ausentes)}", "erro")
                self._adicionar_log(f"   {', '.join(ausentes)}", "erro")
            else:
                self._adicionar_log(f"\n5️⃣  ✅ Ausentes (não encontrados): 0", "sucesso")
            
            if excedentes:
                self._adicionar_log(f"\n6️⃣  ⚠️ Excedentes (não solicitados): {len(excedentes)}", "aviso")
                self._adicionar_log(f"   {', '.join(excedentes)}", "aviso")
            else:
                self._adicionar_log(f"\n6️⃣  ✅ Excedentes (não solicitados): 0", "sucesso")
            
            # Verificar repetidos
            numeros_repetidos = {num: arqs for num, arqs in mapa_numeros_arquivos.items() if len(arqs) > 1}
            
            if numeros_repetidos:
                self._adicionar_log(f"\n7️⃣  🔄 NÚMEROS REPETIDOS DETECTADOS: {len(numeros_repetidos)}", "aviso")
                for numero, arquivos in sorted(numeros_repetidos.items()):
                    self._adicionar_log(f"   Número {numero}: {len(arquivos)} arquivos", "aviso")
                    for arquivo in arquivos:
                        self._adicionar_log(f"      • {arquivo}", "aviso")
            else:
                self._adicionar_log(f"\n7️⃣  ✅ Números repetidos: 0", "sucesso")
            
            self._adicionar_log("\n" + "-" * 80, "info")
            
            # Mensagem resumida
            resumo = f"VERIFICAÇÃO CONCLUÍDA\n\n"
            resumo += f"1️⃣  Total de arquivos na pasta de Destino (Lote): {len(arquivos_encontrados)}\n"
            resumo += f"2️⃣  Números ÚNICOS encontrados no Destino (Lote): {len(numeros_encontrados)}\n"
            resumo += f"3️⃣  Total de números solicitados: {len(lista_numeros_str)}\n"
            resumo += f"4️⃣  Conformes: {len(conformes)}\n"
            
            if ausentes:
                resumo += f"\n5️⃣  ❌ Ausentes ({len(ausentes)}):\n{', '.join(ausentes)}\n"
            else:
                resumo += f"\n5️⃣  ✅ Ausentes: 0\n"
            
            if excedentes:
                resumo += f"\n6️⃣  ⚠️ Excedentes ({len(excedentes)}):\n{', '.join(excedentes)}\n"
            else:
                resumo += f"\n6️⃣  ✅ Excedentes: 0\n"
            
            # Adicionar informações de números repetidos
            if numeros_repetidos:
                resumo += f"\n7️⃣  🔄 NÚMEROS REPETIDOS ({len(numeros_repetidos)}):\n"
                for numero, arquivos in sorted(numeros_repetidos.items()):
                    resumo += f"   • Número {numero}: {len(arquivos)} arquivos\n"
                    for arquivo in arquivos:
                        resumo += f"      - {arquivo}\n"
            else:
                resumo += f"\n7️⃣  ✅ Números repetidos: 0\n"
            
            if not ausentes and not excedentes:
                resumo += "\n✅ Tudo está em conformidade!"
            
            messagebox.showinfo("Verificação Concluída", resumo)
            
        except Exception as e:
            self._adicionar_log(f"❌ Erro: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante verificação: {str(e)}")
    
    def _organizar_lote(self):
        """Organiza o lote - copia arquivos"""
        if not self.pasta_origem:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de origem (banco)!")
            return
        
        if not self.pasta_destino:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de destino (lote)!")
            return
        
        lista_numeros = self._obter_lista_numeros()
        if not lista_numeros:
            messagebox.showerror("Erro", "Por favor, insira números para copiar!")
            return
        
        # Limpar log
        self.log_textbox.delete("1.0", "end")
        
        # Desabilitar botão
        self.btn_organizar.configure(state="disabled")
        
        # Executar em thread
        thread = threading.Thread(
            target=self._thread_copia,
            args=(self.pasta_origem, self.pasta_destino, lista_numeros)
        )
        thread.start()
    
    def _thread_copia(self, pasta_origem, pasta_destino, lista_numeros):
        """Thread para copiar arquivos"""
        try:
            self._adicionar_log("🔍 Iniciando organização do lote...\n", "info")
            self._adicionar_log(f"📂 Pasta de Origem: {pasta_origem}", "info")
            self._adicionar_log(f"📂 Pasta de Destino: {pasta_destino}", "info")
            self._adicionar_log(f"📝 Números a copiar: {len(lista_numeros)}\n", "info")
            self._adicionar_log("-" * 80 + "\n", "info")
            
            # Verificar origem
            if not pasta_origem.exists():
                self._adicionar_log(f"❌ Pasta de origem não existe!\n", "erro")
                messagebox.showerror("Erro", "A pasta de origem não existe!")
                return
            
            # Criar pasta destino
            if not pasta_destino.exists():
                pasta_destino.mkdir(parents=True, exist_ok=True)
                self._adicionar_log(f"✅ Pasta de destino criada\n", "sucesso")
            
            # Converter lista
            lista_numeros_str = {str(num).strip() for num in lista_numeros}
            
            # Contadores
            arquivos_copiados = 0
            numeros_copiados = set()
            erros = 0
            
            # Processar PDFs
            arquivos_encontrados = list(pasta_origem.glob("*.[pP][dD][fF]"))
            
            self._adicionar_log(f"Total de arquivos na origem: {len(arquivos_encontrados)}\n", "info")
            
            for arquivo in arquivos_encontrados:
                numero = self._extrair_numero_arquivo(arquivo.stem)
                
                if numero in lista_numeros_str:
                    try:
                        caminho_destino = pasta_destino / arquivo.name
                        shutil.copy2(str(arquivo), str(caminho_destino))
                        self._adicionar_log(f"✅ Copiado: {arquivo.name}", "sucesso")
                        arquivos_copiados += 1
                        numeros_copiados.add(numero)
                    except Exception as e:
                        self._adicionar_log(f"❌ Erro ao copiar {arquivo.name}: {str(e)}", "erro")
                        erros += 1
            
            # Números faltando
            numeros_nao_encontrados = sorted(lista_numeros_str - numeros_copiados)
            
            # Resumo
            self._adicionar_log("\n" + "-" * 80, "info")
            self._adicionar_log("\n📊 RESUMO DA OPERAÇÃO:\n", "info")
            self._adicionar_log(f"1️⃣  Arquivos copiados: {arquivos_copiados}", "sucesso")
            self._adicionar_log(f"2️⃣  Números únicos copiados: {len(numeros_copiados)}", "sucesso")
            
            if numeros_nao_encontrados:
                self._adicionar_log(f"3️⃣  ❌ Números não encontrados: {len(numeros_nao_encontrados)}", "erro")
                self._adicionar_log(f"   {', '.join(numeros_nao_encontrados)}", "erro")
            else:
                self._adicionar_log(f"3️⃣  ✅ Números não encontrados: 0", "sucesso")
            
            if erros > 0:
                self._adicionar_log(f"\n⚠️ Erros durante cópia: {erros}", "erro")
            
            self._adicionar_log("\n✨ Operação concluída!", "sucesso")
            
            # Mensagem resumida
            resumo = f"Operação concluída!\n\n"
            resumo += f"1️⃣  Arquivos copiados: {arquivos_copiados}\n"
            resumo += f"2️⃣  Números únicos copiados: {len(numeros_copiados)}\n"
            
            if numeros_nao_encontrados:
                resumo += f"\n3️⃣  ❌ Números não encontrados ({len(numeros_nao_encontrados)}):\n"
                resumo += f"{', '.join(numeros_nao_encontrados)}\n"
            else:
                resumo += f"\n3️⃣  ✅ Números não encontrados: 0\n"
            
            if erros > 0:
                resumo += f"\n⚠️ Erros: {erros}\n"
            
            messagebox.showinfo("Sucesso", resumo)
            
        except Exception as e:
            self._adicionar_log(f"❌ Erro geral: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante operação: {str(e)}")
        
        finally:
            self.btn_organizar.configure(state="normal")
