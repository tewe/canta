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

"""Module song_loader

functions to find the ultrastar song-directorys
"""

import os
from canta.song.song import Song


def search_songs(songs_path):
    """Searches recursive for valid ultrastar songs

    A valid ultrastar-song is a Directory with at least:
        - one textfile in the ultrastar format
        - one ogg/mp3 music file
    """
    # create Song objects for every directory in the
    # songs directory and add them to the song list:

    # if you want to change stuff look here:
    # http://docs.python.org/lib/os-file-dir.html
    songs = []
    covers = 0
    mp3s = 0
    for root, dir_names, file_names in os.walk(songs_path):
        if ".svn" in dir_names:
            dir_names.remove(".svn")
        dir_names.sort()
        for dir_name in dir_names:
            absolute_path = os.path.join(songs_path, dir_name)
            for root, dir_names, file_names in os.walk(absolute_path):
                for file_name in file_names:
                    file_name = file_name.decode('utf-8')
                    valid_picture_formats = ['jpg', 'jpeg', 'png']
                    valid_sound_formats = ['ogg', 'mp3']
                    lower_file = file_name.lower()
                    if lower_file == "desc.txt":
                        pass
                    elif lower_file.endswith('.txt'):
                        # The song:
                        song = Song(path = root, file=file_name)
                        song.read_from_us(type="headers")

                        #print "Scanning Directory:\t<" + song.path + ">\n"
                        file_names = unicode_encode_list(file_names)
                        __validate_items__(valid_picture_formats, \
                            song, file_names, 'cover')

                        if 'cover' in song.info:
                            #print "FOUND Cover <%s>" % (song.info['cover'])
                            covers += 1
                        __validate_items__(valid_sound_formats, \
                            song, file_names, 'mp3')

                        if 'mp3' in song.info and song.info != None:
                            mp3s += 1
                            songs.append(song)

    #print mp3s, " Songs with ", covers, " valid Covers found!"
    return songs


def __validate_items__(valid_formats, song, file_names, check_item):
    found = False
    files_with_right_format = []
    search = False
    if check_item in song.info and \
        song.info[check_item] != None and \
            song.info[check_item] in file_names:
        #file in txt file is right
        return True
    elif check_item in song.info:
        if song.info[check_item] != None:
            search = True
    for format in valid_formats:
        # if something about that stands in the file
        # when not searching only files with right extention
        if search:
            item = remove_extention(song.info[check_item]) \
                + "." + format

        for file_name in file_names:
            #print " ", item, file
            if search and item.lower() == file_name.lower():
                #print "exact file"
                found = True
                song.info[check_item] = file_name
                break
                # search for the right endings
                # if thats the wrong file i cant detect it,
                # but better we find sometimes a wrong file,
                # instead of no file found
            elif file_name.lower().endswith(format):
                #print "found a file with right ending", file
                files_with_right_format.append(file_name)
        if found:
            break
    else:
        __search_item_with_bogus__(
            files_with_right_format, song, check_item)



def __search_item_with_bogus__(files_with_right_format, song, check_item):
    ''' i take it if its more i think i better dont take it
    because its to dangerous that its not the right file.'''

    if len(files_with_right_format) == 1:
        #print "FOUND 1 file with right ending but wrong name
        #i take what i get: files_with_right_format[0]
        song.info[check_item] = files_with_right_format[0]
    else:
        #print "found some files with right ending for
        # + check_item + ": ", len (files_with_right_format)
        for file_name in files_with_right_format:
            # bad hack but the covers have often a substring [CO]
            if (file_name.lower().find(check_item)) != -1 \
                    or (file_name.lower()).find("co") != -1:
                song.info[check_item] = file_name
                break
#					else:
#						print file, ": ",file.lower().find(check_item), \
#						    (file.lower()).find("co")
        else:
            #print "\t\t\t<<<<<<<<<<<<<not Found>>>>>>>>>>>>>>>>>"
            if check_item in song.info:
                del song.info[check_item]



def remove_extention(file_name):
    """Remove last extention from a filename-string"""
    file_name_parts = file_name.split('.')
    return '.'.join(file_name_parts[:-1])


def unicode_encode_list(elements):
    """encode each string in a string-list to unicode"""
    new_list = []
    for elem in elements:
        try:
            new_list.append(elem.decode('utf-8'))
        except UnicodeEncodeError:
            new_list.append(elem.decode('iso-8859-1'))
    return new_list
