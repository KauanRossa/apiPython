# 📘 apiPython

## 🚀 Sobre o Projeto

API desenvolvida em Python com o framework Flask, utilizando SQLite como banco de dados.  
Este projeto foi criado com o objetivo de praticar e reforçar conhecimentos em back-end, sem uso de inteligência artificial — apenas com base em conhecimento prévio e pesquisas.

⚠️ Ainda está em desenvolvimento

---

## 🛠 Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [pip](https://pip.pypa.io/en/stable/) / [venv](https://docs.python.org/3/library/venv.html)

---

## 📦 Como Executar o Projeto

1. **Clone o repositório**:
   ```
   bash
   git clone https://github.com/KauanRossa/apiPython.git
   cd apiPython
   ```

2. **Crie um  ambiente  virtual**:
    ```
    python -m venv venv
    ```

3. **Ative o ambiente virtual:**

    Windows

    ```
    venv\Scripts\activate
    ```

    Linux/MacOS

    ```
    source venv/bin/activate
    ```

4. **Instalar dependências**:
    ```
    pip install -r requirements.txt
    ```

5. **Execute a aplicação**:
    ```
    flask --app app/routes run
    ```

---

## 📌 Endpoints da API

| Método | Rota             | Descrição                       |
| ------ | ---------------- | ------------------------------- |
| POST   | `/register`      | Cadastra um novo usuário        |
| POST   | `/login`         | Realiza login e retorna o token |
| GET    | `/getUsers`      | Retorna a lista de usuários     |
| GET    | `/myData`        | Retorna dados do usuário        |
| PUT    | `/updateUser`    | Atualiza dados do usuário       |
| DELETE | `/deleteUser`    | Deleta usuário                  |
| POST   | `/logout`        | Realiza logout (valida token)   |
| GET    | `/validateToken` | Valida o token JWT              |
| POST   | `/registerItems` | Cadastra um novo item           |
| GET    | `/getItems`      | Retorna a lista de itens        |
| PUT    | `/updateItem`    | Atualiza dados do item          |
| DELETE | `/deleteItem`    | Deleta item                     |

---

## 📄 Licença
Este projeto é apenas para fins de aprendizado e prática.
Nenhuma licença foi definida até o momento.

Desenvolvido por Kauan Paiano Rossa