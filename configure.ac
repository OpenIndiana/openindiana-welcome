dnl Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
AC_INIT([openindiana-welcome],
        [0.1],
        [https://bugs.launchpad.net/openindiana],
        [openindiana-welcome],
        [http://openindiana.org/])
AM_INIT_AUTOMAKE([foreign tar-ustar dist-bzip2])
AM_MAINTAINER_MODE
AC_CONFIG_SRCDIR([src/openindiana-about.py])

AC_PROG_INSTALL
AC_PROG_SED
IT_PROG_INTLTOOL([0.40.0])

AM_PATH_PYTHON([2.4])
AM_CHECK_PYGTK([2.0],,[AC_MSG_ERROR([openindiana-welcome requires pygtk-2.0])])

GETTEXT_PACKAGE=openindiana-welcome
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,
                   "${GETTEXT_PACKAGE}",
                   [the gettext translation domain])
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION([0.17])

AC_CONFIG_HEADERS([src/config.h])
AC_CONFIG_FILES([Makefile
        po/Makefile.in
        data/Makefile
        data/html/Makefile
        data/desktop/Makefile
        data/pixmaps/Makefile
        src/Makefile])

AC_OUTPUT

