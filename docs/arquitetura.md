## Processo de ingestão de dados via Bulk Api

### Big Picture

https://drive.google.com/file/d/19Yg6AWwLcIwO05uDiTbF7zPSUEcWa3sR/view?ts=66be4d15



``` mermaid
flowchart TD
    CLIENT[ 1 . Processo que gera os arquivos de importação/carga]
    API_ENF[2. API de Bulk]
    QUEUE_IMP[Fila de Importação]
    BUCKET[Bucket ou hospedagem]
    BDWEB[(Banco de Dados)]
    API_STATS[4. API de Status]

    CLIENT --> | 1.1 Gera arquivo avro/parquet| BUCKET

    CLIENT --> |1.2 Chama api de BULK passando url arquivo| API_ENF

    API_ENF --> |2.1 Enfileira Job| QUEUE_IMP

    API_ENF -->|"2.2 retorna (id e url consulta status)"| CLIENT

    CLIENT -->| 1.3 Solicita informações andamento processo| API_STATS

    API_STATS -->| 4.1 Lê informações job | BDWEB

    API_STATS -->| 4.2 Retorna Retorna status atualizado enfileirado, processando, completo, erro | CLIENT

    subgraph API
        API_ENF
        QUEUE_IMP
        API_STATS
        BUCKET
        BDWEB
    end

    subgraph Externo
        CLIENT
    end
```

``` mermaid
flowchart LR


    QUEUE_IMP[Fila de Importação]
    WORKER[3. Worker de Execução da Importação]
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


### Exportação de dados

1. Os arquivos de exportação terão formato definido para cada figura;

1. Os dados deverão ser transformados para o formato parquet e carregados em algum armazenamento.

1. A url do arquivo armazenado será submetida a Api de Bulk referente a figura ao qual se deseja importar.


### Apis de importação

As apis de bulk irão receber a url do arquivo, enfileirar e devolver uma URL de status para a conferência do andamento/conclusão do processo.

As apis de Bulk seguem o padrão:

>  **PUT** figura/_bulk ->  Para registro do arquivo de importação.

>  **GET** figura/_bulk/status/{id} ->Para consulta do andamento do processo.

<a href="fornecedores_bulk_api.md" target="_blank">Documentação apis</a>

### Worker

Componente responsável por processar os arquivos:

1. Ler o trabalho na fila;
1. Efetuar o download do arquivo;
1. Processar os dados atualizando os registros de status;
    * definir um tamanho máximo para o arquivo na api pode ajudar, pois existem limitaçõe de tamanho de volume, outro recurso seria carregar os dados diretamente no postgers para manipular por lá, ou mesmo. efetuuar as importações de forma paralelizada.( Divide o trabalho entre o banco e aplicação ou alguma ferramenta que efetue trabalho de processamento, tal como );

    Outra alternativa seria fazer um bulk insert (copy) para uma tabela de stage e após utilizar o Merge a partir desta (Bota o banco para trabalhar);


    ### Exemplos

    * <a href="../lista_fornecedores.json" target="_blank">Lista de Fornecedores (exemplo de arquivo de entrada ante da conversão para parquet).</a>

    * <a href="../.exporta.py" target="_blank">Exemplo da conversão de json para parquet.</a>


    * <a href="../.worker.py#L176" target="_blank">Exemplo do worker de processamento dos dados para postgres.</a>
