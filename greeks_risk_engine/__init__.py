from __future__ import annotations
from greeks_ui.hedge_io import HedgeRequest, HedgeResponse, Position, Contract


def solve_hedge(req: HedgeRequest) -> HedgeResponse:
    """Very small stub solver returning dummy trades and greek values."""
    # compute simple aggregate greek exposures
    pre = {g: 0.0 for g in ["delta", "gamma", "vega"]}
    for p in req.positions:
        # Use qty for delta; qty/100 for gamma; qty*0.1 for vega as dummy
        pre["delta"] += p.qty
        pre["gamma"] += p.qty / 100
        pre["vega"] += p.qty * 0.1
    # naive hedge: zero out using an opposite stock trade
    hedge = Position(
        symbol="HEDGE",
        contract=Contract(type="stock"),
        qty=-int(pre["delta"]),
    )
    post = {
        "delta": pre["delta"] + hedge.qty,
        "gamma": pre["gamma"],
        "vega": pre["vega"],
    }
    return HedgeResponse(
        status="ok",
        objective_value=0.0,
        pre_risk=pre,
        post_risk=post,
        trades=[hedge],
        residual_exposure_ok=True,
        violations=[],
    )
