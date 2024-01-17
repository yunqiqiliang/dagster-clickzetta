select
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,order_time:string,order_value:double>').index as int) as index,
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,order_time:string,order_value:double>').user_id as string) as user_id,
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,order_time:string,order_value:double>').order_time as timestamp) as order_time,
        cast(from_json(_airbyte_data,'struct<index:bigint,user_id:bigint,order_time:string,order_value:double>').order_value as double) as order_value,
from {{ source('ql_ws', 'orders') }}

