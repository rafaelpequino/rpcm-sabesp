"""
Módulo de Conversão DOCX para PDF
Converte arquivos DOCX para PDF com alta qualidade
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from src.gui.styles import COLORS, FONTS, SPACING

# Importar bibliotecas de conversão
try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_DISPONIVEL = True
except ImportError:
    DOCX2PDF_DISPONIVEL = False

try:
    from docx import Document
    import win32com.client
    WORD_COM_DISPONIVEL = True
except ImportError:
    WORD_COM_DISPONIVEL = False

try:
    import aspose.words as aw
    ASPOSE_WORDS_DISPONIVEL = True
except ImportError:
    ASPOSE_WORDS_DISPONIVEL = False


class ConversorPdfFrame(ctk.CTkScrollableFrame):
    """Frame para converter DOCX para PDF"""
    
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
        self.pasta_entrada = None
        self.pasta_saida = None
        self.arquivos_selecionados = []
        self.modo_selecao = "pasta"  # "pasta" ou "arquivos"
        self.conversao_ativa = False
        
        # Detectar métodos disponíveis
        self.metodos_disponiveis = self._detectar_metodos()
        
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
    
    def _validar_entrada_manual(self, event=None):
        """Valida o path de entrada quando o usuário cola ou pressiona Enter"""
        path_str = self.entry_entrada.get().strip()
        
        if not path_str:
            return
        
        if self.modo_selecao == "pasta":
            path_obj = Path(path_str)
            if path_obj.exists() and path_obj.is_dir():
                self.pasta_entrada = path_obj
                self._adicionar_log(f"✅ Pasta validada: {path_obj.name}", "info")
            else:
                self.pasta_entrada = None
                self.entry_entrada.delete(0, 'end')
                self._adicionar_log(f"❌ Caminho de pasta inválido", "erro")
        
        # Se foi pressionado Enter, fazer o foco sair do campo
        if event and event.keysym == "Return":
            self.focus()
    
    def _validar_saida_manual(self, event=None):
        """Valida o path de saída quando o usuário cola ou pressiona Enter"""
        path_str = self.entry_saida.get().strip()
        
        if not path_str:
            return
        
        path_obj = Path(path_str)
        if path_obj.exists() and path_obj.is_dir():
            self.pasta_saida = path_obj
            self._adicionar_log(f"✅ Pasta de saída validada: {path_obj.name}", "info")
        else:
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                self.pasta_saida = path_obj
                self._adicionar_log(f"✅ Pasta de saída criada: {path_obj.name}", "info")
            except Exception:
                self.pasta_saida = None
                self.entry_saida.delete(0, 'end')
                self._adicionar_log(f"❌ Caminho de pasta de saída inválido", "erro")
        
        # Se foi pressionado Enter, fazer o foco sair do campo
        if event and event.keysym == "Return":
            self.focus()
    
    def _detectar_metodos(self):
        """Detecta métodos de conversão disponíveis"""
        metodos = []
        
        if WORD_COM_DISPONIVEL:
            metodos.append("word_com")
        
        if DOCX2PDF_DISPONIVEL:
            metodos.append("docx2pdf")
        
        if ASPOSE_WORDS_DISPONIVEL:
            metodos.append("aspose")
        
        return metodos
    
    def _criar_interface(self):
        """Cria a interface do conversor"""
        
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📄 Conversor DOCX → PDF",
            font=FONTS['title']
        )
        titulo.pack(pady=(10, 5))
        
        subtitulo = ctk.CTkLabel(
            self,
            text="Conversão profissional preservando formatação, imagens e tabelas",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        subtitulo.pack(pady=(0, 20))
        
        # ===== MODO DE SELEÇÃO =====
        frame_modo = ctk.CTkFrame(self)
        frame_modo.pack(fill="x", padx=20, pady=10)
        
        label_modo = ctk.CTkLabel(
            frame_modo,
            text="📋 Modo de Seleção:",
            font=FONTS['label']
        )
        label_modo.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.radio_var = ctk.StringVar(value="pasta")
        
        rb_pasta = ctk.CTkRadioButton(
            frame_modo,
            text="📁 Converter toda uma pasta",
            variable=self.radio_var,
            value="pasta",
            command=self._atualizar_modo,
            font=FONTS['small']
        )
        rb_pasta.pack(anchor="w", padx=20, pady=2)
        
        rb_arquivos = ctk.CTkRadioButton(
            frame_modo,
            text="📄 Selecionar arquivos específicos",
            variable=self.radio_var,
            value="arquivos",
            command=self._atualizar_modo,
            font=FONTS['small']
        )
        rb_arquivos.pack(anchor="w", padx=20, pady=(2, 10))
        
        # ===== PASTA/ARQUIVOS DE ENTRADA =====
        frame_entrada = ctk.CTkFrame(self)
        frame_entrada.pack(fill="x", padx=20, pady=10)
        
        self.label_entrada = ctk.CTkLabel(
            frame_entrada,
            text="📂 Pasta de Entrada (DOCX):",
            font=FONTS['label']
        )
        self.label_entrada.pack(anchor="w", padx=10, pady=(10, 5))
        
        container_entrada = ctk.CTkFrame(frame_entrada)
        container_entrada.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry_entrada = ctk.CTkEntry(
            container_entrada,
            placeholder_text="Selecione a pasta ou arquivos...",
            height=35,
            font=FONTS['input']
        )
        self.entry_entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind para validação ao perder foco e ao pressionar Enter
        self.entry_entrada.bind("<FocusOut>", self._validar_entrada_manual)
        self.entry_entrada.bind("<Return>", self._validar_entrada_manual)
        
        self.btn_entrada = ctk.CTkButton(
            container_entrada,
            text="📂 Selecionar Pasta",
            command=self._selecionar_entrada,
            width=150,
            height=35,
            fg_color=COLORS['success'],
            hover_color="#218838"
        )
        self.btn_entrada.pack(side="left")
        
        # ===== PASTA DE SAÍDA =====
        frame_saida = ctk.CTkFrame(self)
        frame_saida.pack(fill="x", padx=20, pady=10)
        
        label_saida = ctk.CTkLabel(
            frame_saida,
            text="📁 Pasta de Saída (PDF):",
            font=FONTS['label']
        )
        label_saida.pack(anchor="w", padx=10, pady=(10, 5))
        
        container_saida = ctk.CTkFrame(frame_saida)
        container_saida.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry_saida = ctk.CTkEntry(
            container_saida,
            placeholder_text="Selecione a pasta de saída...",
            height=35,
            font=FONTS['input']
        )
        self.entry_saida.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind para validação ao perder foco e ao pressionar Enter
        self.entry_saida.bind("<FocusOut>", self._validar_saida_manual)
        self.entry_saida.bind("<Return>", self._validar_saida_manual)
        
        btn_saida = ctk.CTkButton(
            container_saida,
            text="📂 Selecionar",
            command=self._selecionar_saida,
            width=150,
            height=35,
            fg_color=COLORS['success'],
            hover_color="#218838"
        )
        btn_saida.pack(side="left")
        
        # ===== BOTÕES DE AÇÃO =====
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(fill="x", padx=20, pady=10)
        
        container_botoes = ctk.CTkFrame(frame_botoes)
        container_botoes.pack(pady=10)
        
        btn_limpar_hist = ctk.CTkButton(
            container_botoes,
            text="📊 Limpar Histórico",
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
        
        self.btn_converter = ctk.CTkButton(
            container_botoes,
            text="🚀 CONVERTER",
            command=self._executar_conversao,
            width=200,
            height=40,
            fg_color=COLORS['info'],
            hover_color="#138496",
            font=FONTS['button']
        )
        self.btn_converter.pack(side="left", padx=5)
        
        # Label de progresso
        self.label_progresso = ctk.CTkLabel(
            frame_botoes,
            text="",
            font=FONTS['small'],
            text_color=COLORS['info']
        )
        self.label_progresso.pack(pady=5)
        
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
    
    def _atualizar_modo(self):
        """Atualiza interface conforme modo"""
        modo = self.radio_var.get()
        self.modo_selecao = modo
        
        if modo == "pasta":
            self.label_entrada.configure(text="📂 Pasta de Entrada (DOCX):")
            self.btn_entrada.configure(text="📂 Selecionar Pasta")
        else:
            self.label_entrada.configure(text="📄 Arquivos Selecionados:")
            self.btn_entrada.configure(text="📄 Selecionar Arquivos")
        
        # Limpar seleção
        self.entry_entrada.delete(0, 'end')
        self.pasta_entrada = None
        self.arquivos_selecionados = []
    
    def _selecionar_entrada(self):
        """Seleciona pasta ou arquivos"""
        if self.modo_selecao == "pasta":
            self._selecionar_pasta_entrada()
        else:
            self._selecionar_arquivos_entrada()
    
    def _selecionar_pasta_entrada(self):
        """Seleciona pasta de entrada"""
        pasta = filedialog.askdirectory(title="Selecione a pasta com os arquivos DOCX")
        if pasta:
            self.pasta_entrada = Path(pasta)
            self.entry_entrada.delete(0, 'end')
            self.entry_entrada.insert(0, str(pasta))
            
            try:
                docx_files = list(self.pasta_entrada.glob("*.[dD][oO][cC][xX]"))
                self._adicionar_log(f"✅ Pasta selecionada: {len(docx_files)} arquivo(s) DOCX encontrado(s)", "info")
            except:
                pass
    
    def _selecionar_arquivos_entrada(self):
        """Seleciona arquivos específicos"""
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos DOCX para converter",
            filetypes=[("Arquivos DOCX", "*.docx"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivos:
            self.arquivos_selecionados = [Path(f) for f in arquivos]
            total = len(self.arquivos_selecionados)
            
            if total <= 3:
                nomes = ", ".join([f.name for f in self.arquivos_selecionados])
                texto = f"{total} arquivo(s): {nomes}"
            else:
                primeiros = ", ".join([f.name for f in self.arquivos_selecionados[:2]])
                texto = f"{total} arquivo(s): {primeiros}... e mais {total-2}"
            
            self.entry_entrada.delete(0, 'end')
            self.entry_entrada.insert(0, texto)
            
            self._adicionar_log(f"✅ {total} arquivo(s) DOCX selecionado(s)", "info")
    
    def _selecionar_saida(self):
        """Seleciona pasta de saída"""
        pasta = filedialog.askdirectory(title="Selecione a pasta de saída")
        if pasta:
            self.pasta_saida = Path(pasta)
            self.entry_saida.delete(0, 'end')
            self.entry_saida.insert(0, str(pasta))
            self._adicionar_log(f"✅ Pasta de saída selecionada: {pasta}", "info")
    
    def _limpar_historico(self):
        """Limpa apenas o histórico"""
        self.log_textbox.delete("1.0", "end")
        self.label_progresso.configure(text="")
    
    def _limpar_tudo(self):
        """Limpa todos os campos"""
        self.entry_entrada.delete(0, 'end')
        self.entry_saida.delete(0, 'end')
        self.log_textbox.delete("1.0", "end")
        self.label_progresso.configure(text="")
        self.pasta_entrada = None
        self.pasta_saida = None
        self.arquivos_selecionados = []
        self._adicionar_log("✨ Campos limpos!", "info")
    
    def _adicionar_log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log"""
        self.log_textbox.insert("end", mensagem + "\n")
        self.log_textbox.see("end")
        self.update()
    
    def _atualizar_progresso(self, texto):
        """Atualiza texto de progresso"""
        self.label_progresso.configure(text=texto)
        self.update()
    
    def _converter_com_word_com(self, arquivo_docx, arquivo_pdf, word_instance=None):
        """Converte usando Word COM com configurações otimizadas"""
        try:
            # Se não foi passada uma instância, criar uma nova
            fechar_word = False
            if word_instance is None:
                word = win32com.client.Dispatch("Word.Application")
                word.Visible = False
                fechar_word = True
            else:
                word = word_instance
            
            # Abrir documento
            doc = word.Documents.Open(str(arquivo_docx))
            
            # Usar ExportAsFixedFormat com configurações otimizadas
            # Isso preserva melhor a formatação do que SaveAs
            doc.ExportAsFixedFormat(
                OutputFileName=str(arquivo_pdf),
                ExportFormat=17,  # wdExportFormatPDF = 17
                OpenAfterExport=False,
                OptimizeFor=0,  # wdExportOptimizeForPrint = 0 (melhor qualidade)
                CreateBookmarks=0,  # wdExportCreateNoBookmarks = 0
                DocStructureTags=True,  # Preservar estrutura
                BitmapMissingFonts=True,  # Converter fontes ausentes em bitmap
                UseISO19005_1=False  # Não usar PDF/A
            )
            
            doc.Close(SaveChanges=False)
            
            # Só fechar o Word se foi criado nesta chamada
            if fechar_word:
                word.Quit()
            
            return True
        except Exception as e:
            # Se houve erro e criamos o Word, fechá-lo
            if fechar_word and 'word' in locals():
                try:
                    word.Quit()
                except:
                    pass
            raise Exception(f"Erro no Word COM: {str(e)}")
    
    def _converter_com_docx2pdf(self, arquivo_docx, arquivo_pdf):
        """Converte usando docx2pdf"""
        try:
            docx2pdf_convert(str(arquivo_docx), str(arquivo_pdf))
            return True
        except Exception as e:
            raise Exception(f"Erro no docx2pdf: {str(e)}")
    
    def _converter_com_aspose(self, arquivo_docx, arquivo_pdf):
        """Converte usando Aspose com configurações otimizadas"""
        try:
            doc = aw.Document(str(arquivo_docx))
            
            # Configurar opções de salvamento para PDF
            save_options = aw.saving.PdfSaveOptions()
            save_options.compliance = aw.saving.PdfCompliance.PDF17  # PDF 1.7
            save_options.optimize_output = True
            save_options.preserve_form_fields = True
            save_options.jpeg_quality = 100  # Qualidade máxima para imagens
            
            # Salvar com as opções otimizadas
            doc.save(str(arquivo_pdf), save_options)
            return True
        except Exception as e:
            raise Exception(f"Erro no Aspose: {str(e)}")
    
    def _converter_arquivo_com_fallback(self, arquivo_docx, arquivo_pdf, word_instance=None):
        """Converte com fallback automático entre métodos"""
        if not self.metodos_disponiveis:
            raise Exception("Nenhum método de conversão disponível!")
        
        erros_metodos = []
        
        for metodo in self.metodos_disponiveis:
            try:
                nome_metodo = {
                    "word_com": "Microsoft Word COM",
                    "docx2pdf": "docx2pdf",
                    "aspose": "Aspose.Words"
                }.get(metodo, metodo)
                
                if metodo == "word_com":
                    sucesso = self._converter_com_word_com(arquivo_docx, arquivo_pdf, word_instance)
                elif metodo == "docx2pdf":
                    sucesso = self._converter_com_docx2pdf(arquivo_docx, arquivo_pdf)
                elif metodo == "aspose":
                    sucesso = self._converter_com_aspose(arquivo_docx, arquivo_pdf)
                
                if sucesso:
                    return True, nome_metodo
                    
            except Exception as e:
                erro_msg = str(e)
                erros_metodos.append(f"{nome_metodo}: {erro_msg}")
                continue
        
        erros_completos = "\n      ".join(erros_metodos)
        raise Exception(f"Todos os métodos falharam:\n      {erros_completos}")
    
    def _converter_arquivo_worker(self, args):
        """Worker para conversão paralela"""
        idx, total, arquivo_docx, pasta_saida, word_instance = args
        
        try:
            arquivo_pdf = pasta_saida / f"{arquivo_docx.stem}.pdf"
            sucesso, metodo_usado = self._converter_arquivo_com_fallback(
                arquivo_docx, arquivo_pdf, word_instance
            )
            
            return {
                'sucesso': True,
                'arquivo': arquivo_docx.name,
                'metodo': metodo_usado,
                'idx': idx,
                'total': total
            }
        except Exception as e:
            return {
                'sucesso': False,
                'arquivo': arquivo_docx.name,
                'erro': str(e),
                'idx': idx,
                'total': total
            }
    
    
    def _executar_conversao(self):
        """Executa a conversão"""
        # Validar entrada
        if self.modo_selecao == "pasta":
            if not self.pasta_entrada:
                messagebox.showerror("Erro", "Por favor, selecione a pasta de entrada!")
                return
        else:
            if not self.arquivos_selecionados:
                messagebox.showerror("Erro", "Por favor, selecione os arquivos para converter!")
                return
        
        if not self.pasta_saida:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de saída!")
            return
        
        if not self.metodos_disponiveis:
            messagebox.showerror("Erro", "Nenhum método de conversão disponível!\n\nInstale as dependências necessárias.")
            return
        
        if self.conversao_ativa:
            messagebox.showwarning("Aviso", "Já existe uma conversão em andamento!")
            return
        
        # Limpar log
        self.log_textbox.delete("1.0", "end")
        self.label_progresso.configure(text="")
        
        # Desabilitar botão
        self.btn_converter.configure(state="disabled", text="⏳ CONVERTENDO...")
        
        # Executar em thread
        if self.modo_selecao == "pasta":
            thread = threading.Thread(
                target=self._thread_conversao_pasta,
                args=(self.pasta_entrada, self.pasta_saida)
            )
        else:
            thread = threading.Thread(
                target=self._thread_conversao_arquivos,
                args=(self.arquivos_selecionados, self.pasta_saida)
            )
        thread.start()
    
    def _thread_conversao_pasta(self, pasta_entrada, pasta_saida):
        """Thread para conversão de pasta"""
        self.conversao_ativa = True
        word_instance = None
        usar_word_com = "word_com" in self.metodos_disponiveis
        
        try:
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log("🚀 INICIANDO CONVERSÃO DOCX → PDF", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n📂 Pasta de entrada: {pasta_entrada}", "info")
            self._adicionar_log(f"📂 Pasta de saída: {pasta_saida}", "info")
            self._adicionar_log("\n" + "-" * 80 + "\n", "info")
            
            # Verificar pasta
            if not pasta_entrada.exists():
                self._adicionar_log("❌ Pasta de entrada não existe!", "erro")
                messagebox.showerror("Erro", "A pasta de entrada não existe!")
                return
            
            # Criar pasta saída
            if not pasta_saida.exists():
                pasta_saida.mkdir(parents=True, exist_ok=True)
                self._adicionar_log("✅ Pasta de saída criada\n", "sucesso")
            
            # Obter arquivos DOCX
            arquivos_docx = list(pasta_entrada.glob("*.[dD][oO][cC][xX]"))
            
            if not arquivos_docx:
                self._adicionar_log("❌ Nenhum arquivo DOCX encontrado!", "erro")
                messagebox.showwarning("Aviso", "Nenhum arquivo DOCX encontrado!")
                return
            
            total_arquivos = len(arquivos_docx)
            self._adicionar_log(f"📊 Total de arquivos: {total_arquivos}\n", "info")
            
            inicio_conversao = time.time()
            
            # Criar instância única do Word se disponível (otimização)
            if usar_word_com:
                try:
                    self._adicionar_log("⚡ Iniciando Microsoft Word (modo otimizado - sequencial)...\n", "info")
                    word_instance = win32com.client.Dispatch("Word.Application")
                    word_instance.Visible = False
                except Exception as e:
                    self._adicionar_log(f"⚠️ Não foi possível iniciar Word: {e}\n", "aviso")
                    usar_word_com = False
            
            # Se não usar Word COM, usar processamento paralelo
            if not usar_word_com and total_arquivos > 1:
                self._adicionar_log("⚡ Modo paralelo ativado (processamento simultâneo)...\n", "info")
                convertidos, erros, metodos_usados, lista_erros = self._conversao_paralela(
                    arquivos_docx, pasta_saida, total_arquivos
                )
            else:
                # Modo sequencial (Word COM)
                convertidos, erros, metodos_usados, lista_erros = self._conversao_sequencial(
                    arquivos_docx, pasta_saida, total_arquivos, word_instance
                )
            
            tempo_total = time.time() - inicio_conversao
            
            # Resumo
            self._atualizar_progresso("")
            self._adicionar_log("\n" + "=" * 80, "info")
            self._adicionar_log("\n📊 RESUMO DA CONVERSÃO\n", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n✅ Convertidos: {convertidos}", "sucesso")
            self._adicionar_log(f"⏱️ Tempo total: {tempo_total:.1f}s ({tempo_total/max(convertidos, 1):.1f}s por arquivo)", "info")
            
            if metodos_usados:
                self._adicionar_log(f"\n🔧 Métodos utilizados:", "info")
                for metodo, qtd in metodos_usados.items():
                    self._adicionar_log(f"    • {metodo}: {qtd} arquivo(s)", "info")
            
            if erros > 0:
                self._adicionar_log(f"\n❌ Erros: {erros}", "erro")
            
            self._adicionar_log("\n✨ CONVERSÃO CONCLUÍDA!", "sucesso")
            
            resumo = f"Conversão concluída em {tempo_total:.1f}s!\n\nConvertidos: {convertidos}\nErros: {erros}"
            messagebox.showinfo("Conversão Concluída", resumo)
            
        except Exception as e:
            self._adicionar_log(f"\n❌ ERRO GERAL: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante conversão:\n{str(e)}")
        
        finally:
            # Fechar Word se foi criado
            if word_instance is not None:
                try:
                    self._adicionar_log("\n🔄 Fechando Microsoft Word...", "info")
                    word_instance.Quit()
                except Exception as e:
                    self._adicionar_log(f"⚠️ Erro ao fechar Word: {e}", "aviso")
            
            self.btn_converter.configure(state="normal", text="🚀 CONVERTER")
            self.conversao_ativa = False
    
    def _conversao_sequencial(self, arquivos_docx, pasta_saida, total_arquivos, word_instance):
        """Conversão sequencial (um por vez)"""
        convertidos = 0
        erros = 0
        lista_erros = []
        metodos_usados = {}
        
        for idx, arquivo_docx in enumerate(arquivos_docx, 1):
            try:
                progresso = f"[{idx}/{total_arquivos}] Convertendo: {arquivo_docx.name}"
                self._atualizar_progresso(progresso)
                self._adicionar_log(f"[{idx}/{total_arquivos}] 📄 {arquivo_docx.name}", "info")
                
                arquivo_pdf = pasta_saida / f"{arquivo_docx.stem}.pdf"
                
                sucesso, metodo_usado = self._converter_arquivo_com_fallback(
                    arquivo_docx, arquivo_pdf, word_instance
                )
                
                if sucesso:
                    self._adicionar_log(f"    ✅ Convertido com {metodo_usado}", "sucesso")
                    convertidos += 1
                    
                    if metodo_usado not in metodos_usados:
                        metodos_usados[metodo_usado] = 0
                    metodos_usados[metodo_usado] += 1
            
            except Exception as e:
                erro_msg = str(e)
                self._adicionar_log(f"    ❌ ERRO: {erro_msg}", "erro")
                erros += 1
                lista_erros.append(f"{arquivo_docx.name}: {erro_msg}")
        
        return convertidos, erros, metodos_usados, lista_erros
    
    def _conversao_paralela(self, arquivos_docx, pasta_saida, total_arquivos):
        """Conversão paralela (múltiplos simultaneamente)"""
        convertidos = 0
        erros = 0
        lista_erros = []
        metodos_usados = {}
        
        # Usar até 3 threads paralelas (não mais para não sobrecarregar)
        max_workers = min(3, total_arquivos)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Preparar tarefas
            tarefas = []
            for idx, arquivo_docx in enumerate(arquivos_docx, 1):
                args = (idx, total_arquivos, arquivo_docx, pasta_saida, None)
                future = executor.submit(self._converter_arquivo_worker, args)
                tarefas.append(future)
            
            # Processar resultados conforme completam
            for future in as_completed(tarefas):
                resultado = future.result()
                
                progresso = f"[{resultado['idx']}/{resultado['total']}] {resultado['arquivo']}"
                self._atualizar_progresso(progresso)
                self._adicionar_log(f"[{resultado['idx']}/{resultado['total']}] 📄 {resultado['arquivo']}", "info")
                
                if resultado['sucesso']:
                    self._adicionar_log(f"    ✅ Convertido com {resultado['metodo']}", "sucesso")
                    convertidos += 1
                    
                    metodo = resultado['metodo']
                    if metodo not in metodos_usados:
                        metodos_usados[metodo] = 0
                    metodos_usados[metodo] += 1
                else:
                    self._adicionar_log(f"    ❌ ERRO: {resultado['erro']}", "erro")
                    erros += 1
                    lista_erros.append(f"{resultado['arquivo']}: {resultado['erro']}")
        
        return convertidos, erros, metodos_usados, lista_erros
    
    def _thread_conversao_arquivos(self, arquivos_docx, pasta_saida):
        """Thread para conversão de arquivos selecionados"""
        self.conversao_ativa = True
        word_instance = None
        usar_word_com = "word_com" in self.metodos_disponiveis
        
        try:
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log("🚀 INICIANDO CONVERSÃO DOCX → PDF", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n📄 Modo: Arquivos selecionados", "info")
            self._adicionar_log(f"📂 Pasta de saída: {pasta_saida}", "info")
            self._adicionar_log("\n" + "-" * 80 + "\n", "info")
            
            # Criar pasta saída
            if not pasta_saida.exists():
                pasta_saida.mkdir(parents=True, exist_ok=True)
                self._adicionar_log("✅ Pasta de saída criada\n", "sucesso")
            
            total_arquivos = len(arquivos_docx)
            self._adicionar_log(f"📊 Total de arquivos: {total_arquivos}\n", "info")
            
            inicio_conversao = time.time()
            
            # Criar instância única do Word se disponível (otimização)
            if usar_word_com:
                try:
                    self._adicionar_log("⚡ Iniciando Microsoft Word (modo otimizado - sequencial)...\n", "info")
                    word_instance = win32com.client.Dispatch("Word.Application")
                    word_instance.Visible = False
                except Exception as e:
                    self._adicionar_log(f"⚠️ Não foi possível iniciar Word: {e}\n", "aviso")
                    usar_word_com = False
            
            # Se não usar Word COM, usar processamento paralelo
            if not usar_word_com and total_arquivos > 1:
                self._adicionar_log("⚡ Modo paralelo ativado (processamento simultâneo)...\n", "info")
                convertidos, erros, metodos_usados, lista_erros = self._conversao_paralela(
                    arquivos_docx, pasta_saida, total_arquivos
                )
            else:
                # Modo sequencial (Word COM)
                convertidos = 0
                erros = 0
                lista_erros = []
                metodos_usados = {}
                
                for idx, arquivo_docx in enumerate(arquivos_docx, 1):
                    try:
                        if not arquivo_docx.exists():
                            raise Exception("Arquivo não encontrado")
                        
                        progresso = f"[{idx}/{total_arquivos}] Convertendo: {arquivo_docx.name}"
                        self._atualizar_progresso(progresso)
                        self._adicionar_log(f"[{idx}/{total_arquivos}] 📄 {arquivo_docx.name}", "info")
                        
                        arquivo_pdf = pasta_saida / f"{arquivo_docx.stem}.pdf"
                        
                        sucesso, metodo_usado = self._converter_arquivo_com_fallback(
                            arquivo_docx, arquivo_pdf, word_instance
                        )
                        
                        if sucesso:
                            self._adicionar_log(f"    ✅ Convertido com {metodo_usado}", "sucesso")
                            convertidos += 1
                            
                            if metodo_usado not in metodos_usados:
                                metodos_usados[metodo_usado] = 0
                            metodos_usados[metodo_usado] += 1
                    
                    except Exception as e:
                        erro_msg = str(e)
                        self._adicionar_log(f"    ❌ ERRO: {erro_msg}", "erro")
                        erros += 1
                        lista_erros.append(f"{arquivo_docx.name}: {erro_msg}")
            
            tempo_total = time.time() - inicio_conversao
            
            # Resumo
            self._atualizar_progresso("")
            self._adicionar_log("\n" + "=" * 80, "info")
            self._adicionar_log("\n📊 RESUMO DA CONVERSÃO\n", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n✅ Convertidos: {convertidos}", "sucesso")
            self._adicionar_log(f"⏱️ Tempo total: {tempo_total:.1f}s ({tempo_total/max(convertidos, 1):.1f}s por arquivo)", "info")
            
            if metodos_usados:
                self._adicionar_log(f"\n🔧 Métodos utilizados:", "info")
                for metodo, qtd in metodos_usados.items():
                    self._adicionar_log(f"    • {metodo}: {qtd} arquivo(s)", "info")
            
            if erros > 0:
                self._adicionar_log(f"\n❌ Erros: {erros}", "erro")
            
            self._adicionar_log("\n✨ CONVERSÃO CONCLUÍDA!", "sucesso")
            
            resumo = f"Conversão concluída em {tempo_total:.1f}s!\n\nConvertidos: {convertidos}\nErros: {erros}"
            messagebox.showinfo("Conversão Concluída", resumo)
            
        except Exception as e:
            self._adicionar_log(f"\n❌ ERRO GERAL: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante conversão:\n{str(e)}")
        
        finally:
            # Fechar Word se foi criado
            if word_instance is not None:
                try:
                    self._adicionar_log("\n🔄 Fechando Microsoft Word...", "info")
                    word_instance.Quit()
                except Exception as e:
                    self._adicionar_log(f"⚠️ Erro ao fechar Word: {e}", "aviso")
            
            self.btn_converter.configure(state="normal", text="🚀 CONVERTER")
            self.conversao_ativa = False
