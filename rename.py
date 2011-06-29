#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rename.py
#       
#       Copyright 2011 sony <sony@sony-VGN-CS17G-R>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import sys
import os
import glob
import Image
from PIL import Image
from PIL.ExifTags import TAGS
import calendar

def findImages(directory_name):
	images_list = []
	for filename in glob.glob( os.path.join(directory_name, '*.*') ):
		try:
			im=Image.open(filename)
			images_list.append(filename)
		except IOError:
			pass
			# filename not an image file
	return images_list


        

def getExif(fname):
	ret = {}
	try:
		img = Image.open(fname)
		if hasattr( img, '_getexif' ):
			exifinfo = img._getexif()
			if exifinfo != None:
				for tag, value in exifinfo.items():
					decoded = TAGS.get(tag, tag)
					ret[decoded] = value
	except IOError:
		print 'IOERROR ' + fname
	
	return ret
	
	
def rename_images(images_list):
	for fname in images_list:
		filename_with_path , extension = os.path.splitext(fname)
		path,filename_with_ext = os.path.split(fname)
		ret = getExif(fname)
		if "DateTimeOriginal" in ret:
			yearmonthday,hoursminsec = ret["DateTimeOriginal"].split()
			year,month,day = yearmonthday.split(":")
			hours,minutes,sec = hoursminsec.split(":")
			new_name = year + "_" + calendar.month_abbr[int(month)] + "_" + day + "__" + hours + "_" + minutes + "_" + sec
			os.rename(fname,path + "/"+ new_name + extension)
		else:
			print " not renamed----> " , fname
		

def main():
	directory_name = sys.argv[1]
	images_list = findImages(directory_name)
	rename_images(images_list)
	return 0

if __name__ == '__main__':
	main()

