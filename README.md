# Busca-CEP
📦 Sistema de Consulta de CEP com API ViaCEP + MySQL
Projeto desenvolvido como exercício do Bolsa Futuro Digital — SOFTEX, focado em:
✔ Utilização de API em Python
✔ Validação de entrada do usuário
✔ Persistência de dados em banco de dados relacional (MySQL)
✔ Estruturação de um sistema completo em linha de comando
Este projeto permite consultar informações de um CEP utilizando a API pública ViaCEP, exibir os dados e salvar automaticamente em um banco MySQL para histórico e consultas posteriores.
________________________________________
📚 Funcionalidades
🔍 1. Consulta de CEP
•	O usuário digita um CEP
•	O sistema valida se possui 8 dígitos numéricos
•	A API ViaCEP é consultada
•	Caso encontrado, os dados são exibidos em tela
💾 2. Salvamento automático no MySQL
•	Cada consulta válida é registrada na tabela ceps
•	O campo data_consulta é preenchido automaticamente com timestamp
📑 3. Listagem dos CEPs já consultados
•	Mostra todos os CEPs salvos no banco
•	Ordenados pelo mais recente (ORDER BY data_consulta DESC)
🧱 4. Criação automática do banco e tabela
•	O sistema cria o banco cep_db
•	Cria a tabela ceps caso ainda não exista
________________________________________
🛠 Tecnologias Utilizadas
•	Python 3
•	API Pública ViaCEP
•	MySQL / MariaDB
•	Biblioteca Python:
o	requests
o	mysql-connector-python
________________________________________
📦 Estrutura da Tabela (MySQL)
CREATE TABLE ceps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cep VARCHAR(10) NOT NULL,
    logradouro VARCHAR(255),
    bairro VARCHAR(100),
    localidade VARCHAR(100),
    uf CHAR(2),
    data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
O campo data_consulta é preenchido automaticamente pelo MySQL com o horário da inserção.
________________________________________
▶️ Como Executar o Projeto
1️⃣ Instale as dependências
pip install requests mysql-connector-python
2️⃣ Configure o MySQL
Certifique-se de ter um servidor MySQL rodando e credenciais válidas.
O script usa:
host: localhost
user: root
password: *******
(Altere no código se necessário.)
3️⃣ Execute o programa
python nome_do_arquivo.py
________________________________________
📋 Menu Principal
Ao iniciar, você verá:
1 - Buscar CEP
2 - Listar CEPs salvos
3 - Sair
________________________________________
🧠 Fluxo Geral do Sistema
1.	Inicializa banco e tabela (se não existirem)
2.	Exibe menu
3.	Consulta a API ViaCEP
4.	Valida CEP
5.	Exibe dados recebidos
6.	Salva no banco
7.	Permite listar histórico
________________________________________
📁 Trecho principal do código
Exemplo da inserção no banco:
sql = """
    INSERT INTO ceps (cep, logradouro, bairro, localidade, uf)
    VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(sql, valores)
conexao.commit()
Listagem do histórico:
cursor.execute("SELECT * FROM ceps ORDER BY data_consulta DESC")
resultados = cursor.fetchall()
________________________________________
🎯 Objetivo Educacional
Este projeto faz parte do Bolsa Futuro Digital — SOFTEX, com foco em:
•	Uso de APIs REST
•	Processamento de JSON em Python
•	Manipulação de dados com MySQL
•	Boas práticas de programação
•	Criação de aplicações completas de back-end
________________________________________
📌 Possíveis Melhorias Futuras
•	Interface web (Flask ou FastAPI)
•	Salvar logs de erros
•	Filtrar CEPs pelo estado ou cidade
•	Evitar duplicação de CEP já consultado
•	Exportar histórico em CSV

