#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#
# Copyright (c) 2010, 2017, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

#
# customizations for the OpenIndiana project added by Guido Berhoerster
# <guido+openindiana@berhoerster.name>, 2010-09-03
# Copyright (c) 2018, Michal Nowak
#

import locale
import gettext
from gettext import gettext as _
import os, sys
import string
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Gdk

def N_(message): return message

PACKAGE   = "openindiana-welcome"
LOCALEDIR = "%%DATADIR%%/locale"
PIXMAPSDIR = "%%DATADIR%%/pixmaps"

copyright_string = N_("Copyright 2010 The OpenIndiana Project.\nCopyright 2010 Oracle Corporation and/or its affiliates.\nAll Rights Reserved. Use is subject to license terms.")

release_text = N_("Release")
space_text = N_("Used Space")
available_text = N_("Available Space")
memory_text = N_("Memory")
machine_text = N_("System")

def get_machine_info():
	# This is gross, assumes the file output is regular
	file_buffer = os.popen("/usr/sbin/prtdiag", "r").readlines()
	if file_buffer is None:
		return _("Unknown")
	else:
		machine_line = file_buffer.pop(0)
		machine_name = machine_line.split("System Configuration: ",1)
		return machine_name[1][:-1]

def get_machine_memory():
	# This is also gross, assumes the file output is regular
	file_buffer = os.popen("/usr/sbin/prtconf", "r").readlines()
	memory_line = file_buffer.pop(1)
	memory_info = memory_line.split("Memory size: ", 1)
	labels = memory_info[1][:-1].split()
	value = labels[0];
	unit = labels[1];
	if (re.compile("Megabytes").match(unit)):
		return _("%.1f MB") % string.atoi(value)
	elif (re.compile("Gigabytes").match(unit)):
		return _("%.1f GB") % string.atoi(value)
	else:
		return value + " " + unit;

def get_release_string():
	try:
		file_buffer = open("/etc/release", "r").readlines()
		if len(file_buffer) > 0:
			return file_buffer[0].strip()
	except IOError:
		pass
	return _("Unknown")

def format_size_for_display(size):
	KILOBYTE_FACTOR = 1024.0
	MEGABYTE_FACTOR = (1024.0 * 1024.0)
	GIGABYTE_FACTOR = (1024.0 * 1024.0 * 1024.0)

	if size < KILOBYTE_FACTOR:
		return _("%u bytes") % size
	else:
		if size < MEGABYTE_FACTOR:
			displayed_size = size / KILOBYTE_FACTOR
			return _("%.1f KB") % displayed_size
		elif size < GIGABYTE_FACTOR:
			displayed_size = size / MEGABYTE_FACTOR
			return _("%.1f MB") % displayed_size
		else:
			displayed_size = size / GIGABYTE_FACTOR
			return _("%.1f GB") % displayed_size
class LicenseDialog( Gtk.Dialog ):

    def __init__(self, parent, filename):
	flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
	title = _('OpenIndiana Licenses')
	buttons = (Gtk.STOCK_OK, Gtk.ResponseType.OK)
	Gtk.Dialog.__init__(self, title, parent, flags, buttons)
	self.connect('response', lambda w, id: self.destroy())
	
	self.set_modal(True)
	self.set_decorated(True)
	self.set_border_width(6)
	self.set_default_size(700,700)
	self.set_resizable(True)
	self.vbox.set_spacing(12)
	
	self.scrolledwin = Gtk.ScrolledWindow()
	self.scrolledwin.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
	self.scrolledwin.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
	self.vbox.pack_start(self.scrolledwin, True, True, 0)

	self.textview = Gtk.TextView()
	self.textbuffer = self.textview.get_buffer()
	self.textview.set_cursor_visible(False)
	self.textview.set_editable(False)
	
	fd = open(filename, "r")
	
	self.iter = self.textbuffer.get_iter_at_offset(0);
	
	for string in fd.readlines():
		self.textbuffer.insert(self.iter, string)
	
	self.scrolledwin.add(self.textview)
	self.show_all()

