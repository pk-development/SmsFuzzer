#!/usr/bin/env python

# Copyright 2017 Paul Kinsella <>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import wx
from smsfuzzer_funcs import * 

mySerialPort = serial.Serial()
mySerialPort.port = 	"/dev/ttyUSB0" #default so not null
mySerialPort.baudrate = 9600
mySerialPort.bytesize = serial.EIGHTBITS #number of bits per bytes
mySerialPort.parity = 	serial.PARITY_NONE #set parity check: no parity
mySerialPort.stopbits = serial.STOPBITS_ONE #number of stop bits
mySerialPort.timeout = 	0             #non-block read
mySerialPort.xonxoff = 	False     #disable software flow control
mySerialPort.rtscts = 	False     #disable hardware (RTS/CTS) flow control
mySerialPort.dsrdtr = 	False       #disable hardware (DSR/DTR) flow control


WAP_TYPE = [ 
"01",
"02",
"03",
"04",
"05",
"06",
"07",
"08",
"09",
"0A",
"0B",
"0C",
"0D",
"0E",
"0F"]

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,size=(220,350),title='Wap Push')
        panel = wx.Panel(self)

	#####################################################
	#MISC FUCTIONS
	#####################################################
	tested_ports = getOpenSerialPorts()
	if len(tested_ports) < 1:
		tested_ports.append("NO PORTS")

	#####################################################
	#BUTTON FUCTIONS
	#####################################################
	def onPduModeClick(event):
        	wx.MessageBox(getAtReply(self.combo_serial_ports.GetValue(),"AT+CMGF=0"), 'Info', 
            	wx.OK | wx.ICON_INFORMATION)
		

	def onSendClick(event):
		mySerialPort.port = self.combo_serial_ports.GetValue()
                WAP_PDU_STRING = createWapPduString(self.edit_start_date.GetValue(),
						self.edit_end_date.GetValue(),
						self.edit_header.GetValue(),
						self.edit_target_number.GetValue(),
						self.edit_target_msg.GetValue(),
						self.combo_wap_types.GetValue())

		self.edit_debug.SetValue(WAP_PDU_STRING)

		if mySerialPort.open() == False:
			mySerialPort.open()
	
		if mySerialPort.isOpen():
			mySerialPort.flushInput() #flush input buffer, discarding all its contents
        		mySerialPort.flushOutput()#flush output buffer, aborting current output
			mySerialPort.write("AT+CMGS=17"+"\x0D")
			time.sleep(0.3)
			mySerialPort.write(WAP_PDU_STRING+"\x1A")
			time.sleep(0.3)
			bytesToRead = mySerialPort.inWaiting()
			ress = mySerialPort.read(bytesToRead)
        		wx.MessageBox(ress, 'Info', 
            		wx.OK | wx.ICON_INFORMATION)
		else:
			wx.MessageBox('Message did not send', 'Info', 
            		wx.OK | wx.ICON_INFORMATION)

		mySerialPort.close()

	self.lb_comport = wx.StaticText(panel, label="Com Port:",pos=(5,5))
	self.combo_serial_ports = wx.ComboBox(panel,size=(135,30), pos=(80,5), choices=tested_ports, style=wx.CB_READONLY)
	self.combo_serial_ports.SetSelection(0)

	self.lb_start_date = wx.StaticText(panel, label="Start Date:",pos=(5,35))
	self.edit_start_date = wx.TextCtrl(panel,size=(135,30), pos=(80,35),value='201502012221')

	self.lb_end_date = wx.StaticText(panel, label="End Date:",pos=(5,65))
	self.edit_end_date = wx.TextCtrl(panel,size=(135,30), pos=(80,65),value='201502212230')

	self.lb_header = wx.StaticText(panel, label="Header:",pos=(5,95))
	self.edit_header = wx.TextCtrl(panel,size=(135,30), pos=(80,95),value='www.headerhere.com')

	self.lb_target = wx.StaticText(panel, label="Target No:",pos=(5,125))
	self.edit_target_number = wx.TextCtrl(panel,size=(135,30), pos=(80,125),value='123456789012')

	self.lb_target_data = wx.StaticText(panel, label="Sms Msg:",pos=(5,155))
	self.edit_target_msg = wx.TextCtrl(panel,size=(135,60), pos=(80,155),value='Hello World',style=wx.TE_MULTILINE)


	self.btnpdumode = wx.Button(panel, label="Pdu Mode",pos=(5,215),size=(85,30))
	self.btnpdumode.Bind(wx.EVT_BUTTON,onPduModeClick)

	self.combo_wap_types = wx.ComboBox(panel,pos=(90,215),size=(80,30), choices=WAP_TYPE, style=wx.CB_READONLY)
	self.combo_wap_types.SetSelection(11)

	self.btnsend = wx.Button(panel, label="Send",pos=(170,215),size=(45,30))
	self.btnsend.Bind(wx.EVT_BUTTON,onSendClick)

	self.lb_output = wx.StaticText(panel, label="Debug:",pos=(5,240))
	self.edit_debug = wx.TextCtrl(panel,size=(210,70), pos=(5,265),value='',style=wx.TE_MULTILINE)

	



app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()
