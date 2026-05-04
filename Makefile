PLUGIN_NAME = stock-prices
PLUGIN_FILE = $(PLUGIN_NAME).plugin

SOURCES = \
	stock_mcp_server.py \
	.mcp.json \
	.claude-plugin/plugin.json \
	skills/stock-lookup/SKILL.md \
	README.md

$(PLUGIN_FILE): $(SOURCES)
	zip -r $(PLUGIN_FILE) . -x "*.DS_Store" -x "$(PLUGIN_FILE)" -x ".claude/*"

.PHONY: clean
clean:
	rm -f $(PLUGIN_FILE)
