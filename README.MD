# Simulação Importação/Exportação de dados


# Criando ambiente de trabalho

python3.10 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt


# Rodando exemplo

* Subir o banco (necessário para a importação):
```
make test_db_integratto
```

* Executar a exportação dos dados:
```sh
python exporta.py
```

* Executar a importação dos dados:

```sh
python worker.py
```

### Documentos

* [Descrição da arquitetura](docs/arquitetura.md)

* [Documentação das apis](docs/fornecedores.json)


#### Anexos

##### Exemplo merge linha a linha

> https://www.postgresql.org/docs/current/sql-merge.html

** (postgres 15 em diante)
```sql
MERGE INTO fornecedores out
USING VALUES(...) in
ON s.winename = w.winename
WHEN NOT MATCHED AND s.stock_delta > 0 THEN
  INSERT VALUES(s.winename, s.stock_delta)
WHEN MATCHED AND w.stock + s.stock_delta > 0 THEN
  UPDATE SET stock = w.stock + s.stock_delta
WHEN MATCHED THEN
  DELETE;
```

##### Exemplo tabela "stage"

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

```sql
MERGE INTO fornecedores out
--USING stage_area in
USING values(1,2,3,456 )stage_area in
ON s.winename = w.winename
WHEN NOT MATCHED AND s.stock_delta > 0 THEN
  INSERT VALUES(s.winename, s.stock_delta)
WHEN MATCHED AND w.stock + s.stock_delta > 0 THEN
  UPDATE SET stock = w.stock + s.stock_delta
WHEN MATCHED THEN
  DELETE;
```


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