### Process this file with automake to produce Makefile.in

bin_SCRIPTS = openindiana-about

openindiana-about: openindiana-about.py Makefile
	$(SED) 's|%%DATADIR%%|$(datadir)|g' $< >$@
	chmod +x $@

CLEANFILES = $(bin_SCRIPTS)

DISTCLEANFILES = $(CLEANFILES)

EXTRA_DIST = openindiana-about.py

