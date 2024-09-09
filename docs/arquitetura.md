# "Sincronia por api's"

## Big Picture

[Desenho inical C4](https://drive.google.com/file/d/19Yg6AWwLcIwO05uDiTbF7zPSUEcWa3sR/view?ts=66be4d15)


### Fluxo Global

1. Componente que exporta os dados, e efetua Upload para o armazenamento;

2. Requisição de importação dos dados e enfileiramento das tarefas;

3. Componente que processa as tarefas enfileiradas;


``` mermaid
flowchart TD
    CLIENT[1 Processo que gera os arquivos de importação/carga]
    API_URL[Api de Geração de url assinada]
    API_ENF[2 API de Bulk]
    QUEUE_IMP[Fila de Importação]
    BUCKET[Bucket ou hospedagem]
    BDWEB[(Banco de Dados)]
    API_STATS[4 API de Status]

    CLIENT --> |"1.1 (Nome arquivo, tenant)"| API_URL
    API_URL --> |2| BUCKET
    API_URL --> |"1.2 (Url upload bucket)"| CLIENT
    CLIENT --> | 1.3 Gera/ carrega dataset| BUCKET

    CLIENT --> |1.3 Chama api de BULK passando url arquivo| API_ENF

    API_ENF --> |2.1 Enfileira Job| QUEUE_IMP

    API_ENF -->|"2.2 retorna (id e url consulta status)"| CLIENT

    CLIENT -->| 1.3 Solicita informações andamento processo| API_STATS

    API_STATS -->| 4.1 Lê informações job | BDWEB

    API_STATS -->| 4.2 Retorna Retorna status atualizado enfileirado, processando, completo, erro | CLIENT

    subgraph API
        API_URL
        API_ENF

        API_STATS

    end

    subgraph Externo
        CLIENT
    end


    subgraph Serviços
        QUEUE_IMP
        BUCKET
        BDWEB
    end

```

``` mermaid
flowchart LR


    QUEUE_IMP[Fila de Importação]
    WORKER[3 Worker de Execução da Importação]
    BUCKET[Bucket ou hospedagem]
    BDWEB[(Banco de Dados)]


    WORKER -->|3.1 Worker monitora fila| QUEUE_IMP

    WORKER -->|3.2 Baixa arquivo bucket | BUCKET

    WORKER -->|3.3 Processa arquivo e faz MERGE no PostgreSQL| BDWEB

    WORKER -->|3.4 Registra logs/status/estatísticas | BDWEB


    subgraph Worker
        QUEUE_IMP
        WORKER
        BUCKET
        BDWEB
    end
```

1. Os arquivos de exportação terão formato definido para cada figura [(Exemplos)](#exemplos);

1. Os dados deverão ser transformados para o formato parquet e carregados em algum armazenamento, tal como o **S3** ou similar, utilizando-se de url segura ou token.

    > 1. será preciso fornecer algum endpoint de **upload de documentos**, para o caso de uso dos clientes que usam a api de bulk diretamente.

1. A url do arquivo armazenado será submetida a Api de Bulk referente a figura ao qual se deseja importar.

> É possível converter arquivos json para parquet e restaurá-los para json. Por padrão os subníveis são convertidos como uma coluna do tipo json, conforme abaixo:

![image](json_parquet.png)

> Em um processo de importação isso não seria problemático, pois as linguagem geralmente possuem mecanimos de lidar com json, tal como python. Existem soluções que permitem lidar com parquet diretamente no postgres, que já tem suporte a tranformar json em rows para manipulações, mas não foram feitos testes acerca do segundo.


### Captura de dados pelas aplicações

A captura de dados nas aplicação deverá ser feita de forma **intencional** e dentro do escopo de uma transação, sem o uso de triggers, através de apis desenhadas para enfileirar no banco, através da biblioteca [QueueLib](https://github.com/Nasajon/nsj-queue-lib).

> De modo geral enfileirar no QueueLib significa efetuar um insert na tabela de eventos, <a href="https://github.com/Nasajon/nsj-queue-lib/blob/e895a2c598bebefc689f2eb0434c462c3453c214/nsj_queue_lib/client/tarefa_dao.py#L212" target="_blank">preenchendo o campo **payload** com  dados do evento.</a>







### Modelo de mensagem das operações

Modelos de operações que serão enfileiradas no Erp e processadas pelo Worker local.

#### Reload

>Representa uma ordem de subida de dados em massa.

```json
{
"type":"R", // Operação do  tipo recarga
"schema":"ns",
"table":"pessoas",
"filter":"1=1", // Filtro para recarga parcial
"clear_before":true // Limpar figura antes da recarga
}
```

#### Crud

```json
{
"type":"I",// I-insert; U-upate; D-delete; R-reload
"id":"000000000000000",// Id do registro
"schema":"ns",
"table":"pessoas"
}
```


### Processo de extração / Envio

```mermaid
graph TD
    F["Fila - QueueLib"]
    W[Worker] 
    B(Postgres)
    A[Api]
    W1{{4 transf. dados / conv. parquet}}

    F --> |1 msg| W
    W --> |2 consultas| B
   B --> |3 dados| W
   W -.-> W1 -.-> W
   W --> |5 parquet| A
   A --> |6 Status| W
```

### Transformação de dados


```mermaid
graph TD
    B(Postgres)
    W[Worker Extração]
    R["REST API Lib [DSL Transformação]"]
    P["Pandas Lib [Parquet converter]"]
    A[Api]

    B --> |1 dados| W
    W --> |2 transformação dados | R
    R --> |3 dados convertidos| P
    P --> |4 parquet| W
    W --> |5 parquet| A
    A --> |6 Status| W

    subgraph Worker
    W
    R
    P
    end
```


### DSL e formato de  conversão

A conversão de dados do banco do erp, será feita através da biblioteca [RestLib](https://github.com/Nasajon/nsj_rest_lib), que é uma biblioteca nossa, que possui estruturas que já conhecem nosso modelo de dados e conseguem converter para um formato json já em uso pelas aplicações [DadosMestre](https://github.com/Nasajon/dados-mestre-api), [Força de Vendas](https://github.com/Nasajon/forca-vendas-api), [Pedidos](https://github.com/Nasajon/pedidosAPI) entre outras.

Nessa biblioteca, cada figura possui um DTO que pode relacionar-se com outros DTO's por agregação ou composição. Esses DTO's funcionam com base em código herdado, para as operações genéricas, e anotações em classes/atributos que indicam como lidar com as colunas das entidades e seus relacionamentos.

> Exemplo <a href="https://github.com/Nasajon/dados-mestre-api/blob/production/nasajon/dto/fornecedor_erp3.py" target="_blank">DTO de Fornecedores</a>.

#### Essa abordagem tem por objetivo:

* Aproveitamento de bibliotecas já existentes;
* Coesão e compatibilidade das estruturas de dados entre as aplicações;
* Aproveitamento da experiência dos desenvolvedores com a lib;

### Apis de importação

As apis de bulk irão receber a url do arquivo, enfileirar e devolver uma URL de status para a conferência do andamento/conclusão do processo.


| Method | Path | Description |
| --- | --- | --- |
| POST | [/erp3/2531/fornecedores/_bulk](fornecedores_bulk_api.md#posterp32531fornecedores_bulk) | API para gerar url de upload do dados. |
| PUT | [/erp3/2531/fornecedores/_bulk](fornecedores_bulk_api.md#puterp32531fornecedores_bulk) | API para carga de dados em Bulk. |
| GET | [/erp3/2531/fornecedores/_bulk/status/{id}](fornecedores_bulk_api.md#geterp32531fornecedores_bulkstatusid) | API para recuperação de status de Bulk. |
| GET | [/erp3/2531/fornecedores/_bulk/status/{id}/failures](fornecedores_bulk_api.md#geterp32531fornecedores_bulkstatusidfailures) | API para recuperação de dados falhados durante a importação. Retorna um dataset com as falhas. |


> <a href="fornecedores_bulk_api.md" target="_blank">Documentação das apis</a>

### Worker

Componente responsável por processar os arquivos. Consiste em:

1. Ler o trabalho na fila;
1. Efetuar o download do arquivo;
1. Processar os dados atualizando os registros de status;

    * Será preciso definir um tamanho máximo para o arquivo na api, pois existem limitações/custo de tamanho de volume para o processo de download e processamento.

    * Uma outra solução seria carregar os dados diretamente do bucket para o postgres usando o **Copy** (Descrito [neste artigo](https://docs.aws.amazon.com/pt_br/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html) ) para uma tabela de **STAGE**, similar o quer ocorre com o **SYM_DATA**, e manipular por lá usando **[Merge](https://www.postgresql.org/docs/current/sql-merge.html)**.

    * Outar hipótese seria paginar em lotes e efetuar as importações de forma paralelizada.(Divide o trabalho entre o banco e aplicação ou alguma ferramenta que efetue trabalho de processamento, tal como NIFI);


### Exemplos

* <a href="../lista_fornecedores.json" target="_blank">Lista de Fornecedores (exemplo de arquivo de entrada antes da conversão para parquet).</a>

* <a href="../.exporta.py" target="_blank">Exemplo da conversão de json para parquet.</a>


* <a href="../.worker.py#L176" target="_blank">Exemplo do worker de processamento dos dados para postgres.</a>

*  Exemplo tabela "stage"

```sql
create table stage_area(
    id uuid default uuid_generate_v4() primary key,
    batch uuid default uuid generate_v4(),
    created_time timestamp default current_timestamp,
    updated_time timestamp default current_timestamp,
    schema_name text not null,
    table_name text not null,
    columns text not null,
    data text not null,
    status text default 'RD',
    status_message text
);

/*
Status possíveis
RD - READY - Pronto para carregamento/em espera
SK - SKIPED - Ignorado por escolha
LD - LOADING -  Em estado de carregamento
ER - ERROR - Erro qualquer, detalhado em status_message
OK - Processado com sucesso
*/
```

* Exemplo merge linha a linha

> https://www.postgresql.org/docs/current/sql-merge.html

** (postgres 15 em diante)

```sql
MERGE INTO ns.pessoas AS dest
USING (VALUES
  ('a92708e1-a7bc-4162-98b4-a2b8a2152407'::uuid, '300202', 'KING PRODUCOES E EVENTOS LTDA (alteardo merge)', true::int, true::int, true::int,'I'),
  ('ff9a0a8d-a7d3-48d6-8623-6dc6d69859bb', '300202', 'KING PRODUCOES E EVENTOS LTDA (alteardo merge)', true::int, true::int, true::int, 'D')
) AS orig (id, pessoa, nome, fornecedorativado, vendedorativado, fichaativado, op)
ON dest.id = orig.id
WHEN MATCHED AND orig.op <>'D' /*orig.id IS NOT NULL*/ THEN
    UPDATE SET
        id = orig.id,
        pessoa = orig.pessoa,
        nome = orig.nome,
        fornecedorativado = orig.fornecedorativado,
        vendedorativado = orig.vendedorativado,
        fichaativado = orig.fichaativado
WHEN NOT MATCHED /*--AND orig.id IS NOT NULL*/ THEN
    INSERT (id, pessoa, nome, fornecedorativado, vendedorativado, fichaativado)
    VALUES (orig.id, orig.pessoa, orig.nome, orig.fornecedorativado, orig.vendedorativado, orig.fichaativado)
WHEN MATCHED AND orig.op ='D' /*orig.id IS NULL*/ THEN
    DELETE;
```
