### Process this file with automake to produce Makefile.in

EXTRA_DIST = \
	autogen.sh \
	ChangeLog \
	intltool-extract.in \
	intltool-merge.in \
	intltool-update.in

DISTCLEANFILES = \
	intltool-extract \
	intltool-merge \
	intltool-update

ChangeLog: $(srcdir)/ChangeLog

$(srcdir)/ChangeLog:
	if hg tip >/dev/null 2>&1; then \
		hg log --style changelog >$@; \
	else \
		echo "could not generate ChangeLog" >&2; \
		echo "The changelog coud not be generated." >ChangeLog; \
	fi

SUBDIRS = po data src
