# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 13:34:40 2018

@author: Goldy
"""

#Reading pcap file

import pyshark

cap=pyshark.FileCapture('C:\Final Year Project\Implementation\pyshark.pcap')
cap
for packet in cap:
	print packet
