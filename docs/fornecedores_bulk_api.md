# Manutenção de Fornecedores.

> Version 0.0.1

Gerencia todas as atividades relacionadas com a manutenção de Fornecedores no ERP Desktop.

## Path Table

| Method | Path | Description |
| --- | --- | --- |
| POST | [/erp3/2531/fornecedores/_bulk](#posterp32531fornecedores_bulk) | API para gerar url de upload do dados. |
| PUT | [/erp3/2531/fornecedores/_bulk](#puterp32531fornecedores_bulk) | API para carga de dados em Bulk. |
| GET | [/erp3/2531/fornecedores/_bulk/status/{id}](#geterp32531fornecedores_bulkstatusid) | API para recuperação de status de Bulk. |
| GET | [/erp3/2531/fornecedores/_bulk/status/{id}/failures](#geterp32531fornecedores_bulkstatusidfailures) | API para recuperação de dados falhados durante a importação. Retorna um dataset com as falhas. |

## Reference Table

| Name | Path | Description |
| --- | --- | --- |
| OAuth2 | [#/components/securitySchemes/OAuth2](#componentssecurityschemesoauth2) |  |
| bulk_url_request | [#/components/schemas/bulk_url_request](#componentsschemasbulk_url_request) | Corpo da requisição de solicitação de url. |
| bulk_url_response | [#/components/schemas/bulk_url_response](#componentsschemasbulk_url_response) | Resposta da requisição de solicitação de url. |
| bulk_request | [#/components/schemas/bulk_request](#componentsschemasbulk_request) | Corpo da requisição de envio de arquivo para carregamento. |
| bulk_response | [#/components/schemas/bulk_response](#componentsschemasbulk_response) | Resposta da requisição de envio de arquivo para carregamento. |
| bulk_status | [#/components/schemas/bulk_status](#componentsschemasbulk_status) | Resposta da requisição de constad de status do processo de carga. |

## Path Details

***

### [POST]/erp3/2531/fornecedores/_bulk

- Summary  
API para gerar url de upload do dados.

#### Headers

```ts
Authorization: string
```

#### RequestBody

- application/json

```ts
// Corpo da requisição de solicitação de url.
{
  // Identificador do tenant ao qual o registro pertence.
  tenant: integer
  // Identificador do grupo empresarial ao qual o registro pertence.
  grupo_empresarial_id: string
  // Nome do arquivo que será carregado.
  file: string
}
```

#### Responses

- 200 Sucesso

`application/json`

```ts
// Resposta da requisição de solicitação de url.
{
  // ID do processo para acompanhamento.
  upload_url?: string
}
```

- 400 Requisição inválida. Causas prováveis: a) faltando propriedades obrigatórias; b) erro de formatação do json de entrada; c) formato incorreto em alguma das propriedades;

- 401 Proibido acesso. Causa provável: falha na autenticação.

- 403 Proibida ação. Causa provável: falha na autorização.

- 404 Não encontrado. Causa provável: identificador não existente no grupo_empresarial/tenant.

- 500 Erro interno do servidor. Ver detalhes no corpo da resposta.

***

### [PUT]/erp3/2531/fornecedores/_bulk

- Summary  
API para carga de dados em Bulk.

#### Headers

```ts
Authorization: string
```

#### RequestBody

- application/json

```ts
// Corpo da requisição de envio de arquivo para carregamento.
{
  // Identificador do tenant ao qual o registro pertence.
  tenant: integer
  // Identificador do grupo empresarial ao qual o registro pertence.
  grupo_empresarial_id: string
  // URl com o arquivo usado na importação.
  url: string
}
```

#### Responses

- 200 Sucesso

`application/json`

```ts
// Resposta da requisição de envio de arquivo para carregamento.
{
  // ID do processo para acompanhamento.
  id?: string
  status_url?: string
}
```

- 400 Requisição inválida. Causas prováveis: a) faltando propriedades obrigatórias; b) erro de formatação do json de entrada; c) formato incorreto em alguma das propriedades;

- 401 Proibido acesso. Causa provável: falha na autenticação.

- 403 Proibida ação. Causa provável: falha na autorização.

- 404 Não encontrado. Causa provável: identificador não existente no grupo_empresarial/tenant.

- 500 Erro interno do servidor. Ver detalhes no corpo da resposta.

***

### [GET]/erp3/2531/fornecedores/_bulk/status/{id}

- Summary  
API para recuperação de status de Bulk.

#### Headers

```ts
Authorization: string
```

#### Responses

- 200 Sucesso

`application/json`

```ts
// Resposta da requisição de constad de status do processo de carga.
{
  // ID do processo para acompanhamento.
  id?: string
  // Status do processamento.
  status?: string
  // Mensagens adicionais relacionadas ao processo.
  message?: string
  // Número de registros processados com sucesso.
  successes?: integer
  // Número de registros com falha de processamento.
  failures?: integer
  // Número de registros ainda não processados.
  pending?: integer
  // Número de registros da solicitação.
  total?: integer
}
```

- 401 Proibido acesso. Causa provável: falha na autenticação.

- 403 Proibida ação. Causa provável: falha na autorização.

- 404 Não encontrado. Causa provável: identificador não existente.

- 500 Erro interno do servidor. Ver detalhes no corpo da resposta.

***

### [GET]/erp3/2531/fornecedores/_bulk/status/{id}/failures

- Summary  
API para recuperação de dados falhados durante a importação. Retorna um dataset com as falhas.

#### Headers

```ts
Authorization: string
```

#### Responses

- 200 Sucesso

`application/octet-stream`

```ts
{
  "type": "string",
  "format": "binary",
  "example": "Retorna um dataset com os dados com erro de importação."
}
```

- 401 Proibido acesso. Causa provável: falha na autenticação.

- 403 Proibida ação. Causa provável: falha na autorização.

- 404 Não encontrado. Causa provável: identificador não existente.

- 500 Erro interno do servidor. Ver detalhes no corpo da resposta.

## References

### #/components/securitySchemes/OAuth2

```ts
{
  "type": "oauth2",
  "flows": {
    "password": {
      "tokenUrl": "https://auth.nasajon.com.br/auth/realms/master/protocol/openid-connect/token",
      "scopes": {
        "offline_access": "Token para acesso offline"
      }
    }
  }
}
```

### #/components/schemas/bulk_url_request

```ts
// Corpo da requisição de solicitação de url.
{
  // Identificador do tenant ao qual o registro pertence.
  tenant: integer
  // Identificador do grupo empresarial ao qual o registro pertence.
  grupo_empresarial_id: string
  // Nome do arquivo que será carregado.
  file: string
}
```

### #/components/schemas/bulk_url_response

```ts
// Resposta da requisição de solicitação de url.
{
  // ID do processo para acompanhamento.
  upload_url?: string
}
```

### #/components/schemas/bulk_request

```ts
// Corpo da requisição de envio de arquivo para carregamento.
{
  // Identificador do tenant ao qual o registro pertence.
  tenant: integer
  // Identificador do grupo empresarial ao qual o registro pertence.
  grupo_empresarial_id: string
  // URl com o arquivo usado na importação.
  url: string
}
```

### #/components/schemas/bulk_response

```ts
// Resposta da requisição de envio de arquivo para carregamento.
{
  // ID do processo para acompanhamento.
  id?: string
  status_url?: string
}
```

### #/components/schemas/bulk_status

```ts
// Resposta da requisição de constad de status do processo de carga.
{
  // ID do processo para acompanhamento.
  id?: string
  // Status do processamento.
  status?: string
  // Mensagens adicionais relacionadas ao processo.
  message?: string
  // Número de registros processados com sucesso.
  successes?: integer
  // Número de registros com falha de processamento.
  failures?: integer
  // Número de registros ainda não processados.
  pending?: integer
  // Número de registros da solicitação.
  total?: integer
}
```
