from greeks_ui.hedge_io import HedgeRequest, HedgeResponse

# 👉  assumes user already pip-installed or symlinked their engine package.
from greeks_risk_engine import solve_hedge as _core_solver   # noqa: E402


def solve(req: HedgeRequest) -> HedgeResponse:
    """Delegate to core engine; re-cast result into our HedgeResponse."""
    return HedgeResponse.model_validate(_core_solver(req))
