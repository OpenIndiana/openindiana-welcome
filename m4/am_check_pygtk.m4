dnl AM_CHECK_PYGTK(VERSION [,ACTION-IF-FOUND [,ACTION-IF-NOT-FOUND]])
dnl Check if pygtk supports the given version.
AC_DEFUN([AM_CHECK_PYGTK],
[AC_REQUIRE([AM_PATH_PYTHON])
AC_MSG_CHECKING(for pygtk version $1)
py_mod_var=`echo $1 | sed 'y%./+-%__p_%'`
AC_CACHE_VAL(py_cv_mod_$py_mod_var, [
prog="
import sys
try:
    import pygtk
    pygtk.require('$1')
except:
    sys.exit(1)
sys.exit(0)"
if $PYTHON -c "$prog" 1>&AC_FD_CC 2>&AC_FD_CC
  then
    eval "py_cv_mod_$py_mod_var=yes"
  else
    eval "py_cv_mod_$py_mod_var=no"
  fi
])
py_val=`eval "echo \`echo '$py_cv_mod_'$py_mod_var\`"`
if test "x$py_val" != xno; then
  AC_MSG_RESULT(yes)
  ifelse([$2], [],, [$2
])dnl
else
  AC_MSG_RESULT(no)
  ifelse([$3], [],, [$3
])dnl
fi
])

