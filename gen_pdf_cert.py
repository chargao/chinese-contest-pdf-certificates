#!/usr/local/bin/python
# coding: utf-8
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import csv
import os

#string variables
filename = "example_input.csv"
bg_img_path = 'images/library_bg3.png'
logo_img_path = 'images/logo_transparent.png'
stamp_img_path = "images/stamp_transparent.png"

title_cn = "第十三届黄河杯中文有奖阅读竞赛"
title_en = "THE 13TH YELLOW RIVER CUP CHINESE READING CONTEST"

committee_cn="北美黄河杯中文竞赛委员会"
committee_en=["NORTH AMERICAN YELLOW RIVER CUP","CHINESE CONTEST COMMITTEE"]
today=datetime.today().strftime('%Y-%m-%d')

#string constants
level_cn=["初级","中级","高级"]
level_en=["BEGINNER","INTERMEDIATE","ADVANCED"]

places=["完成 COMPLETION",
		"一等奖 FIRST PLACE",
		"二等奖 SECOND PLACE",
		"三等奖 THIRD PLACE",
		"鼓励奖 ENCOURAGEMENT AWARD",
		"荣誉奖 HONORARY AWARD"]

#calculations
half_x = 5.5*inch

##############################################################################

def generate_certificate(entry):
	level = entry[0]
	name = entry[1].strip()
	name_cn = entry[2].strip()
	place = entry[5]

	# assign places based on "place" column in csv
	if place == '0':
		return # no award
	else:
		place= places[int(place)]

	# set text for context level in cert
	lvl_en = level_en[int(level)-1]
	lvl_cn = level_cn[int(level)-1]

	# create canvas
	# c = canvas.Canvas("results/"+lvl_en.lower()+"_"+name+"_certificate.pdf", pagesize=landscape(letter))
	c = canvas.Canvas(
		"results/"+lvl_en.title()+"_"+name+"_Certificate.pdf", 
		pagesize=landscape(letter))
	draw_static_elements(c)

	# certificate type
	c.setStrokeColor(black)
	c.setFillColor(Color(0,0,0, alpha=1.0))
	c.setFont('Helvetica', 24)
	if place != places[4]:
		c.drawCentredString(half_x,7.5*inch, "CERTIFICATE OF ACHIEVEMENT")
	else:
		c.drawCentredString(half_x,7.5*inch, "CERTIFICATE OF ENCOURAGEMENT")

	#awardee name
	c.setFont('STHeiti', 30)
	c.drawCentredString(half_x,4.75*inch,name_cn +"    " + name)

	c.setFont('STHeiti', 28)
	c.drawCentredString(half_x,4.25*inch,lvl_cn + place)
	 
	#output
	c.save()

def draw_static_elements(c):
	#background
	c.drawImage(image=bg_img_path,x=0.25*inch,y=0.25*inch,width=10.5*inch,height=8.0*inch, mask='auto')
	
	#gold border
	c.setStrokeColorRGB(1.0,0.8,0.067)
	c.setFillColor(Color(100,100,100, alpha=0.25))
	c.setLineWidth(3)
	c.rect(0.0625*inch,0.0625*inch,10.875*inch,8.375*inch,fill=1)
	c.setLineWidth(1)
	c.rect(0.125*inch,0.125*inch,10.75*inch,8.25*inch,fill=1)

	#title	
	c.setStrokeColor(black)
	c.setFillColor(Color(0,0,0, alpha=1.0))
	c.setStrokeColorRGB(0.9,0.0,0.0)
	c.setFillColorRGB(0.9,0.0,0.0)
	c.setFont('Kaiti', 36)
	c.drawCentredString(half_x,6.95*inch, title_cn)
	c.setFont('Helvetica', 24)
	c.drawCentredString(half_x,6.5*inch, title_en)

	#line
	c.setLineWidth(.3)
	c.setStrokeColor(black)
	c.setFillColor(Color(0,0,0, alpha=1.0))
	c.line(3*inch,4.65*inch,8*inch,4.65*inch)
	c.line(3*inch,4.62*inch,8*inch,4.62*inch)

	#footer 
	c.setFont('Kaiti', 24)
	c.drawCentredString(half_x,2.33*inch,committee_cn)
	c.setFont('Helvetica', 20)
	c.drawCentredString(half_x,2.00*inch,committee_en[0])
	c.drawCentredString(half_x,1.67*inch,committee_en[1])
	c.drawCentredString(half_x,1.33*inch,today)

	#logo
	c.drawImage(image=logo_img_path,x=9*inch,y=1*inch,width=inch,height=inch, mask='auto')

	#stamp
	c.setStrokeColorRGB(0.8,0.0,0.0)
	c.setFillColorRGB(0.8,0.0,0.0)
	c.setFont('Helvetica', 14)
	c.drawCentredString(1.5*inch,2.3*inch,"DIRECTOR")
	c.drawCentredString(1.5*inch,2.05*inch,"JIMMY GAO")
	c.drawImage(image=stamp_img_path,x=1*inch,y=1*inch,width=inch,height=inch, mask='auto')
 
#main
if __name__ == '__main__':
	pdfmetrics.registerFont(TTFont('STHeiti', 'stheiti.ttf')) 
	pdfmetrics.registerFont(TTFont('Kaiti', 'ukai.ttc'))

	if not os.path.exists('results'):
		os.makedirs('results')

	with open(filename, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		# field names in first row 
		csvreader.__next__() 

		for row in csvreader: 
			print(row)
			generate_certificate(row)
