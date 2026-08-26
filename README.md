# AI Agents

A collection of lightweight AI-powered agents for system monitoring, trading sentiment analysis, and automation.

## Agents

| Agent | Purpose |
| :--- | :--- |
| `monitor_agent.py` | Collects CPU, memory, disk, and service status |
| `ai_agent.py` | Quick AI queries via Ollama |
| `trading_agent.py` | Stock/crypto sentiment analysis (yfinance + ccxt) |
| `agent_runner.py` | Full system health report with AI analysis |

## Requirements

- Python 3.11+
- Ollama (with a model like `llama3.2:3b` or `qwen2.5:7b`)
- `pip install yfinance ccxt`

## Usage

```bash
python trading_agent.py AAPL
python monitor_agent.py
python agent_runner.py

Author: Vincent Ododa