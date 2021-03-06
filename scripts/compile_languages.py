#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

print 'this script will not work under windows yet'

for root, dirs, files in os.walk('locale'):
    break

for dir in dirs:
    print 'Compiling language: ' + dir + ' .. ',
    os.system('msgfmt -o locale/' + dir + '/LC_MESSAGES/canta.mo locale/' + dir + '/LC_MESSAGES/canta.po')
    print "DONE!"
