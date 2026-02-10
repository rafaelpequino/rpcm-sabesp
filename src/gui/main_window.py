"""
Janela principal da aplicação - Sistema Unificado de Automações
Integra: Gerador de RPCM, Organizador de Lotes e Conversor DOCX → PDF
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from typing import Optional
import sys
import logging
import pyperclip

from src.gui.styles import COLORS, FONTS, SPACING, WINDOW, CTK_THEME
from src.gui.organizador_lotes import OrganizadorLotesFrame
from src.gui.conversor_pdf import ConversorPdfFrame
from src.utils.validators import Validator
from src.utils.logger_config import setup_logger
from src.utils.config_manager import ConfigManager
from src.core.document_generator import DocumentGenerator, BatchDocumentGenerator, DocumentGenerationError
from src.models.documento_rpcm import DocumentoRPCM

# Configurar logger
logger = setup_logger()


class MainWindow(ctk.CTk):
    """Janela principal da aplicação - Sistema Unificado de Automações - RPCMS - EPC Sabesp"""
    
    def __init__(self):
        super().__init__()
        
        # Configurar tema
        ctk.set_appearance_mode(CTK_THEME['appearance_mode'])
        ctk.set_default_color_theme(CTK_THEME['color_theme'])
        
        # Configurações da janela
        self.title("Sistema Unificado de Automações - RPCMS - EPC Sabesp")
        self.geometry(f"{WINDOW['default_width']}x{WINDOW['default_height']}")
        self.minsize(WINDOW['min_width'], WINDOW['min_height'])
        
        # Variáveis de controle
        self.lista_documentos = []  # Lista de documentos
        self.template_path = None  # Caminho do template selecionado
        self.aba_atual = "rpcm"  # Aba ativa (rpcm, lotes, conversor)
        
        # Inicializar geradores
        self.generator = None
        self.batch_generator = None
        self.template_valido = self._inicializar_geradores()
        
        # Criar interface
        self._criar_interface()
        
        # Atualizar status inicial
        if self.template_valido:
            self.update_status("Sistema pronto ✓", "success")
        else:
            self.update_status("⚠ Template RPCM não encontrado - coloque template_rpcm.docx na pasta templates/", "error")
    
    def _inicializar_geradores(self) -> bool:
        """Inicializa os geradores de documentos"""
        try:
            self.generator = DocumentGenerator()
            self.batch_generator = BatchDocumentGenerator()
            logger.info("Geradores inicializados com sucesso")
            return True
        except FileNotFoundError as e:
            logger.error(f"Template não encontrado: {e}")
            messagebox.showerror(
                "Template não encontrado",
                "O arquivo template_rpcm.docx não foi encontrado na pasta templates/.\n\n"
                "Por favor, coloque o template nesta pasta e reinicie a aplicação.\n\n"
                "Consulte templates/README.md para instruções."
            )
            return False
        except Exception as e:
            logger.error(f"Erro ao inicializar geradores: {e}", exc_info=True)
            messagebox.showerror(
                "Erro de Inicialização",
                f"Erro ao inicializar sistema:\n{str(e)}"
            )
            return False
    
    def _criar_interface(self):
        """Cria todos os componentes da interface com navegação por abas"""
        
        # ===== NAVEGAÇÃO SUPERIOR (NAVBAR) =====
        self.navbar = ctk.CTkFrame(self, height=70)
        self.navbar.pack(fill="x", padx=0, pady=0)
        self.navbar.pack_propagate(False)
        
        # Título principal
        titulo_frame = ctk.CTkFrame(self.navbar)
        titulo_frame.pack(side="left", padx=20, pady=10)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="🏢 Sistema Unificado de Automações - RPCMS - EPC Sabesp",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS['primary']
        )
        titulo.pack()
        
        # Botões de navegação
        botoes_frame = ctk.CTkFrame(self.navbar)
        botoes_frame.pack(side="right", padx=20, pady=10)
        
        self.btn_nav_rpcm = ctk.CTkButton(
            botoes_frame,
            text="📄 Gerador de RPCM",
            command=lambda: self._trocar_aba("rpcm"),
            width=180,
            height=45,
            font=FONTS['button'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['hover']
        )
        self.btn_nav_rpcm.pack(side="left", padx=5)
        
        self.btn_nav_conversor = ctk.CTkButton(
            botoes_frame,
            text="🔄 Conversor DOCX → PDF",
            command=lambda: self._trocar_aba("conversor"),
            width=180,
            height=45,
            font=FONTS['button'],
            fg_color=COLORS['secondary'],
            hover_color=COLORS['border'],
            text_color=COLORS['text']
        )
        self.btn_nav_conversor.pack(side="left", padx=5)
        
        self.btn_nav_lotes = ctk.CTkButton(
            botoes_frame,
            text="📁 Organizador de Lotes",
            command=lambda: self._trocar_aba("lotes"),
            width=180,
            height=45,
            font=FONTS['button'],
            fg_color=COLORS['secondary'],
            hover_color=COLORS['border'],
            text_color=COLORS['text']
        )
        self.btn_nav_lotes.pack(side="left", padx=5)
        
        # ===== BARRA DE STATUS (criar antes para poder usar update_status) =====
        self._criar_barra_status()
        
        # ===== CONTAINER PRINCIPAL PARA ABAS =====
        self.container_abas = ctk.CTkFrame(self)
        self.container_abas.pack(fill="both", expand=True, before=self.status_frame)
        
        # ===== CRIAR AS ABAS =====
        # Aba RPCM (gerador de documentos)
        self.frame_rpcm = ctk.CTkScrollableFrame(self.container_abas)
        self._criar_conteudo_rpcm()
        
        # Aba Organizador de Lotes
        self.frame_lotes = OrganizadorLotesFrame(self.container_abas)
        
        # Aba Conversor PDF
        self.frame_conversor = ConversorPdfFrame(self.container_abas)
        
        # Mostrar aba inicial (RPCM)
        self._trocar_aba("rpcm")
    
    def _trocar_aba(self, aba: str):
        """Troca a aba ativa"""
        self.aba_atual = aba
        
        # Esconder todas as abas
        self.frame_rpcm.pack_forget()
        self.frame_lotes.pack_forget()
        self.frame_conversor.pack_forget()
        
        # Resetar cores dos botões
        self.btn_nav_rpcm.configure(
            fg_color=COLORS['secondary'],
            text_color=COLORS['text']
        )
        self.btn_nav_lotes.configure(
            fg_color=COLORS['secondary'],
            text_color=COLORS['text']
        )
        self.btn_nav_conversor.configure(
            fg_color=COLORS['secondary'],
            text_color=COLORS['text']
        )
        
        # Mostrar aba selecionada e destacar botão
        if aba == "rpcm":
            self.frame_rpcm.pack(fill="both", expand=True, padx=SPACING['padding'], pady=SPACING['padding'])
            self.btn_nav_rpcm.configure(
                fg_color=COLORS['primary'],
                text_color=COLORS['secondary']
            )
            self.update_status("Gerador de RPCM ativo", "info")
        elif aba == "lotes":
            self.frame_lotes.pack(fill="both", expand=True)
            self.btn_nav_lotes.configure(
                fg_color=COLORS['primary'],
                text_color=COLORS['secondary']
            )
            self.update_status("Organizador de Lotes ativo", "info")
        elif aba == "conversor":
            self.frame_conversor.pack(fill="both", expand=True)
            self.btn_nav_conversor.configure(
                fg_color=COLORS['primary'],
                text_color=COLORS['secondary']
            )
            self.update_status("Conversor DOCX → PDF ativo", "info")
    
    def _criar_conteudo_rpcm(self):
        """Cria o conteúdo da aba de Gerador de RPCM"""
        
        # 1. Seleção de Template
        self._criar_secao_template()
        
        # 2. Campos de Entrada
        self._criar_campos_entrada()
        
        # 3. Botão Adicionar
        self._criar_botao_adicionar()
        
        # 4. Tabela de Lista
        self._criar_tabela_lista()
        
        # 5. Botões de Ação
        self._criar_botoes_acao()
    
    def _criar_secao_template(self):
        """Cria a seção de seleção de template"""
        frame = ctk.CTkFrame(self.frame_rpcm)
        frame.pack(fill="x", pady=(0, SPACING['margin']))
        
        label = ctk.CTkLabel(
            frame, 
            text="📄 TEMPLATE", 
            font=FONTS['subtitle']
        )
        label.pack(pady=SPACING['small_margin'], anchor="w", padx=10)
        
        # Container para o botão e label do arquivo
        container = ctk.CTkFrame(frame)
        container.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botão Selecionar Template
        btn_selecionar = ctk.CTkButton(
            container,
            text="📁 Selecionar Template",
            command=self._on_selecionar_template,
            font=FONTS['button'],
            height=35,
            width=200,
            fg_color=COLORS['info'],
            hover_color="#138496"
        )
        btn_selecionar.pack(side="left", padx=10, pady=10)
        
        # Label mostrando o template atual
        self.label_template_atual = ctk.CTkLabel(
            container,
            text=self._get_texto_template_status(),
            font=FONTS['small'],
            text_color=COLORS['warning'] if not self.template_valido else COLORS['success'],
            anchor="w"
        )
        self.label_template_atual.pack(side="left", padx=10, fill="x", expand=True)
    
    def _get_texto_template_status(self) -> str:
        """Retorna o texto de status do template"""
        if not self.template_valido:
            return "⚠ Nenhum template selecionado"
        
        if self.template_path:
            # Template customizado
            return f"✓ Template: {Path(self.template_path).name}"
        else:
            # Template padrão
            return "✓ Template padrão: template_rpcm.docx"
    
    def _criar_campos_entrada(self):
        """Cria os campos de entrada de dados"""
        frame = ctk.CTkFrame(self.frame_rpcm)
        frame.pack(fill="x", pady=SPACING['margin'])
        
        label = ctk.CTkLabel(
            frame, 
            text="DADOS DO DOCUMENTO", 
            font=FONTS['subtitle']
        )
        label.pack(pady=SPACING['small_margin'], anchor="w", padx=10)
        
        # Container dos campos
        campos_frame = ctk.CTkFrame(frame)
        campos_frame.pack(fill="x", padx=10, pady=10)
        
        # Grupo *
        self._criar_campo(campos_frame, "Grupo:", "grupo", obrigatorio=True)
        
        # Subgrupo (opcional)
        self._criar_campo(campos_frame, "Subgrupo:", "subgrupo", obrigatorio=False)
        
        # Nº Preço *
        self._criar_campo(campos_frame, "Nº Preço:", "numero_preco", obrigatorio=True, 
                         placeholder="123456")
        
        # Descrição *
        self._criar_campo(campos_frame, "Descrição:", "descricao", obrigatorio=True)
        
        # Unidade *
        self._criar_campo(campos_frame, "Unidade:", "unidade", obrigatorio=True, 
                         placeholder="m, un, kg, etc")
    
    def _criar_campo(self, parent, label_text: str, field_name: str, 
                     obrigatorio: bool = False, placeholder: str = ""):
        """
        Cria um campo de entrada com label
        
        Args:
            parent: Widget pai
            label_text: Texto do label
            field_name: Nome do campo (para referência)
            obrigatorio: Se o campo é obrigatório
            placeholder: Texto placeholder
        """
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", pady=SPACING['small_margin'])
        
        # Label com indicador de obrigatório
        label_str = f"{label_text} *" if obrigatorio else label_text
        label = ctk.CTkLabel(row, text=label_str, font=FONTS['label'], width=120, anchor="w")
        label.pack(side="left", padx=(10, 5))
        
        # Campo de entrada
        entry = ctk.CTkEntry(
            row, 
            height=SPACING['field_height'],
            placeholder_text=placeholder,
            font=FONTS['input']
        )
        entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
        
        # Salvar referência ao campo
        setattr(self, f"entry_{field_name}", entry)
        
        # Label de erro (inicialmente oculto)
        error_label = ctk.CTkLabel(
            row, 
            text="", 
            font=FONTS['small'],
            text_color=COLORS['error']
        )
        error_label.pack(side="left", padx=5)
        setattr(self, f"error_{field_name}", error_label)
    
    def _criar_botao_adicionar(self):
        """Cria o botão Adicionar à Lista e Copiar do Excel"""
        self.frame_adicionar = ctk.CTkFrame(self.frame_rpcm)
        self.frame_adicionar.pack(fill="x", pady=SPACING['margin'])
        
        # Container para os botões lado a lado
        botoes_container = ctk.CTkFrame(self.frame_adicionar)
        botoes_container.pack(pady=10)
        
        self.btn_adicionar = ctk.CTkButton(
            botoes_container,
            text="➕ Adicionar à Lista",
            command=self._on_adicionar_lista,
            font=FONTS['button'],
            height=35,
            width=200
        )
        self.btn_adicionar.pack(side="left", padx=5)
        
        self.btn_copiar_excel = ctk.CTkButton(
            botoes_container,
            text="📋 Copiar do Excel",
            command=self._on_copiar_excel,
            font=FONTS['button'],
            height=35,
            width=200,
            fg_color=COLORS['info'],
            hover_color="#138496"
        )
        self.btn_copiar_excel.pack(side="left", padx=5)
    
    def _criar_tabela_lista(self):
        """Cria a tabela de lista de documentos"""
        self.frame_lista = ctk.CTkFrame(self.frame_rpcm)
        self.frame_lista.pack(fill="both", expand=True, pady=SPACING['margin'])
        
        label = ctk.CTkLabel(
            self.frame_lista, 
            text="LISTA DE DOCUMENTOS", 
            font=FONTS['subtitle']
        )
        label.pack(pady=SPACING['small_margin'], anchor="w", padx=10)
        
        # Frame da tabela com scroll
        self.tabela_scroll = ctk.CTkScrollableFrame(self.frame_lista, height=200)
        self.tabela_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho da tabela
        header = ctk.CTkFrame(self.tabela_scroll)
        header.pack(fill="x", pady=(0, 5))
        
        headers = ["Nº Preço", "Grupo", "Subgrupo", "Descrição", "Unidade", "Ação"]
        widths = [100, 120, 120, 200, 80, 80]
        
        for header_text, width in zip(headers, widths):
            label = ctk.CTkLabel(
                header, 
                text=header_text, 
                font=FONTS['label'],
                width=width
            )
            label.pack(side="left", padx=2)
        
        # Container para as linhas
        self.linhas_container = ctk.CTkFrame(self.tabela_scroll)
        self.linhas_container.pack(fill="both", expand=True)
    
    def _criar_botoes_acao(self):
        """Cria os botões de ação principais"""
        self.frame_botoes = ctk.CTkFrame(self.frame_rpcm)
        self.frame_botoes.pack(fill="x", pady=SPACING['margin'])
        
        # Botão Gerar Documentos
        self.btn_gerar = ctk.CTkButton(
            self.frame_botoes,
            text="📄 Gerar Documentos",
            command=self._gerar_documentos_lote,
            font=FONTS['button'],
            height=40,
            fg_color=COLORS['success'],
            hover_color="#218838"
        )
        self.btn_gerar.pack(side="left", padx=5, pady=10, expand=True, fill="x")
        
        # Desabilitar se template não existe
        if not self.template_valido:
            self.btn_gerar.configure(state="disabled")
        
        # Botão Limpar
        self.btn_limpar = ctk.CTkButton(
            self.frame_botoes,
            text="🗑️ Limpar Tudo",
            command=self._on_limpar_tudo,
            font=FONTS['button'],
            height=40,
            fg_color=COLORS['warning'],
            hover_color="#e0a800"
        )
        self.btn_limpar.pack(side="left", padx=5, pady=10, expand=True, fill="x")
    
    def _criar_barra_status(self):
        """Cria a barra de status no rodapé"""
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Sistema iniciando...",
            font=FONTS['small'],
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    # ===== MÉTODOS DE CONTROLE =====
    
    def _on_adicionar_lista(self):
        """Handler para adicionar item à lista (Modo Lote)"""
        # Coletar dados dos campos
        grupo = self.entry_grupo.get().strip()
        subgrupo = self.entry_subgrupo.get().strip()
        numero_preco = self.entry_numero_preco.get().strip()
        descricao = self.entry_descricao.get().strip()
        unidade = self.entry_unidade.get().strip()
        
        # Validar campos
        valid, errors = Validator.validate_all_fields(
            grupo, subgrupo, numero_preco, descricao, unidade
        )
        
        if not valid:
            messagebox.showerror(
                "Validação",
                "Erros encontrados:\n\n" + "\n".join(f"• {e}" for e in errors)
            )
            return
        
        # Verificar duplicata (mesmo nº preço)
        for doc in self.lista_documentos:
            if doc['numero_preco'] == numero_preco:
                messagebox.showwarning(
                    "Duplicata",
                    f"Número de Preço {numero_preco} já está na lista!"
                )
                return
        
        # Adicionar à lista
        documento = {
            'grupo': grupo,
            'subgrupo': subgrupo,
            'numero_preco': numero_preco,
            'descricao': descricao,
            'unidade': unidade
        }
        self.lista_documentos.append(documento)
        
        # Adicionar à tabela visual
        self._adicionar_linha_tabela(documento)
        
        # Limpar campos (exceto regulamentação)
        self._limpar_campos_dados()
        
        # Focar no primeiro campo
        self.entry_grupo.focus()
        
        self.update_status(f"Item adicionado: {numero_preco} ({len(self.lista_documentos)} na lista)", "success")
    
    def _on_copiar_excel(self):
        """Handler para copiar dados do Excel via clipboard"""
        try:
            # Ler dados do clipboard
            clipboard_data = pyperclip.paste()
            
            if not clipboard_data or not clipboard_data.strip():
                messagebox.showwarning(
                    "Clipboard Vazio",
                    "Não há dados copiados.\n\n"
                    "Copie os dados do Excel (Ctrl+C) e tente novamente."
                )
                return
            
            # Parsear dados (formato TSV - Tab Separated Values)
            linhas = clipboard_data.strip().split('\n')
            
            # Verificar se há dados
            if not linhas:
                messagebox.showwarning(
                    "Sem Dados",
                    "Nenhuma linha encontrada nos dados copiados."
                )
                return
            
            # Processar cada linha
            itens_adicionados = 0
            itens_duplicados = 0
            erros = []
            
            for i, linha in enumerate(linhas, 1):
                # Separar por TAB
                colunas = linha.split('\t')
                
                # Verificar se tem 5 colunas (Grupo, Subgrupo, Nº Preço, Descrição, Unidade)
                if len(colunas) < 5:
                    erros.append(f"Linha {i}: formato inválido (esperado 5 colunas, encontrado {len(colunas)})")
                    continue
                
                grupo = colunas[0].strip()
                subgrupo = colunas[1].strip()
                numero_preco = colunas[2].strip()
                descricao = colunas[3].strip()
                unidade = colunas[4].strip()
                
                # Pular linha de cabeçalho (se existir)
                if numero_preco.upper() in ['Nº PREÇO', 'N° PREÇO', 'NUMERO PRECO', 'N PRECO']:
                    continue
                
                # Validar campos obrigatórios
                valid, validation_errors = Validator.validate_all_fields(
                    grupo, subgrupo, numero_preco, descricao, unidade
                )
                
                if not valid:
                    erros.append(f"Linha {i} ({numero_preco}): {', '.join(validation_errors)}")
                    continue
                
                # Verificar duplicata
                duplicado = False
                for doc in self.lista_documentos:
                    if doc['numero_preco'] == numero_preco:
                        itens_duplicados += 1
                        duplicado = True
                        break
                
                if duplicado:
                    continue
                
                # Adicionar à lista
                documento = {
                    'grupo': grupo,
                    'subgrupo': subgrupo,
                    'numero_preco': numero_preco,
                    'descricao': descricao,
                    'unidade': unidade
                }
                self.lista_documentos.append(documento)
                self._adicionar_linha_tabela(documento)
                itens_adicionados += 1
            
            # Mostrar resultado
            mensagem = f"✓ {itens_adicionados} itens adicionados à lista"
            
            if itens_duplicados > 0:
                mensagem += f"\n⚠ {itens_duplicados} itens duplicados ignorados"
            
            if erros:
                mensagem += f"\n\n✗ {len(erros)} erros encontrados:"
                for erro in erros[:5]:  # Mostrar até 5 erros
                    mensagem += f"\n  • {erro}"
                if len(erros) > 5:
                    mensagem += f"\n  ... e mais {len(erros) - 5} erros"
            
            if itens_adicionados > 0:
                messagebox.showinfo("Importação Concluída", mensagem)
                self.update_status(f"✓ {itens_adicionados} itens importados do Excel", "success")
            else:
                messagebox.showwarning("Nenhum Item Adicionado", mensagem)
                self.update_status("⚠ Nenhum item válido encontrado", "warning")
                
        except Exception as e:
            logger.error(f"Erro ao copiar do Excel: {e}", exc_info=True)
            messagebox.showerror(
                "Erro",
                f"Erro ao processar dados do clipboard:\n\n{str(e)}\n\n"
                "Certifique-se de copiar os dados diretamente do Excel."
            )
            self.update_status("✗ Erro ao importar dados", "error")
    
    def _on_selecionar_template(self):
        """Handler para selecionar arquivo de template"""
        # Abrir diálogo para selecionar arquivo
        arquivo = filedialog.askopenfilename(
            title="Selecionar Template DOCX",
            filetypes=[
                ("Word Documents", "*.docx"),
                ("Todos os arquivos", "*.*")
            ],
            initialdir=Path.cwd() / "templates" if (Path.cwd() / "templates").exists() else Path.cwd()
        )
        
        if not arquivo:
            return  # Usuário cancelou
        
        arquivo_path = Path(arquivo)
        
        # Validar arquivo
        if not arquivo_path.exists():
            messagebox.showerror(
                "Arquivo não encontrado",
                f"O arquivo selecionado não existe:\n{arquivo}"
            )
            return
        
        if arquivo_path.suffix.lower() != '.docx':
            messagebox.showwarning(
                "Formato inválido",
                "Por favor, selecione um arquivo .docx válido."
            )
            return
        
        # Tentar carregar o template
        try:
            # Testar se o arquivo é um template válido
            from docxtpl import DocxTemplate
            DocxTemplate(str(arquivo_path))
            
            # Template válido - salvar caminho
            self.template_path = str(arquivo_path)
            
            # Reinicializar geradores com novo template
            try:
                self.generator = DocumentGenerator(self.template_path)
                self.batch_generator = BatchDocumentGenerator(self.template_path)
                self.template_valido = True
                
                # Habilitar botão gerar
                self.btn_gerar.configure(state="normal")
                
                # Atualizar label
                self.label_template_atual.configure(
                    text=self._get_texto_template_status(),
                    text_color=COLORS['success']
                )
                
                # Atualizar status
                self.update_status(f"✓ Template carregado: {arquivo_path.name}", "success")
                
                messagebox.showinfo(
                    "Template Carregado",
                    f"Template carregado com sucesso!\n\n{arquivo_path.name}"
                )
                
                logger.info(f"Template customizado carregado: {arquivo_path}")
                
            except Exception as e:
                logger.error(f"Erro ao inicializar geradores: {e}", exc_info=True)
                messagebox.showerror(
                    "Erro ao Carregar Template",
                    f"Erro ao inicializar geradores com o template:\n\n{str(e)}"
                )
                self.template_valido = False
                self.btn_gerar.configure(state="disabled")
                self.update_status("✗ Erro ao carregar template", "error")
        
        except Exception as e:
            logger.error(f"Erro ao validar template: {e}", exc_info=True)
            messagebox.showerror(
                "Template Inválido",
                f"O arquivo selecionado não é um template válido:\n\n{str(e)}\n\n"
                "Certifique-se de que é um arquivo .docx válido."
            )
            self.update_status("✗ Template inválido", "error")
    
    def _adicionar_linha_tabela(self, documento: dict):
        """Adiciona uma linha à tabela visual"""
        linha = ctk.CTkFrame(self.linhas_container)
        linha.pack(fill="x", pady=2)
        
        # Células
        widths = [100, 120, 120, 200, 80, 80]
        valores = [
            documento['numero_preco'],
            documento['grupo'],
            documento['subgrupo'] or "(vazio)",
            documento['descricao'],
            documento['unidade']
        ]
        
        for valor, width in zip(valores, widths[:-1]):
            label = ctk.CTkLabel(
                linha,
                text=valor,
                font=FONTS['small'],
                width=width,
                anchor="w"
            )
            label.pack(side="left", padx=2)
        
        # Botão remover
        btn_remover = ctk.CTkButton(
            linha,
            text="❌",
            width=widths[-1],
            command=lambda: self._remover_item_lista(documento['numero_preco'], linha),
            fg_color=COLORS['error'],
            hover_color="#c82333"
        )
        btn_remover.pack(side="left", padx=2)
    
    def _remover_item_lista(self, numero_preco: str, linha_widget):
        """Remove item da lista"""
        # Remover da lista de dados
        self.lista_documentos = [
            doc for doc in self.lista_documentos 
            if doc['numero_preco'] != numero_preco
        ]
        
        # Remover da interface
        linha_widget.destroy()
        
        self.update_status(f"Item removido: {numero_preco} ({len(self.lista_documentos)} na lista)", "info")
    
    def _limpar_campos_dados(self):
        """Limpa apenas os campos de dados (mantém regulamentação)"""
        self.entry_grupo.delete(0, 'end')
        self.entry_subgrupo.delete(0, 'end')
        self.entry_numero_preco.delete(0, 'end')
        self.entry_descricao.delete(0, 'end')
        self.entry_unidade.delete(0, 'end')
    
    def _gerar_documentos_lote(self):
        """Gera múltiplos documentos"""
        # Verificar se há itens na lista
        if not self.lista_documentos:
            messagebox.showwarning(
                "Lista vazia",
                "Adicione pelo menos um documento à lista antes de gerar."
            )
            return
        
        # Selecionar pasta de destino
        pasta = filedialog.askdirectory(
            title="Selecionar pasta para salvar documentos"
        )
        
        if not pasta:
            return  # Usuário cancelou
        
        # Gerar documentos REALMENTE
        total = len(self.lista_documentos)
        self.btn_gerar.configure(state="disabled")
        
        # Limpar lista do batch generator e adicionar todos os documentos
        self.batch_generator.limpar_lista()
        
        try:
            # Adicionar todos os documentos ao batch generator
            for doc_dict in self.lista_documentos:
                documento = DocumentoRPCM(
                    grupo=doc_dict['grupo'],
                    subgrupo=doc_dict.get('subgrupo', ''),  # Pode estar vazio
                    numero_preco=doc_dict['numero_preco'],
                    descricao=doc_dict['descricao'],
                    unidade=doc_dict['unidade']
                )
                self.batch_generator.adicionar_documento(documento)
            
            # Callback de progresso
            def atualizar_progresso(atual, total_docs, nome_arquivo):
                self.update_status(f"⏳ Gerando {nome_arquivo} ({atual}/{total_docs})...", "info")
                self.update()  # Forçar atualização da interface
            
            # Gerar todos os documentos
            resultados = self.batch_generator.gerar_todos(pasta, atualizar_progresso)
            
            # Montar mensagem de resultado
            mensagem = f"Geração em lote concluída!\n\n"
            mensagem += f"✓ Sucesso: {resultados['sucesso']}\n"
            
            if resultados['erro'] > 0:
                mensagem += f"✗ Erros: {resultados['erro']}\n\n"
                mensagem += "Documentos com erro:\n"
                for erro in resultados['erros'][:5]:  # Mostrar até 5
                    mensagem += f"  • {erro['numero_preco']}: {erro['erro']}\n"
            
            messagebox.showinfo("Geração Concluída", mensagem)
            
            self.update_status(
                f"✓ {resultados['sucesso']} documentos gerados com sucesso",
                "success" if resultados['erro'] == 0 else "warning"
            )
        
        except DocumentGenerationError as e:
            logger.error(f"Erro na geração em lote: {e}")
            messagebox.showerror("Erro na Geração", f"Erro ao gerar documentos:\n\n{str(e)}")
            self.update_status("✗ Erro na geração em lote", "error")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao gerar documentos:\n{e}")
            self.update_status("✗ Erro na geração em lote", "error")
        
        finally:
            self.btn_gerar.configure(state="normal")
    
    def _on_limpar_tudo(self):
        """Handler para limpar tudo"""
        if messagebox.askyesno("Confirmar", "Deseja limpar todos os campos e a lista?"):
            # Limpar campos
            self._limpar_campos_dados()
            
            # Limpar lista
            self.lista_documentos.clear()
            for widget in self.linhas_container.winfo_children():
                widget.destroy()
            
            self.update_status("Formulário limpo", "info")
    
    def _on_importar_excel(self):
        """Handler para importar Excel"""
        # Selecionar arquivo
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo Excel/CSV",
            filetypes=[
                ("Excel", "*.xlsx"),
                ("Excel 97-2003", "*.xls"),
                ("CSV", "*.csv"),
                ("Todos", "*.*")
            ]
        )
        
        if not arquivo:
            return
        
        # Importar REALMENTE via batch_generator
        self.update_status("⏳ Importando dados...", "info")
        
        try:
            num_importados = self.batch_generator.importar_excel(arquivo)
            
            # Atualizar lista visual e lista_documentos
            self.lista_documentos.clear()
            for widget in self.linhas_container.winfo_children():
                widget.destroy()
            
            # Adicionar à lista visual
            for documento in self.batch_generator.documentos:
                doc_dict = {
                    'grupo': documento.grupo,
                    'subgrupo': documento.subgrupo,
                    'numero_preco': documento.numero_preco,
                    'descricao': documento.descricao,
                    'unidade': documento.unidade
                }
                self.lista_documentos.append(doc_dict)
                self._adicionar_linha_tabela(doc_dict)
            
            messagebox.showinfo(
                "Importação Concluída",
                f"✓ {num_importados} documentos importados com sucesso!"
            )
            self.update_status(f"✓ {num_importados} itens importados", "success")
            
        except ImportError as e:
            logger.error(f"Erro ao importar: {e}")
            messagebox.showerror("Erro na Importação", str(e))
            self.update_status("✗ Erro ao importar arquivo", "error")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro inesperado:\n{e}")
            self.update_status("✗ Erro na importação", "error")
    
    def update_status(self, message: str, tipo: str = "info"):
        """
        Atualiza a barra de status
        
        Args:
            message: Mensagem a exibir
            tipo: Tipo da mensagem (info, success, error, warning)
        """
        self.status_label.configure(text=message)
        
        # Mudar cor baseado no tipo
        colors_map = {
            'info': COLORS['info'],
            'success': COLORS['success'],
            'error': COLORS['error'],
            'warning': COLORS['warning']
        }
        self.status_label.configure(text_color=colors_map.get(tipo, COLORS['text']))


def main():
    """Função principal para iniciar a aplicação"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
