.PHONY: test_db_integratto

ENV_VARS = $(shell cat .env)
env_setup:
	$(foreach v,$(ENV_VARS),$(eval export $(v)))

requirements:
	pip install -r requirements.txt

# Levanta uma base do integratto ERP para testes locais. O bkp no formato .backup precisa estar na pasta tests/ERP
test_db_integratto:
	docker-compose up -d db_integratto2
	sleep 2
	docker exec -it testes_api_db_integratto2_1 sh -c "./docker-entrypoint-initdb.d/002_init.sh"
	@for i in `seq 1 50`; do \
		if (docker-compose exec db_integratto2 sh -c 'psql -h db -U postgres -d integratto2 -p 5432 -c "select 1 from public.sym_data;"') then break; \
		else echo "base postgres integratto2 esta sendo inicializada..."; sleep 10; fi \
	done
	echo "base postgres integratto2 inicializada"

run_worker: env_setup
	python3 .worker.py

build_doc_openapi_md:
# https://github.com/Mermade/widdershins
# https://techdocs.studio/blog/openapi-to-markdown
	widdershins docs/fornecedores.json -o -c docs/fornecedores_bulk_api.md

build_doc: build_doc_openapi_md