#!/usr/bin/env python3
#requires tkinter
# under linux: python-tk
# under windows: usually included in the python installer
#requires inkscape on the path
#ensure the settings are set correctly in inkscape's gui

import subprocess
from tkinter import Tk, filedialog
import pathlib

root = Tk()
root.input_filename = filedialog.askopenfilename(\
	title = "choose file to convert from", \
	filetypes = (("pdf files", "*.pdf"),("svg files","*.svg")) \
	)

if type(root.input_filename) == tuple:
	raise Exception("No input filename provided")

p = pathlib.Path(root.input_filename)
input_dir = p.parent
output_hint = "{}.emf".format(p.name.split(".")[0])

root.output_filename = filedialog.asksaveasfilename(\
	title = "choose file to convert to", \
	defaultextension = ".emf",
	initialdir = input_dir, \
	initialfile = output_hint \
	)

if type(root.output_filename) == tuple:
	raise Exception("No output filename provided")


print("Trying to convert {} to {}".format(root.input_filename, root.output_filename))

cmd = ["inkscape", "-f={}".format(root.input_filename), "--export-emf={}".format(root.output_filename)]

try:
	subprocess.check_call(cmd, stderr=subprocess.STDOUT)
	print("Sucessfully converted")
except CalledProcessError as e:
	print("Conversion failed with error: {}",format(e))