### Process this file with automake to produce Makefile.in

desktopdir = $(datadir)/applications
desktop_in_files = \
	openindiana-welcome.desktop.in \
	openindiana-about.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST = $(desktop_in_files)

CLEANFILES = $(desktop_DATA)

