#!/bin/bash
# Thru API + Tunnel launcher
# Auto-starts API server, Cloudflare tunnel, and updates discovery Gist.

set -e

# ── Config ──
API_PORT=${PORT:-3001}
THRU_KEY=${THRU_KEY_NAME:-frio}
GIST_ID="65291a33ad7e375cd86e8814e7000c97"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🕊️  Thru API Launcher"
echo "   Port: $API_PORT"
echo "   Key:  $THRU_KEY"
echo ""

# ── Kill old instances ──
fuser -k ${API_PORT}/tcp 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 1

# ── Start API Server ──
echo "▸ Starting API server..."
cd "$HOME"
THRU_KEY_NAME=$THRU_KEY PORT=$API_PORT python3 "$SCRIPT_DIR/server.py" &
API_PID=$!
sleep 2

# Verify API is up
if ! curl -sf http://localhost:${API_PORT}/api/status > /dev/null 2>&1; then
    echo "✗ API server failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi
echo "✓ API server running (PID: $API_PID)"

# ── Start Cloudflare Tunnel ──
echo "▸ Starting Cloudflare tunnel..."
/tmp/cloudflared tunnel --url http://localhost:${API_PORT} 2>&1 | while IFS= read -r line; do
    # Capture tunnel URL
    if echo "$line" | grep -qo "https://[a-z0-9-]*\.trycloudflare\.com"; then
        TUNNEL_URL=$(echo "$line" | grep -o "https://[a-z0-9-]*\.trycloudflare\.com")
        echo "✓ Tunnel ready: $TUNNEL_URL"

        # Update Gist
        echo "▸ Updating discovery Gist..."
        gh gist edit "$GIST_ID" -f "api-url.txt" <<< "$TUNNEL_URL" 2>/dev/null && \
            echo "✓ Gist updated" || \
            echo "⚠ Gist update failed (manual update needed)"
        
        echo ""
        echo "═══════════════════════════════════════════"
        echo "  🔗 API: $TUNNEL_URL"
        echo "  🌐 Frontend: https://thru-counter.vercel.app"
        echo "═══════════════════════════════════════════"
        echo ""
    fi
    # Suppress cloudflared noise, only show URL line
done &
TUNNEL_PID=$!

# ── Wait ──
echo "Press Ctrl+C to stop all services"
trap "echo ''; echo 'Shutting down...'; kill $API_PID $TUNNEL_PID 2>/dev/null; pkill -f cloudflared 2>/dev/null; exit 0" INT TERM
wait
