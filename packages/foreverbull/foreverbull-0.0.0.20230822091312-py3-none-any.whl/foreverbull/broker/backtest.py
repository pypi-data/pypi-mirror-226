import requests

from foreverbull import models

from .http import api_call


@api_call
def create(backtest: models.backtest.Backtest) -> requests.Request:
    return requests.Request(
        method="POST",
        url="/backtest/api/backtests",
        json=backtest.model_dump(),
    )


@api_call
def get(name: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/backtest/api/backtests/{name}",
    )


@api_call
def ingest(name: str) -> requests.Request:
    return requests.Request(
        method="POST",
        url=f"/backtest/api/backtests/{name}/ingest",
    )


@api_call
def new_session(backtest: str, source: str, source_key: str) -> requests.Request:
    return requests.Request(
        method="POST",
        url="/backtest/api/sessions",
        json={"backtest": backtest, "source": source, "source_key": source_key},
    )


@api_call
def get_session(backtest_name: str, session_id: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/backtest/api/sessions/{session_id}",
    )


@api_call
def get_execution(execution_id: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/backtest/api/executions/{execution_id}",
    )
