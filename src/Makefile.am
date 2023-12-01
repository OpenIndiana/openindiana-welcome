### Process this file with automake to produce Makefile.in

bin_SCRIPTS = openindiana-about

openindiana-about: openindiana-about.py Makefile
	$(SED) -e 's|%%DATADIR%%|$(datadir)|g' -e 's|%%PYTHON%%|$(PYTHON)|g' $< >$@
	chmod +x $@

CLEANFILES = $(bin_SCRIPTS)

DISTCLEANFILES = $(CLEANFILES)

EXTRA_DIST = openindiana-about.py

