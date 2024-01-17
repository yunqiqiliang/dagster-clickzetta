import numpy as np
import pandas as pd
from dagster import AssetExecutionContext, asset
from dagster_airbyte import build_airbyte_assets
from dagster_dbt import DbtCliResource, dbt_assets
from scipy import optimize

from ..utils.constants import AIRBYTE_CONNECTION_ID, DBT_MANIFEST_PATH,AIRBYTE_CONNECTION_ID_EMPLOYEES

airbyte_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_ID,
    destination_tables=["orders", "users"],
    asset_key_prefix=["ql_ws"]
)

airbyte_assets_employees = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_ID_EMPLOYEES,
    destination_tables=["departments", "dept_emp","dept_manager","employees","salaries","titles"],
    asset_key_prefix=["ql_ws"]
)




@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    io_manager_key="db_io_manager",
)
def dbt_project_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()



def model_func(x, a, b):
    return a * np.exp(b * (x / 10**18 - 1.6095))


@asset(compute_kind="python")
def order_forecast_model(daily_order_summary: pd.DataFrame) -> np.ndarray:
    """Model parameters that best fit the observed data."""
    train_set = daily_order_summary.to_numpy()
    print(daily_order_summary.head())

    df_train_set = pd.DataFrame(train_set)
    x_data = (df_train_set.iloc[:, 0].apply(pd.Timestamp.timestamp) // 1).astype(np.int64)

    # Convert xdata from a Timestamp array to a string array
    # x_data = (train_set[:, 0].apply(pd.Timestamp.timestamp) // 1).astype(np.int64)

    # x_data = train_set[:, 0].astype(np.int64) // 10**9
    
    # Convert ydata from a Timestamp array to a numerical array
    y_data = train_set[:, 2]
    
    return optimize.curve_fit(
        f=model_func, xdata=x_data, ydata=y_data, p0=[10, 100]
    )[0]

# @asset(compute_kind="python", io_manager_key="db_io_manager")
# def predicted_orders(
#     daily_order_summary: pd.DataFrame, order_forecast_model: np.ndarray, 
# ) -> pd.DataFrame:
#     """Predicted orders for the next 30 days based on the fit paramters."""
#     a, b = tuple(order_forecast_model)
#     start_date = daily_order_summary.order_date.max()
#     future_dates = pd.date_range(start=start_date, end=start_date + pd.DateOffset(days=30))
#     predicted_data = model_func(x=future_dates.astype(np.int64), a=a, b=b)
#     return pd.DataFrame({"order_date": future_dates, "num_orders": predicted_data})

