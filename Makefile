
FILES=installvpn nordvpn.spec Makefile

clean:
	rm -f ovpn.zip

dist:
	rm -f nordvpn.tar.gz
	spectool --get-files nordvpn.spec
	tar czvf nordvpn.tar.gz $(FILES) >/dev/null