class DialogOS(Gtk.Dialog):
	def __init__(self, parent=None):
        	Gtk.Dialog.__init__(self, self.__class__.__name__, parent, 0, None)
		self.connect('destroy', lambda *w: Gtk.main_quit())
		self.set_name('os_dialog')

		Gtk.Window.set_default_icon_from_file (PIXMAPSDIR + "/aboutOI.png")

		# Set the dialog default spacing for about
		self.set_title(_("Welcome to OpenIndiana"))
		self.set_border_width(5)
		self.set_resizable(False)
		self.vbox.set_border_width(2)
		self.action_area.set_border_width(5)

		vbox = Gtk.VBox(False, 8)
		vbox.set_border_width(5)
		self.vbox.pack_start(vbox, False, False, 0)

		self.dialog = None

		# Logo
		logo = Gtk.Image()
		logo.set_from_file (PIXMAPSDIR + "/oiLogo.png")
		vbox.pack_start(logo, False, False, 0)

		# Copyright
		copyright_label = Gtk.Label()
		copyright_label.set_markup("<span size=\"small\">%s</span>" % _(copyright_string))
		copyright_label.set_justify(Gtk.Justification.CENTER)
		hbox = Gtk.HBox(True, 0)
		hbox.pack_start(copyright_label, False, False, 12)
		vbox.pack_start(hbox, False, False, 0)

		# System Information

		size_vbox = Gtk.VBox(False, 0)
		vbox.pack_end(size_vbox, False, False, 0)

		vfs = os.statvfs("/")
		size = vfs.f_blocks * vfs.f_frsize
		avail = vfs.f_bfree * vfs.f_frsize
		used = size - avail

		# Add some vertical space with an empty hbox
		hbox = Gtk.HBox(False, 0)
		size_vbox.pack_start(hbox, False, False, 10)

		# Version
		release_label = Gtk.Label()
		release_label.set_alignment(0, 0)
		release_label.set_markup("<span size=\"small\"><b>%s:</b></span> <span size=\"small\">%s</span>" % (_(release_text), get_release_string()))
		release_label.set_justify(Gtk.Justification.LEFT)
		hbox = Gtk.HBox(False, 0)
		hbox.pack_start(release_label, False, False, 12)
		size_vbox.pack_start(hbox, False, False, 0)

		# System Configuration Information
		machine_label = Gtk.Label()
		machine_label.set_alignment(0, 0)
		machine_label.set_markup("<span size=\"small\"><b>%s:</b></span> <span size=\"small\">%s</span>" % (_(machine_text), get_machine_info()))
		machine_label.set_justify(Gtk.Justification.LEFT)
		hbox = Gtk.HBox(False, 0)
		hbox.pack_start(machine_label, False, False, 12)
		size_vbox.pack_start(hbox, False, False, 0)

		# Memory Information
		memory_label = Gtk.Label()
		memory_label.set_alignment(0, 0)
		memory_label.set_markup("<span size=\"small\"><b>%s:</b></span> <span size=\"small\">%s</span>" % (_(memory_text), get_machine_memory()))
		memory_label.set_justify(Gtk.Justification.LEFT)
		hbox = Gtk.HBox(False, 0)
		hbox.pack_start(memory_label, False, False, 12)
		size_vbox.pack_start(hbox, False, False, 0)

		# Used Space
		used_label = Gtk.Label()
		used_label.set_alignment(0, 0)
		used_label.set_markup("<span size=\"small\"><b>%s:</b></span> <span size=\"small\">%s</span>" % (_(space_text), format_size_for_display(used)))
		used_label.set_justify(Gtk.Justification.LEFT)
		hbox = Gtk.HBox(False, 0)
		hbox.pack_start(used_label, False, False, 12)
		size_vbox.pack_start(hbox, False, False, 0)

		# Available Space
		avail_label = Gtk.Label()
		avail_label.set_alignment(0, 0)
		avail_label.set_markup("<span size=\"small\"><b>%s:</b></span> <span size=\"small\">%s</span>" % (_(available_text), format_size_for_display(avail)))
		avail_label.set_justify(Gtk.Justification.LEFT)
		hbox = Gtk.HBox(False, 0)
		hbox.pack_start(avail_label, False, False, 12)
		size_vbox.pack_start(hbox, False, False, 0)

		devices_button = Gtk.Button(_("_License"), None, Gtk.ResponseType.NONE)
		devices_button.connect('clicked', self.on_license_button_clicked)
		self.action_area.pack_end (devices_button, False, True, 0)

		close_button=self.add_button(Gtk.STOCK_CLOSE,Gtk.ResponseType.CANCEL)
		self.set_default_response (Gtk.ResponseType.CANCEL)
		close_button.grab_default()
		close_button.grab_focus()
		close_button.connect('clicked', lambda *w: Gtk.main_quit())

		help_button = Gtk.Button(stock=Gtk.STOCK_HELP)
		help_button.connect('clicked', self.on_getting_started_button_clicked)
		self.action_area.pack_end(help_button, False, True, 0)
		self.action_area.set_child_secondary(help_button,True)

		self.show_all()

	def on_license_button_clicked (self, button):
		# Can display using zenity or natively. Zenity ends up faster, but
		# the window gets displayed behind the about dialog. Natively ends
		# up being much slower.
		# os.spawnv(os.P_NOWAIT, "/usr/bin/zenity", ["/usr/bin/zenity", "--text-info", "--width=700", "--height=700", "--title=OpenIndiana License", "--filename=/etc/notices/LICENSE"])
		dialog = LicenseDialog(self, "/etc/notices/LICENSE")
		dialog.run()
		return None

	def on_getting_started_button_clicked(self, button):
		os.spawnv(os.P_NOWAIT, "/usr/bin/firefox", ["/usr/bin/firefox", "file:///usr/share/doc/openindiana-welcome/html/index.html"])
		return None


def main():
	locale.setlocale (locale.LC_ALL, "")
	gettext.textdomain (PACKAGE)
	gettext.install (PACKAGE, LOCALEDIR)

	dialog = DialogOS()
	Gtk.main()

if __name__ == '__main__':
	main()
