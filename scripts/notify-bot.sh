#!/bin/bash
# Send progress update to @tani_pintar_bot
# Usage: ./notify-bot.sh "Your message here"

BOT_TOKEN="8693067374:AAFKH9RdXDHmT6yhYA4LWzBRhdDdOfWwQT8"
CHAT_ID="8689301832"
MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
  echo "Usage: $0 \"Your message here\""
  exit 1
fi

curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
  -d chat_id="$CHAT_ID" \
  -d text="$MESSAGE" \
  -d parse_mode="Markdown"

echo ""
echo "✅ Sent to @tani_pintar_bot"
