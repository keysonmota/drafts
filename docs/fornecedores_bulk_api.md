---
title: Manutenção de Fornecedores. v0.0.1
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="manuten-o-de-fornecedores-">Manutenção de Fornecedores. v0.0.1</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Gerencia todas as atividades relacionadas com a manutenção de Fornecedores no ERP Desktop.

Base URLs:

* <a href="https://api.nasajon.app/dados-mestre">https://api.nasajon.app/dados-mestre</a>

# Authentication

- oAuth2 authentication. 

    - Flow: password

    - Token URL = [https://auth.nasajon.com.br/auth/realms/master/protocol/openid-connect/token](https://auth.nasajon.com.br/auth/realms/master/protocol/openid-connect/token)

|Scope|Scope Description|
|---|---|
|offline_access|Token para acesso offline|

<h1 id="manuten-o-de-fornecedores--ingest-o-de-dados-em-massa-">Ingestão de dados em massa.</h1>

## put__erp3_2531_fornecedores__bulk

`PUT /erp3/2531/fornecedores/_bulk`

API para carga de dados em Bulk.

> Body parameter

```json
{
  "url": "https://armazemento.com/meuarquivo"
}
```

<h3 id="put__erp3_2531_fornecedores__bulk-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|Authorization|header|string|true|Token gerado pelo OAuth 2|
|body|body|[bulk_request](#schemabulk_request)|false|Corpo da requisição, contendo a url do arquivo importação.|

> Example responses

> 200 Response

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "status_url": "/erp3/2531/fornecedores/_bulk/status/00000000-0000-0000-0000-000000000000"
}
```

<h3 id="put__erp3_2531_fornecedores__bulk-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Sucesso|[bulk_response](#schemabulk_response)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Requisição inválida. Causas prováveis: a) faltando propriedades obrigatórias; b) erro de formatação do json de entrada; c) formato incorreto em alguma das propriedades;|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Proibido acesso. Causa provável: falha na autenticação.|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Proibida ação. Causa provável: falha na autorização.|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Não encontrado. Causa provável: identificador não existente no grupo_empresarial/tenant.|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Erro interno do servidor. Ver detalhes no corpo da resposta.|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2 ( Scopes: offline_access )
</aside>

<h1 id="manuten-o-de-fornecedores--get-status-bulk">GET Status Bulk</h1>

## get__erp3_2531_fornecedores__bulk_status_{id}

`GET /erp3/2531/fornecedores/_bulk/status/{id}`

API para recuperação de status de Bulk.

<h3 id="get__erp3_2531_fornecedores__bulk_status_{id}-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|Authorization|header|string|true|Token gerado pelo OAuth 2|
|id|path|string|true|Id da operação recebida pela api de Bulk.|

> Example responses

> 200 Response

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "status": "processing",
  "message": "ocorreram erros durante o processo de importação.",
  "successes": "550",
  "failures": "50",
  "total": "1000"
}
```

<h3 id="get__erp3_2531_fornecedores__bulk_status_{id}-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Sucesso|[bulk_status](#schemabulk_status)|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Proibido acesso. Causa provável: falha na autenticação.|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Proibida ação. Causa provável: falha na autorização.|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Não encontrado. Causa provável: identificador não existente.|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Erro interno do servidor. Ver detalhes no corpo da resposta.|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2 ( Scopes: offline_access )
</aside>

# Schemas

<h2 id="tocS_bulk_request">bulk_request</h2>
<!-- backwards compatibility -->
<a id="schemabulk_request"></a>
<a id="schema_bulk_request"></a>
<a id="tocSbulk_request"></a>
<a id="tocsbulk_request"></a>

```json
{
  "url": "https://armazemento.com/meuarquivo"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|url|string|false|none|URl com o arquivo usado na importação|

<h2 id="tocS_bulk_response">bulk_response</h2>
<!-- backwards compatibility -->
<a id="schemabulk_response"></a>
<a id="schema_bulk_response"></a>
<a id="tocSbulk_response"></a>
<a id="tocsbulk_response"></a>

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "status_url": "/erp3/2531/fornecedores/_bulk/status/00000000-0000-0000-0000-000000000000"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string|false|none|ID do processo para acompanhamento|
|status_url|string|false|none|none|

<h2 id="tocS_bulk_status">bulk_status</h2>
<!-- backwards compatibility -->
<a id="schemabulk_status"></a>
<a id="schema_bulk_status"></a>
<a id="tocSbulk_status"></a>
<a id="tocsbulk_status"></a>

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "status": "processing",
  "message": "ocorreram erros durante o processo de importação.",
  "successes": "550",
  "failures": "50",
  "total": "1000"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string|false|none|none|
|status|string|false|none|none|
|message|string|false|none|none|
|successes|integer|false|none|none|
|failures|integer|false|none|none|
|total|integer|false|none|none|

