PLUGIN_NAME = stock-prices
PLUGIN_FILE = $(PLUGIN_NAME).plugin

PLUGIN_SOURCES = \
	run_stdio.py \
	server.py \
	.mcp.json \
	.claude-plugin/plugin.json \
	skills/stock-lookup/SKILL.md \
	README.md

$(PLUGIN_FILE): $(PLUGIN_SOURCES)
	zip -r $(PLUGIN_FILE) $(PLUGIN_SOURCES)

.PHONY: clean
clean:
	rm -f $(PLUGIN_FILE)
