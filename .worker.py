import pandas as pd
#from nsj_gcf_utils import json_util
from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

class BulkImportService:
    _db: DBAdapter3

    def __init__(self, db: DBAdapter3 = None):
        self._db = db

    def _merge_cmd(self, tabela, values, columns, update_cmd, insert_cmd):
        return f"""
            MERGE INTO {tabela} AS dest
            USING (VALUES
            {values}
            ) AS orig ({columns})
            ON dest.id = orig.id
            WHEN MATCHED AND orig.op <>'D' /*orig.id IS NOT NULL*/ THEN
                UPDATE SET
                    {update_cmd}
            WHEN NOT MATCHED /*--AND orig.id IS NOT NULL*/ THEN
                {insert_cmd}
            WHEN MATCHED AND orig.op ='D' /*orig.id IS NULL*/ THEN
                DELETE;
            """

    def _nome_tabela(self):
        pass

    def _values(self):
        pass

    def _insert_cmd(self):
        pass

    def _update_cmd(self):
        pass

    def load(self, data):
        pass


class Fornecedor(BulkImportService):

    def _nome_tabela(self):
        return "ns.pessoas"

    def _values(self):
        pass

    def _insert_cmd(self):
        pass

    def _update_cmd(self):
        pass

    def load(self, data):
        pass


class Contatos(BulkImportService):

    def _nome_tabela(self):
        return "ns.contatos"

    def _values(self):
        pass

    def _insert_cmd(self):
        pass

    def _update_cmd(self):
        pass

    def load(self, data):
        pass

class Enderecos(BulkImportService):

    def _nome_tabela(self):
        return "ns.enderecos"

    def _values(self):
        pass

    def _insert_cmd(self):
        pass

    def _update_cmd(self):
        pass

    def load(self, data):
        pass

class Contas(BulkImportService):

    def _nome_tabela(self):
        pass

    def _values(self):
        pass

    def _insert_cmd(self):
        pass

    def _update_cmd(self):
        pass

    def load(self, data):
        pass

class WorkerImportacao:
    _db: DBAdapter3
    _frncd_svc : Fornecedor
    _cntts_svc : Contatos
    _ndrcs_svc : Enderecos
    _cnts_svc  : Contas
    _f: dict

    def __init__(self, db: DBAdapter3 = None):
        self._db = db
        self._f = {
            "fornecedor" : None,
            "contas" : None,
            "enderecos": None,
            "contatos": None
        }


    def merge_fornecedor(self, fornecedor):
        self._frncd_svc.load(fornecedor)

    def merge_contas(self, contas):
        self._cnts_svc.load(contas)

    def merge_enderecos(self, enderecos):
        self._ndrcs_svc.load(enderecos)

    def merge_contatos(self, contatos):
        self._cnts_svc.load(contatos)

    def import_linha(self, json):
        #print(json)

        contatos=True if "contatos" in json else False
        enderecos=True if "enderecos" in json else False
        contas=True if "contas_fornecedores" in json else False

        if json["OP"] != "D":
            self.merge_fornecedor(json)

        if contas:
            self.merge_contas(json["contas_fornecedores"])

        if enderecos:
            self.merge_enderecos(json["enderecos"])

        if contatos:
            self.merge_contatos(json["contatos"])

        if json["OP"] == "D":
            self.merge_fornecedor(json)


df = pd.read_parquet("pacote2.parquet","pyarrow")
# json_str = data.to_json(
#     orient="records",
#     index=False, indent=True
# )

json_data = df.to_dict("records")
#print(json_data)

from infra.injector_factory import InjectorFactory
with InjectorFactory() as factory:
    for json in json_data:
        worker = WorkerImportacao(factory.db_adapter3())
        worker.import_linha(json)




# if __name__ == "__main__":
#     from infra.injector_factory import InjectorFactory
#     with InjectorFactory() as factory:
#         MultiDataBaseAdapter(factory.database_dao(), factory.lock_dao()).run()


