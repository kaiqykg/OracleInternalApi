# BLUEPRINT DE IMPLANTAÇÃO E OPERAÇÃO (ORACLE INTERNAL API)

Este documento complementa o `README.md` do repositório com o passo a passo canônico para instalação, parametrização e deploy do serviço em ambiente corporativo.

---

## 1. ⚡ Pré-Requisitos do Sistema Operacional

1. **Python 3.10 ou superior (64-bit)**:
   * Download: [python.org/downloads](https://www.python.org/downloads/)
   * ⚠️ Marcar: **`"Add python.exe to PATH"`**.
2. **Microsoft Visual C++ Redistributable 2015–2022 (x64)**:
   * Link direto Microsoft: [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 2. 📦 Oracle Instant Client: Download e Diretório Exato

* **Link Oficial**:
  ➜ [Oracle Instant Client Downloads for Microsoft Windows (x64) 64-bit](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)
* **Pacote**:
  * **Basic Package (64-bit)** (arquivo `instantclient-basic-windows.x64-21.x.x.x.zip`).
* **Estrutura de Pastas**:
  1. Criar a pasta `oracle/` na raiz do projeto.
  2. Extrair o zip como `instantclient_21_23/`.
  3. Estrutura final:
     ```text
     OracleInternalApi/
     └── oracle/
         └── instantclient_21_23/
             ├── oci.dll
             ├── oraociei.dll (~220 MB)
             ├── orasql.dll
             ├── orannzsbb.dll
             └── ...
     ```

---

## 3. 🔐 Arquivos de Configuração (.env)

### `.env` (Raiz)
```ini
PORT=3001
HOST=0.0.0.0
API_KEY=sua_chave_secreta_de_api_pcm_2026
```

### `oracleDb secret/.env`
```ini
DB_USER=seu_usuario_oracle
DB_PASS=sua_senha_oracle
DB_DSN=host_do_banco:1521/nome_do_servico_ou_sid
```

---

## 4. 🛠️ Instalação das Dependências

```bash
pip install -r requirements.txt
```

---

## 5. 🚀 Execução do Serviço

* **Python**:
  ```bash
  python start.py
  ```
* **Script Batch Windows (Servidor Local C:\)**:
  Renomear `start_bat.txt` para `start.bat` e executar.
* **Serviço Windows 24/7 (NSSM)**:
  ```cmd
  nssm install OracleInternalApi "C:\Python313\python.exe" "C:\OracleInternalApi\start.py"
  nssm start OracleInternalApi
  ```

---

## 6. 🧪 Testes de Validação

* **Healthcheck**: `curl http://localhost:3001/api/status`
* **Query**: `Invoke-RestMethod` no endpoint `http://localhost:3001/api/query` com cabeçalho `x-api-key`.
* **Swagger UI**: `http://localhost:3001/docs`
