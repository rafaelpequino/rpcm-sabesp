"""
Janela principal da aplicação
Interface completa com modo Individual e Lote
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from pathlib import Path
from typing import Optional
import sys
import logging

from src.gui.styles import COLORS, FONTS, SPACING, WINDOW, CTK_THEME
from src.utils.validators import Validator
from src.utils.logger_config import setup_logger
from src.utils.config_manager import ConfigManager
from src.core.document_generator import DocumentGenerator, BatchDocumentGenerator, DocumentGenerationError
from src.models.documento_rpcm import DocumentoRPCM

# Configurar logger
logger = setup_logger()


class MainWindow(ctk.CTk):
    """Janela principal da aplicação Automação RPCM"""
    
    def __init__(self):
        super().__init__()
        
        # Configurar tema
        ctk.set_appearance_mode(CTK_THEME['appearance_mode'])
        ctk.set_default_color_theme(CTK_THEME['color_theme'])
        
        # Configurações da janela
        self.title("Automação RPCM - Sabesp")
        self.geometry(f"{WINDOW['default_width']}x{WINDOW['default_height']}")
        self.minsize(WINDOW['min_width'], WINDOW['min_height'])
        
        # Variáveis de controle
        self.modo_var = ctk.StringVar(value="individual")
        self.lista_documentos = []  # Lista de documentos no modo lote
        
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
            self.update_status("⚠ Template não encontrado - coloque template_rpcm.docx na pasta templates/", "error")
    
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
        """Cria todos os componentes da interface"""
        
        # Container principal com scroll
        self.main_container = ctk.CTkScrollableFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=SPACING['padding'], pady=SPACING['padding'])
        
        # 1. Seletor de Modo
        self._criar_seletor_modo()
        
        # 2. Campos de Entrada
        self._criar_campos_entrada()
        
        # 3. Botão Adicionar (Modo Lote)
        self._criar_botao_adicionar()
        
        # 4. Tabela de Lista (Modo Lote)
        self._criar_tabela_lista()
        
        # 5. Área do Editor
        self._criar_area_editor()
        
        # 6. Botões de Ação (CRIAR MAS NÃO EMPACOTAR AINDA)
        self._criar_botoes_acao()
        
        # 7. Barra de Status
        self._criar_barra_status()
        
        # 8. AGORA SIM empacotar os botões no final
        self.frame_botoes.pack(fill="x", pady=SPACING['margin'])
    
    def _criar_seletor_modo(self):
        """Cria o seletor de modo (Individual/Lote)"""
        frame = ctk.CTkFrame(self.main_container)
        frame.pack(fill="x", pady=(0, SPACING['margin']))
        
        label = ctk.CTkLabel(
            frame, 
            text="MODO DE OPERAÇÃO", 
            font=FONTS['subtitle']
        )
        label.pack(pady=SPACING['small_margin'])
        
        # Radio buttons
        radio_frame = ctk.CTkFrame(frame)
        radio_frame.pack(pady=SPACING['small_margin'])
        
        self.radio_individual = ctk.CTkRadioButton(
            radio_frame,
            text="⚪ Modo Individual",
            variable=self.modo_var,
            value="individual",
            command=self._on_modo_changed,
            font=FONTS['label']
        )
        self.radio_individual.pack(side="left", padx=20, pady=10)
        
        self.radio_lote = ctk.CTkRadioButton(
            radio_frame,
            text="🔵 Modo Lote",
            variable=self.modo_var,
            value="lote",
            command=self._on_modo_changed,
            font=FONTS['label']
        )
        self.radio_lote.pack(side="left", padx=20, pady=10)
    
    def _criar_campos_entrada(self):
        """Cria os campos de entrada de dados"""
        frame = ctk.CTkFrame(self.main_container)
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
        """Cria o botão Adicionar à Lista (Modo Lote)"""
        self.frame_adicionar = ctk.CTkFrame(self.main_container)
        # Inicialmente oculto (só aparece no modo lote)
        
        self.btn_adicionar = ctk.CTkButton(
            self.frame_adicionar,
            text="➕ Adicionar à Lista",
            command=self._on_adicionar_lista,
            font=FONTS['button'],
            height=35
        )
        self.btn_adicionar.pack(pady=10)
    
    def _criar_tabela_lista(self):
        """Cria a tabela de lista de documentos (Modo Lote)"""
        self.frame_lista = ctk.CTkFrame(self.main_container)
        # Inicialmente oculto
        
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
    
    def _criar_area_editor(self):
        """Cria área placeholder para o editor (será implementado na Etapa 2)"""
        self.frame_editor = ctk.CTkFrame(self.main_container)
        self.frame_editor.pack(fill="both", expand=True, pady=SPACING['margin'])
        
        label = ctk.CTkLabel(
            self.frame_editor, 
            text="REGULAMENTAÇÃO", 
            font=FONTS['subtitle']
        )
        label.pack(pady=SPACING['small_margin'], anchor="w", padx=10)
        
        # Texto informativo
        info_label = ctk.CTkLabel(
            self.frame_editor,
            text="ℹ️ Editor de Texto Rico será implementado na Etapa 2\n"
                 "Suportará colar do Word/PDF com formatação perfeita\n"
                 "Espaçamento 1,5 e Arial 10pt automáticos",
            font=FONTS['small'],
            text_color=COLORS['info'],
            justify="left"
        )
        info_label.pack(pady=10, padx=10)
        
        # Caixa de texto temporária
        self.text_regulamentacao = ctk.CTkTextbox(
            self.frame_editor,
            height=200,
            font=FONTS['input']
        )
        self.text_regulamentacao.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Inserir texto placeholder
        self.text_regulamentacao.insert("1.0", 
            "Digite ou cole aqui a regulamentação do documento...\n\n"
            "(Na Etapa 2, este será substituído por um editor WYSIWYG profissional)"
        )
    
    def _criar_botoes_acao(self):
        """Cria os botões de ação principais (mas NÃO empacota ainda)"""
        self.frame_botoes = ctk.CTkFrame(self.main_container)
        # NÃO fazer .pack() aqui! Será feito manualmente no final de _criar_interface
        
        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(
            self.frame_botoes,
            text="📄 Gerar Documento",
            command=self._on_gerar_documento,
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
    
    def _on_modo_changed(self):
        """Handler quando o modo é alterado"""
        modo = self.modo_var.get()
        
        if modo == "lote":
            # Desempacotar o editor e botões primeiro para reposicionar
            self.frame_editor.pack_forget()
            self.frame_botoes.pack_forget()
            
            # Mostrar elementos do modo lote NA ORDEM CORRETA
            self.frame_adicionar.pack(fill="x", pady=SPACING['margin'])
            self.frame_lista.pack(fill="both", expand=True, pady=SPACING['margin'])
            
            # Reempacotar o editor DEPOIS da lista
            self.frame_editor.pack(fill="both", expand=True, pady=SPACING['margin'])
            
            # Reempacotar os botões NO FINAL (por último)
            self.frame_botoes.pack(fill="x", pady=SPACING['margin'])
            
            self.btn_gerar.configure(text="📄 Gerar Documentos")
            self.update_status("Modo Lote ativado", "info")
        else:
            # Esconder elementos do modo lote
            self.frame_adicionar.pack_forget()
            self.frame_lista.pack_forget()
            
            # Reempacotar botões no final do modo individual também
            self.frame_botoes.pack_forget()
            self.frame_botoes.pack(fill="x", pady=SPACING['margin'])
            
            self.btn_gerar.configure(text="📄 Gerar Documento")
            self.update_status("Modo Individual ativado", "info")
    
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
    
    def _on_gerar_documento(self):
        """Handler para gerar documento(s)"""
        modo = self.modo_var.get()
        
        if modo == "individual":
            self._gerar_documento_individual()
        else:
            self._gerar_documentos_lote()
    
    def _gerar_documento_individual(self):
        """Gera um único documento (Modo Individual)"""
        # Verificar template
        if not self.template_valido:
            messagebox.showerror(
                "Template não encontrado",
                "Coloque o arquivo template_rpcm.docx na pasta templates/"
            )
            return
        
        # Coletar dados
        grupo = self.entry_grupo.get().strip()
        subgrupo = self.entry_subgrupo.get().strip()
        numero_preco = self.entry_numero_preco.get().strip()
        descricao = self.entry_descricao.get().strip()
        unidade = self.entry_unidade.get().strip()
        regulamentacao = self.text_regulamentacao.get("1.0", "end-1c").strip()
        
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
        
        if not regulamentacao:
            messagebox.showwarning("Validação", "A regulamentação é obrigatória")
            return
        
        # Criar objeto DocumentoRPCM primeiro para usar o método get_nome_arquivo()
        try:
            documento = DocumentoRPCM(
                grupo=grupo,
                subgrupo=subgrupo,  # Pode estar vazio
                numero_preco=numero_preco,
                descricao=descricao,
                unidade=unidade,
                regulamentacao_html=regulamentacao
            )
        except ValueError as e:
            messagebox.showerror("Validação", str(e))
            return
        
        # Perguntar onde salvar (usando nome limpo do documento)
        nome_sugerido = documento.get_nome_arquivo()
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Documento",
            defaultextension=".docx",
            initialfile=nome_sugerido,
            filetypes=[("Word Documents", "*.docx")]
        )
        
        if not arquivo:
            return  # Usuário cancelou
        
        # Gerar documento REAL
        self.update_status("⏳ Gerando documento...", "info")
        self.btn_gerar.configure(state="disabled")
        
        try:
            
            # Gerar documento
            resultado = self.generator.gerar_documento(documento, arquivo)
            
            messagebox.showinfo(
                "Sucesso",
                f"Documento gerado com sucesso!\n\n{resultado}"
            )
            
            self.update_status("✓ Documento gerado com sucesso!", "success")
            
        except DocumentGenerationError as e:
            logger.error(f"Erro na geração: {e}")
            messagebox.showerror("Erro na Geração", f"Erro ao gerar documento:\n\n{str(e)}")
            self.update_status("✗ Erro na geração do documento", "error")
        except Exception as e:
            logger.error(f"Erro inesperado: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao criar arquivo:\n{e}")
            self.update_status("✗ Erro ao gerar documento", "error")
        
        finally:
            self.btn_gerar.configure(state="normal")
    
    def _gerar_documentos_lote(self):
        """Gera múltiplos documentos (Modo Lote)"""
        # Verificar se há itens na lista
        if not self.lista_documentos:
            messagebox.showwarning(
                "Lista vazia",
                "Adicione pelo menos um documento à lista antes de gerar."
            )
            return
        
        # Verificar regulamentação
        regulamentacao = self.text_regulamentacao.get("1.0", "end-1c").strip()
        if not regulamentacao:
            messagebox.showwarning("Validação", "A regulamentação é obrigatória")
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
                    unidade=doc_dict['unidade'],
                    regulamentacao_html=regulamentacao
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
            
            # Limpar regulamentação
            self.text_regulamentacao.delete("1.0", "end")
            
            # Limpar lista (modo lote)
            self.lista_documentos.clear()
            for widget in self.linhas_container.winfo_children():
                widget.destroy()
            
            self.update_status("Formulário limpo", "info")
    
    def _on_importar_excel(self):
        """Handler para importar Excel (Modo Lote)"""
        # Verificar regulamentação
        regulamentacao = self.text_regulamentacao.get("1.0", "end-1c").strip()
        if not regulamentacao:
            messagebox.showwarning(
                "Regulamentação vazia",
                "Preencha a regulamentação antes de importar dados."
            )
            return
        
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
            num_importados = self.batch_generator.importar_excel(arquivo, regulamentacao)
            
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
