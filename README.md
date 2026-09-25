# 🏛️ OracleInternalApi — Gateway de Alta Performance (PCM)

Gateway HTTP interno construído em **FastAPI** e **Python oracledb (Thick Mode)** com pool persistente de conexões para comunicação direta, ultrarrápida (< 20 ms) e segura com o banco de dados Oracle corporativo.

Projetado especificamente para eliminar intermediários na nuvem (Vercel, Turso, túneis remotos), operando na mesma rede local da planta industrial.

---

## ⚡ 1. Pré-Requisitos de Infraestrutura

Antes de iniciar, o servidor Windows ou estação de trabalho deve possuir:

1. **Python 3.10 ou superior (64-bit)**:
   * Download: [python.org/downloads](https://www.python.org/downloads/)
   * ⚠️ **Crítico na instalação**: Marcar a opção **"Add python.exe to PATH"**.
2. **Microsoft Visual C++ Redistributable 2015–2022 (x64)**:
   * O driver nativo do Oracle Instant Client depende das bibliotecas de runtime C do Windows.
   * Link direto oficial Microsoft: [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe)
   * *Se não instalado, ocorrerá o erro DPI-1047: Cannot locate a 64-bit Oracle Client library.*

---

## 📦 2. Instalação do Oracle Instant Client (Passo a Passo)

O modo Thick do `python-oracledb` exige as DLLs nativas da Oracle compiladas em C para Windows 64-bit.

### Passo 2.1: Download Oficial
* Acesse a página oficial de downloads da Oracle:
  ➜ **[Oracle Instant Client for Microsoft Windows (x64) 64-bit](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)**
* Baixe o pacote:
  * **Basic Package** (ex: `instantclient-basic-windows.x64-21.23.0.0.0.zip` ou superior).
  * *(Não baixe a versão "Basic Light" caso a sua usina utilize charsets complexos ou WE8MSWIN1252).*

### Passo 2.2: Onde Colocar e Como Renomear a Pasta
1. Na raiz do projeto `OracleInternalApi/`, crie uma pasta chamada `oracle`.
2. Extraia o conteúdo do arquivo ZIP baixado dentro de `oracle/`.
3. Certifique-se de que o nome da subpasta extraída seja exatamente:
   `instantclient_21_23`
4. A estrutura de diretórios DEVE ficar rigorosamente assim:

```text
OracleInternalApi/
└── oracle/
    └── instantclient_21_23/
        ├── oci.dll              <-- Arquivo central do Oracle Call Interface
        ├── oraociei.dll         <-- Arquivo de bibliotecas de suporte (~220 MB)
        ├── orasql.dll
        ├── orannzsbb.dll
        ├── ocijdbc21.dll
        └── ... (demais DLLs extraídas)
```

> ⚠️ **Atenção**: Evite criar pastas aninhadas duplicadas como `oracle/instantclient_21_23/instantclient_21_23/oci.dll`. O arquivo `oci.dll` deve estar diretamente em `oracle/instantclient_21_23/oci.dll`.

---

## 🔐 3. Configuração dos Arquivos de Ambiente (.env)

A arquitetura adota segregação de segredos em **duas camadas**:

### Camada 1: Configurações do Serviço HTTP (`.env`)
Na raiz do projeto (`OracleInternalApi/`), crie um arquivo chamado `.env` (baseado em `.env.example`):

```ini
PORT=3001
HOST=0.0.0.0
API_KEY=sua_chave_secreta_de_api_pcm_2026
```

### Camada 2: Credenciais do Banco Oracle (`oracleDb secret/.env`)
Crie a pasta `oracleDb secret` na raiz do projeto e, dentro dela, o arquivo `.env`:

```ini
DB_USER=seu_usuario_oracle
DB_PASS=sua_senha_oracle
DB_DSN=host_do_banco:1521/nome_do_servico_ou_sid
```

*Exemplo de DSN TNS padrão*: `192.168.0.10:1521/ORCLPDB` ou `SRV-ORACLE.usina.local:1521/PROD`.

---

## 🛠️ 4. Instalação das Dependências Python

Abra o terminal (PowerShell ou Prompt de Comando) na pasta `OracleInternalApi`:

```bash
pip install -r requirements.txt
```

As dependências instaladas serão:
* `fastapi`: Framework web assíncrono de alto desempenho.
* `uvicorn`: Servidor ASGI HTTP ultrarrápido.
* `oracledb`: Driver oficial da Oracle com suporte ao modo Thick e pool persistente.
* `pydantic`: Validação estrita e tipada de payloads.
* `python-dotenv`: Resolução automática de arquivos `.env`.

---

## 🚀 5. Inicialização do Serviço

### Opção A: Via Python (Recomendado / Multiplataforma)
```bash
python start.py
```
*(Ou diretamente: `python -m uvicorn main:app --host 0.0.0.0 --port 3001`)*.

### Opção B: Via Script Batch no Servidor Local (Windows)
Se o projeto for copiado para um disco local (ex: `C:\OracleInternalApi`), renomeie o arquivo `start_bat.txt` para `start.bat` e execute com dois cliques:

```bat
start.bat
```

### Opção C: Executar como Serviço Automático do Windows (NSSM)
Para manter a API rodando 24/7 mesmo após logoff do servidor:
1. Baixe o [NSSM (Non-Sucking Service Manager)](https://nssm.cc/download).
2. Execute no terminal como Administrador:
   ```cmd
   nssm install OracleInternalApi "C:\Python313\python.exe" "C:\OracleInternalApi\start.py"
   nssm set OracleInternalApi AppDirectory "C:\OracleInternalApi"
   nssm start OracleInternalApi
   ```

---

## 🧪 6. Validação e Testes de Conectividade (Smoke Tests)

Com o serviço rodando, teste as rotas em outro terminal:

### 1. Teste de Conexão com o Banco (Healthcheck aberto)
```bash
curl http://localhost:3001/api/status
```
*Retorno esperado*:
```json
{
  "status": "ONLINE",
  "service": "OracleInternalApi",
  "mode": "Oracle Thick Mode (Instant Client 21.23)",
  "latencyMs": 20.16,
  "database": {
    "sysdate": "2026-09-25T07:43:23",
    "sessionUser": "SEU_USUARIO",
    "totalSampleOwners": 10,
    "sampleOwners": ["APPQOSSYS", "DBSNMP", "SYS", "SYSTEM", "..."]
  }
}
```

### 2. Teste de Execução de Consulta (Autenticado via x-api-key)
No PowerShell:
```powershell
$headers = @{
    "x-api-key" = "sua_chave_secreta_de_api_pcm_2026"
    "Content-Type" = "application/json"
}
$body = @{
    sql = "SELECT COUNT(*) AS TOTAL_ORDENS FROM INDUSTRIA.ORDEM_SERVICO"
    format = "records"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:3001/api/query" -Method Post -Headers $headers -Body $body
```

*Retorno esperado*:
```json
{
  "success": true,
  "format": "records",
  "totalRows": 1,
  "executionTimeMs": 70.72,
  "columns": ["TOTAL_ORDENS"],
  "data": [
    { "TOTAL_ORDENS": 150956 }
  ],
  "error": null
}
```

### 3. Documentação Interativa (Swagger UI)
Acesse no navegador:
➜ **`http://localhost:3001/docs`**

---

## 📋 7. Formatos Suportados na Rota `/api/query`

O payload aceita o campo opcional `"format"`:

1. **`"records"` (Padrão)**: Retorna lista de objetos JSON (`[{"TAG": "M-01", "HORAS": 10}, ...]`), ideal para consumo direto em UIs e dashboards.
2. **`"table"`**: Retorna matriz compacta `{"columns": [...], "rows": [[...], ...]}` para menor tráfego de rede em relatórios extensos com dezenas de milhares de linhas.
