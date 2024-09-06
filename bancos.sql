create table stage_area(
    id uuid default uuid_generate_v4() primary key,
    batch uuid default uuid_generate_v4(),
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