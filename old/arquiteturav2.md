## Processo de ingestão de dados via Bulk Api

### Big Picture

https://drive.google.com/file/d/19Yg6AWwLcIwO05uDiTbF7zPSUEcWa3sR/view?ts=66be4d15


``` mermaid
flowchart TD
    CLIENT[ 1 . Processo que gera os arquivos de importação/carga]
    API_ENF[2. API de Enfileiramento]
    QUEUE_IMP[Fila de Importação]
    WORKER[3. Worker de Execução da Importação]
    BUCKET[Bucket ou hospedagem]
    BDWEB[(Banco de Dados)]
    API_STATS[4. API de Status]

    CLIENT --> | 1.1 Gera arquivo avro/parquet| BUCKET

    CLIENT --> |1.2 Chama api de BULK passando url arquivo| API_ENF

    API_ENF --> |2.1 Enfileira Job| QUEUE_IMP

    API_ENF -->|"2.2 retorna (id e url consulta status)"| CLIENT

    WORKER -->|3.1 Worker monitora fila| QUEUE_IMP

    WORKER -->|3.2 Baixa arquivo bucket | BUCKET

    WORKER -->|3.3 Processa arquivo e faz MERGE no PostgreSQL| BDWEB

    WORKER -->|3.4 Registra logs/status/estatísticas | BDWEB

    CLIENT -->| 1.3 Solicita informações andamento processo| API_STATS

    API_STATS -->| 4.1 Lê informaçẽos job | BDWEB

    API_STATS -->| 4.2 Retorna informações | CLIENT

 %% API_STATS -->|Retorna status atualizado enfileirado, processando, completo, erro| CLIENT



```


    subgraph API/ Wolker
        API_ENF
        QUEUE_IMP
        API_STATS
        WORKER
        BUCKET
        BDWEB
    end
    subgraph Externo
        CLIENT
    end



#### Exportação de dados



#### Apis de importação





#### Worker


```mermaid
flowchart TD
%% Nodes
    A("fab:fa-youtube <a rel="noopener" href="https://www.youtube.com/watch?v=T5Zthq-QR2A&amp" target="_blank">Starter Guide</a>")
    B("fab:fa-youtube <a rel="noopener" href="https://www.youtube.com/watch?v=rfQ_yGJ8QAQ&amp" target="_blank">Make Flowchart</a>")
    C("fa:fa-book-open <a rel="noopener" href="https://mermaid.js.org/syntax/flowchart.html" target="_blank">Learn More</a>")
    D{"Use the editor"}
    E(fa:fa-shapes Visual Editor)
    F("fa:fa-chevron-up Add node in toolbar")
    G("fa:fa-comment-dots AI chat")
    H("fa:fa-arrow-left Open AI in side menu")
    I("fa:fa-code Text")
    J(fa:fa-arrow-left Type Mermaid syntax)

%% Edge connections between nodes
    A --> B --> C --> D -- Build and Design --> E --> F
    D -- Use AI --> G --> H
    D -- Mermaid js --> I --> J

%% Individual node styling. Try the visual editor toolbar for easier styling!
    style E color:#FFFFFF, fill:#AA00FF, stroke:#AA00FF
    style G color:#FFFFFF, stroke:#00C853, fill:#00C853
    style I color:#FFFFFF, stroke:#2962FF, fill:#2962FF

%% You can add notes with two "%" signs in a row!
```