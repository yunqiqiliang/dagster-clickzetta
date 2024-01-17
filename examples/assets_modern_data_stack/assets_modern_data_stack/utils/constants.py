from dagster._utils import file_relative_path
from dagster_dbt import DbtCliResource
from dagster_postgres.utils import get_conn_string

# =========================================================================
# To get this value, run `python -m assets_modern_data_stack.setup_airbyte`
# and grab the connection id that it prints at the end
# PG2Lakehouse
AIRBYTE_CONNECTION_ID = "86822de3-ca7d-40b7-866c-df5b8fdd8723"
AIRBYTE_CONNECTION_ID_EMPLOYEES = "8f7c3f58-9049-47d1-b80b-f4f7445d328d"
# PG2PG
# AIRBYTE_CONNECTION_ID = "07f5d4e2-c260-4d7f-9d6c-8a5e157aa893"

# =========================================================================


PG_SOURCE_CONFIG = {
    "username": "metabase",
    "password": "metasample123",
    "host": "172.17.1.220",
    "port": 5432,
    "database": "mds_source",
}
PG_DESTINATION_CONFIG = {
    "username": "metabase",
    "password": "metasample123",
    "host": "172.17.1.220",
    "port": 5436,
    "database": "mds_replica",
}

AIRBYTE_CONFIG = {"host": "172.17.1.220", "port": "8000", "username":"airbyte","password":"password"}
DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)
dbt_parse_invocation = dbt_resource.cli(["parse"]).wait()
DBT_MANIFEST_PATH = dbt_parse_invocation.target_path.joinpath("manifest.json")

POSTGRES_CONFIG = {
    "con_string": get_conn_string(
        username=PG_DESTINATION_CONFIG["username"],
        password=PG_DESTINATION_CONFIG["password"],
        hostname=PG_DESTINATION_CONFIG["host"],
        port=str(PG_DESTINATION_CONFIG["port"]),
        db_name=PG_DESTINATION_CONFIG["database"],
    )
}
