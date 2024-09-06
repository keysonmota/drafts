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

* Documentação das apis: [Openapi](docs/fornecedores.json), [Md](docs/fornecedores_bulk_api.md)
