import requests
import mysql.connector
from mysql.connector import Error

def inicializar_banco():
    """Cria o banco e a tabela se não existirem"""
    try:
        # Conecta SEM especificar o database
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="********"
        )
        cursor = conexao.cursor()
        
        # Cria o banco
        cursor.execute("CREATE DATABASE IF NOT EXISTS cep_db")
        print("Banco 'cep_db' verificado/criado")
        
        # Usa o banco
        cursor.execute("USE cep_db")
        
        # Cria a tabela (nome: ceps)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ceps (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cep VARCHAR(10) NOT NULL,
                logradouro VARCHAR(255),
                bairro VARCHAR(100),
                localidade VARCHAR(100),
                uf CHAR(2),
                data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Tabela 'ceps' verificada/criada\n")
        
        conexao.commit()
        cursor.close()
        conexao.close()
        
        return True
        
    except Error as erro:
        print(f"Erro ao inicializar banco: {erro}")
        return False

def conectar_banco():
    """Conecta ao banco de dados"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="tapcv1980",
            database="cep_db"
        )
    except Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None

def salvar_no_banco(dados):
    """Salva os dados do CEP no banco"""
    try:
        conexao = conectar_banco()
        
        if not conexao:
            return False
        
        cursor = conexao.cursor()

        sql = """
            INSERT INTO ceps (cep, logradouro, bairro, localidade, uf)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            dados["cep"],
            dados["logradouro"],
            dados["bairro"],
            dados["localidade"],
            dados["uf"]
        )

        cursor.execute(sql, valores)
        conexao.commit()
        
        print(f"\nDados salvos no MySQL! ID: {cursor.lastrowid}\n")
        
        cursor.close()
        conexao.close()
        
        return True
        
    except Error as erro:
        print(f"Erro ao salvar no banco: {erro}\n")
        return False

def buscar_cep():
    """Busca CEP na API e salva no banco"""
    while True:
        cep = input("Digite seu CEP (ou 'sair' para encerrar): ").strip()
        
        # Opção de sair
        if cep.lower() == 'sair':
            print("Pesquisa finalizada!")
            break

        # Mantém somente números
        cep = ''.join([c for c in cep if c.isdigit()])

        # Validação simples
        if len(cep) != 8:
            print("CEP inválido! Digite exatamente 8 números.\n")
            continue

        try:
            # Consulta API
            url = f"https://viacep.com.br/ws/{cep}/json/"
            resposta = requests.get(url, timeout=5)
            
            if resposta.status_code != 200:
                print("Erro ao consultar a API. Tente novamente.\n")
                continue
            
            dados = resposta.json()

            if dados.get("erro"):
                print("CEP não encontrado!\n")
                continue

            # Exibe os dados
            print("\n" + "="*50)
            print("CEP ENCONTRADO:")
            print("="*50)
            print(f"  CEP:        {dados['cep']}")
            print(f"  Logradouro: {dados['logradouro']}")
            print(f"  Bairro:     {dados['bairro']}")
            print(f"  Cidade:     {dados['localidade']}")
            print(f"  UF:         {dados['uf']}")
            print("="*50)

            # Salva no banco
            salvar_no_banco(dados)
            
            # Pergunta se quer buscar outro
            continuar = input("\nDeseja buscar outro CEP? (s/n): ").strip().lower()
            if continuar != 's':
                print("Até logo!")
                break

        except requests.Timeout:
            print("Tempo esgotado. Tente novamente.\n")
        except requests.RequestException as erro:
            print(f"Erro ao consultar API: {erro}\n")
        except Exception as erro:
            print(f"Erro inesperado: {erro}\n")

def listar_ceps_salvos():
    """Lista todos os CEPs salvos no banco"""
    try:
        conexao = conectar_banco()
        
        if not conexao:
            return
        
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM ceps ORDER BY data_consulta DESC")
        
        resultados = cursor.fetchall()
        
        if resultados:
            print("\n" + "="*60)
            print("CEPs SALVOS NO BANCO DE DADOS")
            print("="*60)
            for registro in resultados:
                print(f"\n[ID: {registro[0]}]")
                print(f"  CEP: {registro[1]}")
                print(f"  Endereço: {registro[2]}")
                print(f"  Bairo: {registro[3]}")
                print(f"  Cidade: {registro[4]}")
                print(f"  UF: {registro[5]}")
                print(f"  Data: {registro[6]}")
                print("-" * 60)
        else:
            print("\nNenhum CEP salvo ainda.")
        
        cursor.close()
        conexao.close()
        
    except Error as erro:
        print(f"Erro ao listar CEPs: {erro}")

# ===== PROGRAMA PRINCIPAL =====
if __name__ == "__main__":
    print("\n" + "="*60)
    print("        SISTEMA DE CONSULTA DE CEP")
    print("="*60 + "\n")
    
    # Inicializa o banco e tabela
    if not inicializar_banco():
        print("Não foi possível inicializar o banco de dados.")
        exit()
    
    # Menu
    while True:
        print("\n" + "="*60)
        print("MENU:")
        print("  1 - Buscar CEP")
        print("  2 - Listar CEPs salvos")
        print("  3 - Sair")
        print("="*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            buscar_cep()
        elif opcao == "2":
            listar_ceps_salvos()
        elif opcao == "3":
            print("\nAté logo!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")