#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# QUANTUM OPTIONS INTELLIGENCE — Setup & Launch Script
# ═══════════════════════════════════════════════════════════════

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     QUANTUM OPTIONS INTELLIGENCE — v2.0                  ║"
echo "║     Multi-Agent AI Options Trading Platform              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Install dependencies
echo "▶ Installing dependencies..."
pip install -r requirements.txt -q

echo "▶ Launching platform..."
echo ""
echo "  URL: http://localhost:8501"
echo ""
echo "  API KEY: Enter your Anthropic key in the top bar"
echo "  AGENTS:  Chart Analyst → Contract Scanner → Strategy Architect"
echo ""

streamlit run app.py \
  --server.port 8501 \
  --server.headless true \
  --browser.gatherUsageStats false \
  --theme.base dark \
  --theme.backgroundColor "#020408" \
  --theme.secondaryBackgroundColor "#080d14" \
  --theme.textColor "#e8f4fd" \
  --theme.primaryColor "#00d4ff"
