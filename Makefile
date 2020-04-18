.PHONY: all

PLIST_NAME:=info.hotoku.bkeep

all: load

clean: unload
	rm $(PLIST_NAME).plist || true

load: $(PLIST_NAME).plist unload
	cp -f $(PLIST_NAME).plist ~/Library/LaunchAgents/$(PLIST_NAME).plist
	launchctl load ~/Library/LaunchAgents/$(PLIST_NAME).plist

unload:
	launchctl unload ~/Library/LaunchAgents/$(PLIST_NAME).plist || true
	rm ~/Library/LaunchAgents/$(PLIST_NAME).plist || true

$(PLIST_NAME).plist: $(PLIST_NAME).jinja.plist render.py
	python $(word 2,$^) $< > $@
