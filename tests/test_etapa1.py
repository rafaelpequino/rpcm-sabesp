"""
Script de teste para validar a Etapa 1
Testa todas as funcionalidades implementadas
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("Testando imports...")
    
    try:
        import customtkinter as ctk
        print("  [OK] customtkinter")
    except ImportError as e:
        print(f"  [ERRO] customtkinter: {e}")
        return False
    
    try:
        from src.utils.validators import Validator
        print("  [OK] validators")
    except ImportError as e:
        print(f"  [ERRO] validators: {e}")
        return False
    
    try:
        from src.gui.styles import COLORS, FONTS
        print("  [OK] styles")
    except ImportError as e:
        print(f"  [ERRO] styles: {e}")
        return False
    
    try:
        from src.gui.main_window import MainWindow
        print("  [OK] main_window")
    except ImportError as e:
        print(f"  [ERRO] main_window: {e}")
        return False
    
    return True


def test_validators():
    """Testa os validadores"""
    print("\nTestando validadores...")
    
    from src.utils.validators import Validator
    
    # Teste 1: Campo obrigatório vazio
    valid, msg = Validator.validate_required("", "Teste")
    assert not valid, "Deve falhar em campo vazio"
    print("  [OK] Validacao de campo obrigatorio vazio")
    
    # Teste 2: Campo obrigatório preenchido
    valid, msg = Validator.validate_required("Valor", "Teste")
    assert valid, "Deve passar em campo preenchido"
    print("  [OK] Validacao de campo obrigatorio preenchido")
    
    # Teste 3: Número de preço válido
    valid, msg = Validator.validate_numero_preco("123456")
    assert valid, "Deve aceitar apenas números"
    print("  [OK] Validacao de numero de preco valido")
    
    # Teste 4: Número de preço inválido
    valid, msg = Validator.validate_numero_preco("01.01.01")
    assert not valid, "Deve rejeitar formato com pontos"
    print("  [OK] Validacao de numero de preco invalido")
    
    # Teste 5: Descrição com caracteres inválidos
    valid, msg = Validator.validate_filename("Teste/com:caracteres*invalidos")
    assert not valid, "Deve rejeitar caracteres inválidos"
    print("  [OK] Validacao de descricao com caracteres invalidos")
    
    # Teste 6: Descrição válida
    valid, msg = Validator.validate_filename("Descricao valida")
    assert valid, "Deve aceitar descrição válida"
    print("  [OK] Validacao de descricao valida")
    
    # Teste 7: Subgrupo opcional (sempre válido)
    valid, msg = Validator.validate_subgrupo("")
    assert valid, "Subgrupo vazio deve ser válido"
    print("  [OK] Validacao de subgrupo opcional")
    
    # Teste 8: Validação de todos os campos
    valid, errors = Validator.validate_all_fields(
        "GRUPO", "SUBGRUPO", "123456", "Descricao", "m"
    )
    assert valid, "Todos os campos válidos devem passar"
    print("  [OK] Validacao de todos os campos validos")
    
    # Teste 9: Validação com campos vazios
    valid, errors = Validator.validate_all_fields(
        "", "", "", "", ""
    )
    assert not valid, "Campos vazios devem falhar"
    assert len(errors) > 0, "Deve retornar erros"
    print("  [OK] Validacao de campos vazios")
    
    return True


def test_template_check():
    """Testa verificação de template"""
    print("\nTestando verificacao de template...")
    
    template_path = Path("templates/template_rpcm.docx")
    
    if template_path.exists():
        print(f"  [OK] Template encontrado: {template_path}")
    else:
        print(f"  [AVISO] Template nao encontrado: {template_path}")
        print("  [INFO] Coloque o arquivo template_rpcm.docx na pasta templates/")
    
    return True


def test_structure():
    """Testa estrutura de arquivos"""
    print("\nTestando estrutura de arquivos...")
    
    required_files = [
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/main.py",
        "src/gui/__init__.py",
        "src/gui/main_window.py",
        "src/gui/styles.py",
        "src/gui/widgets/__init__.py",
        "src/utils/__init__.py",
        "src/utils/validators.py",
        "templates/README.md",
        "docs/README_PLANEJAMENTO_FINAL.md",
        "docs/ETAPA_1_INTERFACE_USABILIDADE.md",
    ]
    
    all_ok = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [ERRO] {file} nao encontrado")
            all_ok = False
    
    return all_ok


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("TESTE DA ETAPA 1 - INTERFACE E USABILIDADE")
    print("=" * 60)
    
    testes = [
        ("Imports", test_imports),
        ("Validadores", test_validators),
        ("Template", test_template_check),
        ("Estrutura", test_structure),
    ]
    
    resultados = []
    for nome, teste_func in testes:
        try:
            resultado = teste_func()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"\n[ERRO] Erro no teste {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    total = len(resultados)
    sucesso = sum(1 for _, r in resultados if r)
    
    for nome, resultado in resultados:
        status = "[OK]" if resultado else "[ERRO]"
        print(f"  {status} {nome}")
    
    print(f"\n{sucesso}/{total} testes passaram")
    
    if sucesso == total:
        print("\n[OK] TODOS OS TESTES PASSARAM!")
        print("\nProximos passos:")
        print("  1. Coloque o template_rpcm.docx na pasta templates/")
        print("  2. Execute: python src/main.py")
        print("  3. Teste a interface manualmente")
        print("  4. Prossiga para a Etapa 2 - Editor de Texto")
    else:
        print("\n[AVISO] ALGUNS TESTES FALHARAM")
        print("Verifique os erros acima antes de prosseguir")
    
    return sucesso == total


if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
