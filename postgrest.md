# PostgREST

## Setup

In order to launch postgREST API effectively, you need to setup a connection to the database and create an anonymous user
with preferred access to table(s) to query.

e.g:
```sql 
-- PostgREST anonymous user setup
create role web_anon nologin;

grant usage on schema public to web_anon;
grant select on public.data_storage_assets to web_anon;
grant select on public.data_storage_enterprisegroup to web_anon;
grant select on public.data_storage_legalperson to web_anon;
grant select on public.data_storage_party to web_anon;
grant select on public.data_storage_physicalperson to web_anon;
grant web_anon to root;
```