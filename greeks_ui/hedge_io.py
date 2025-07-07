from typing import List, Optional, Literal, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class Contract(BaseModel):
    type: Literal["stock", "option", "etf"]
    cp: Optional[Literal["C", "P"]] = None
    strike: Optional[float] = None
    expiry: Optional[datetime] = None


class Position(BaseModel):
    id: Optional[str] = None
    symbol: str
    contract: Contract = Field(default_factory=lambda: Contract(type="option"))
    qty: int
    multiplier: int = 1
    mark_price: Optional[float] = None


class TargetLimit(BaseModel):
    max_abs: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None


class HedgeRequest(BaseModel):
    timestamp_utc: datetime
    positions: List[Position]
    greeks_to_neutralize: List[str]
    target_limits: Dict[str, TargetLimit]
    objective: str
    cost_per_contract: float
    allowed_hedges: List[Position]
    solver: str = "osqp"
    max_iters: int = 10_000
    tolerance: float = 1e-6
    dry_run: bool = False


class HedgeResponse(BaseModel):
    status: str
    objective_value: float
    pre_risk: Dict[str, float]
    post_risk: Dict[str, float]
    trades: List[Position]
    residual_exposure_ok: bool
    violations: List[Dict[str, object]]
