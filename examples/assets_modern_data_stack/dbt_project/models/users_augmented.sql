select
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,is_bot:boolean>').index as int) as index,
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,is_bot:boolean>').user_id as string) as user_id,
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,is_bot:boolean>').is_bot as boolean) as is_bot
from {{ source('ql_ws', 'users') }}