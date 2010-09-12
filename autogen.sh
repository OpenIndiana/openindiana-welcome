#!/bin/sh

error_msg () {
    printf "%s\n" "$@" >&2
}

if [ ! -f ./src/openindiana-about.py ]; then
    error_msg "this script must be executed from the root directory of the openindiana-welcome distribution"
    exit 1
fi

if ! gettext_version="$(autopoint --version 2>/dev/null | head -1)"; then
    error_msg "autopoint not found, please install gettext and ensure that autopoint is in PATH"
    exit 1
fi

if ! intltool_version="$(intltoolize --version 2>/dev/null | head -1)"; then
    error_msg "intltoolize not found, please install intltool and ensure that intltoolize is in PATH"
    exit 1
fi

if ! autoconf_version="$(autoconf --version 2>/dev/null | head -1)"; then
    error_msg "autoconf not found, please install autoconf and ensure that autoconf is in PATH"
    exit 1
fi

if ! autoheader_version="$(autoheader --version 2>/dev/null | head -1)"; then
    error_msg "autoheader not found, please install autoheader and ensure that autoheader is in PATH"
    exit 1
fi

if ! automake_version="$(automake --version 2>/dev/null | head -1)"; then
    error_msg "automake not found, please install automake and ensure that automake is in PATH"
    exit 1
fi

cat <<EOF
        Buildsystem summary
        ===================

        Gettext:        $gettext_version
        Intltool:       $intltool_version
        Autoconf:       $autoconf_version
        Autoheader:     $autoheader_version
        Automake:       $automake_version

EOF

set -e
autopoint --force $AP_OPTS
intltoolize --force --copy --automake
aclocal -I m4 --install $AL_OPTS
autoconf $AC_OPTS
autoheader $AH_OPTS
automake --add-missing --copy $AM_OPTS

