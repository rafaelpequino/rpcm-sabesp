"""
Estilos e temas para a interface
Define cores, fontes e configurações visuais seguindo a identidade Sabesp
"""

# Paleta de Cores Sabesp
COLORS = {
    # Cores principais
    'primary': '#0066CC',  # Azul Sabesp
    'secondary': '#FFFFFF',  # Branco
    'background': '#F5F5F5',  # Cinza claro
    'text': '#333333',  # Cinza escuro
    
    # Cores de status
    'success': '#28A745',  # Verde
    'error': '#DC3545',  # Vermelho
    'warning': '#FFC107',  # Amarelo
    'info': '#17A2B8',  # Azul claro
    
    # Cores de interface
    'border': '#CCCCCC',
    'hover': '#0052A3',
    'disabled': '#999999',
    'placeholder': '#999999',
}

# Configurações de fonte
FONTS = {
    'family': 'Segoe UI',
    'fallback': 'Arial',
    'title': ('Segoe UI', 14, 'bold'),
    'subtitle': ('Segoe UI', 12, 'bold'),
    'label': ('Segoe UI', 10),
    'input': ('Segoe UI', 10),
    'button': ('Segoe UI', 10, 'bold'),
    'small': ('Segoe UI', 9),
}

# Espaçamentos
SPACING = {
    'padding': 20,
    'margin': 10,
    'small_margin': 5,
    'field_height': 30,
}

# Tamanhos da janela
WINDOW = {
    'min_width': 900,
    'min_height': 700,
    'default_width': 1000,
    'default_height': 800,
}

# Configurações do CustomTkinter
CTK_THEME = {
    'color_theme': 'blue',  # blue, green, dark-blue
    'appearance_mode': 'light',  # light, dark, system
}
