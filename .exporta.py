# from pyarrow import json
# import pyarrow.parquet as pq
# table = json.read_json('lista_fornecedores.json')
# pq.write_table(table, 'pacote.parquet')  # save json/table as parquet

import pandas as pd

data = pd.read_json("lista_fornecedores.json")
data.to_parquet("pacote1.parquet")

data = pd.read_json("fornecedor.json")
data.to_parquet("pacote2.parquet")

print("arquivo enviado ao server")