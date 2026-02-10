"""
Módulo de Conversão DOCX para PDF
Converte arquivos DOCX para PDF com alta qualidade
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
import traceback

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
        super().__init__(parent)
        
        # Variáveis
        self.pasta_entrada = None
        self.pasta_saida = None
        self.arquivos_selecionados = []
        self.modo_selecao = "pasta"  # "pasta" ou "arquivos"
        self.conversao_ativa = False
        
        # Detectar métodos disponíveis
        self.metodos_disponiveis = self._detectar_metodos()
        
        self._criar_interface()
    
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
    
    def _converter_com_word_com(self, arquivo_docx, arquivo_pdf):
        """Converte usando Word COM"""
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            
            doc = word.Documents.Open(str(arquivo_docx))
            doc.SaveAs(str(arquivo_pdf), FileFormat=17)
            doc.Close()
            word.Quit()
            
            return True
        except Exception as e:
            raise Exception(f"Erro no Word COM: {str(e)}")
    
    def _converter_com_docx2pdf(self, arquivo_docx, arquivo_pdf):
        """Converte usando docx2pdf"""
        try:
            docx2pdf_convert(str(arquivo_docx), str(arquivo_pdf))
            return True
        except Exception as e:
            raise Exception(f"Erro no docx2pdf: {str(e)}")
    
    def _converter_com_aspose(self, arquivo_docx, arquivo_pdf):
        """Converte usando Aspose"""
        try:
            doc = aw.Document(str(arquivo_docx))
            doc.save(str(arquivo_pdf))
            return True
        except Exception as e:
            raise Exception(f"Erro no Aspose: {str(e)}")
    
    def _converter_arquivo_com_fallback(self, arquivo_docx, arquivo_pdf):
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
                
                self._adicionar_log(f"    🔄 Tentando: {nome_metodo}...", "info")
                
                if metodo == "word_com":
                    sucesso = self._converter_com_word_com(arquivo_docx, arquivo_pdf)
                elif metodo == "docx2pdf":
                    sucesso = self._converter_com_docx2pdf(arquivo_docx, arquivo_pdf)
                elif metodo == "aspose":
                    sucesso = self._converter_com_aspose(arquivo_docx, arquivo_pdf)
                
                if sucesso:
                    return True, nome_metodo
                    
            except Exception as e:
                erro_msg = str(e)
                erros_metodos.append(f"{nome_metodo}: {erro_msg}")
                self._adicionar_log(f"    ⚠️ Falhou: {erro_msg}", "aviso")
                continue
        
        erros_completos = "\n      ".join(erros_metodos)
        raise Exception(f"Todos os métodos falharam:\n      {erros_completos}")
    
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
            
            # Processar arquivos
            convertidos = 0
            erros = 0
            lista_erros = []
            metodos_usados = {}
            
            for idx, arquivo_docx in enumerate(arquivos_docx, 1):
                try:
                    progresso = f"[{idx}/{total_arquivos}] Convertendo: {arquivo_docx.name}"
                    self._atualizar_progresso(progresso)
                    self._adicionar_log(f"\n[{idx}/{total_arquivos}] 📄 {arquivo_docx.name}", "info")
                    
                    arquivo_pdf = pasta_saida / f"{arquivo_docx.stem}.pdf"
                    
                    sucesso, metodo_usado = self._converter_arquivo_com_fallback(arquivo_docx, arquivo_pdf)
                    
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
            
            # Resumo
            self._atualizar_progresso("")
            self._adicionar_log("\n" + "=" * 80, "info")
            self._adicionar_log("\n📊 RESUMO DA CONVERSÃO\n", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n✅ Convertidos: {convertidos}", "sucesso")
            
            if metodos_usados:
                self._adicionar_log(f"\n🔧 Métodos utilizados:", "info")
                for metodo, qtd in metodos_usados.items():
                    self._adicionar_log(f"    • {metodo}: {qtd} arquivo(s)", "info")
            
            if erros > 0:
                self._adicionar_log(f"\n❌ Erros: {erros}", "erro")
            
            self._adicionar_log("\n✨ CONVERSÃO CONCLUÍDA!", "sucesso")
            
            resumo = f"Conversão concluída!\n\nConvertidos: {convertidos}\nErros: {erros}"
            messagebox.showinfo("Conversão Concluída", resumo)
            
        except Exception as e:
            self._adicionar_log(f"\n❌ ERRO GERAL: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante conversão:\n{str(e)}")
        
        finally:
            self.btn_converter.configure(state="normal", text="🚀 CONVERTER")
            self.conversao_ativa = False
    
    def _thread_conversao_arquivos(self, arquivos_docx, pasta_saida):
        """Thread para conversão de arquivos selecionados"""
        self.conversao_ativa = True
        
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
            
            # Processar arquivos
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
                    self._adicionar_log(f"\n[{idx}/{total_arquivos}] 📄 {arquivo_docx.name}", "info")
                    
                    arquivo_pdf = pasta_saida / f"{arquivo_docx.stem}.pdf"
                    
                    sucesso, metodo_usado = self._converter_arquivo_com_fallback(arquivo_docx, arquivo_pdf)
                    
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
            
            # Resumo
            self._atualizar_progresso("")
            self._adicionar_log("\n" + "=" * 80, "info")
            self._adicionar_log("\n📊 RESUMO DA CONVERSÃO\n", "sucesso")
            self._adicionar_log("=" * 80, "info")
            self._adicionar_log(f"\n✅ Convertidos: {convertidos}", "sucesso")
            
            if metodos_usados:
                self._adicionar_log(f"\n🔧 Métodos utilizados:", "info")
                for metodo, qtd in metodos_usados.items():
                    self._adicionar_log(f"    • {metodo}: {qtd} arquivo(s)", "info")
            
            if erros > 0:
                self._adicionar_log(f"\n❌ Erros: {erros}", "erro")
            
            self._adicionar_log("\n✨ CONVERSÃO CONCLUÍDA!", "sucesso")
            
            resumo = f"Conversão concluída!\n\nConvertidos: {convertidos}\nErros: {erros}"
            messagebox.showinfo("Conversão Concluída", resumo)
            
        except Exception as e:
            self._adicionar_log(f"\n❌ ERRO GERAL: {str(e)}", "erro")
            messagebox.showerror("Erro", f"Erro durante conversão:\n{str(e)}")
        
        finally:
            self.btn_converter.configure(state="normal", text="🚀 CONVERTER")
            self.conversao_ativa = False
