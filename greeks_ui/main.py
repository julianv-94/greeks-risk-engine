from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import csv
import io
import json
import datetime as dt
from greeks_ui.hedge_io import HedgeRequest, Position, Contract, TargetLimit
from greeks_ui.hedge_engine import solve
from typing import Optional, Literal, cast

app = FastAPI(title="Greeks Hedger UI")
templates = Jinja2Templates(directory="greeks_ui/templates")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def csv_to_positions(raw: str) -> list[Position]:
    rdr = csv.DictReader(io.StringIO(raw))
    out = []
    for row in rdr:
        out.append(
            Position(
                symbol=row["symbol"],
                contract=Contract(
                    type=cast(
                        Literal["stock", "option", "etf"],
                        row.get("type", "option"),
                    ),
                    cp=cast(
                        Optional[Literal["C", "P"]],
                        row.get("cp") or None,
                    ),
                    strike=float(row["strike"]) if row.get("strike") else None,
                    expiry=(
                        dt.datetime.fromisoformat(row["expiry"])
                        if row.get("expiry")
                        else None
                    ),
                ),
                qty=int(row["qty"]),
                multiplier=int(row.get("multiplier", 1)),
                mark_price=(
                    float(row["mark_price"]) if row.get("mark_price") else None
                ),
            )
        )
    return out


@app.post("/solve", response_class=HTMLResponse)
async def solve_ui(
    request: Request,
    file: UploadFile,
    delta_limit: float = Form(...),
    gamma_limit: float = Form(...),
    vega_limit: float = Form(...),
) -> HTMLResponse:
    raw = (await file.read()).decode()
    positions = (
        csv_to_positions(raw)
        if file.filename and file.filename.endswith(".csv")
        else [Position.model_validate(p) for p in json.loads(raw)]
    )

    req = HedgeRequest(
        timestamp_utc=dt.datetime.utcnow(),
        positions=positions,
        greeks_to_neutralize=["delta", "gamma", "vega"],
        target_limits={
            "delta": TargetLimit(max_abs=delta_limit),
            "gamma": TargetLimit(max_abs=gamma_limit),
            "vega":  TargetLimit(max_abs=vega_limit),
        },
        objective="min_variance",
        cost_per_contract=1.0,
        allowed_hedges=[],  # let engine pick full chain
    )
    res = solve(req)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "response": res.model_dump(mode="json"),
            "json": json.dumps(res.model_dump(mode="json")),
        },
    )
