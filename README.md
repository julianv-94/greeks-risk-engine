# Greeks Risk-Engine UI

Clone → install → run:
```bash
git clone <repo> && cd greeks-risk-engine-ui
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn greeks_ui.main:app --reload
# browse to http://localhost:8000
```
Upload a .csv like:
```
symbol,type,cp,strike,expiry,qty,multiplier,mark_price
AAPL,option,C,200,2025-09-19,-75,100,12.35
AAPL,stock,,,
,250,1,194.55
```
or a JSON matching HedgeRequest.positions.
