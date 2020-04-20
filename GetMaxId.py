#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  GetMaxId.py
#  
#  Copyright 2020 Unknown <saharul@MXLinux>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


CSV_FILE = "ServisMaster.csv"


# FUNCTION TO GET THE MAXIMUM ID IN THE DB
def GetMaxId():
    with open(CSV_FILE,"r") as f:
        for line in f:
            line = line.rstrip()
            Id = line.split(",", 1)
            if not line: continue
        return(Id[0])

#GetMaxId()
