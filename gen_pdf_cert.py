#!/usr/local/bin/python
# coding: utf-8
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import csv

#string constants
filename = "sample_results_raw.csv"

title_cn = "第八届黄河杯中文有奖阅读竞赛"
title_en = "THE 8TH YELLOW RIVER CUP CHINESE READING CONTEST"

committee_cn="北美黄河杯中文竞赛委员会"
committee_en="NORTH AMERICAN YELLOW RIVER CUP"
committee_en2 ="CHINESE CONTEST COMMITTEE"
date_of_completion="09/30/2019"

level_1_cn="初级"
level_2_cn="中级"

first_place="一等奖 FIRST PLACE"
second_place="二等奖 SECOND PLACE"
third_place="三等奖 THIRD PLACE"
completion="完成 COMPLETION"

#calculations
half_x = 5.5*inch
total_score_level_1 = 1643
total_score_level_2 = 1360
total_num_essays_level_1 = '99'
total_num_essays_level_2 = '90'

def generate_certificate(entry):
	level = entry[0]
	name = entry[1]
	name_cn = entry[2]
	score = int(entry[4])
	finished = entry[6]

	#only process students who completed all essays
	if level == '1' and finished.split(" ")[0] != total_num_essays_level_1:
		return
	elif level == '2' and finished.split(" ")[0] != total_num_essays_level_2:
		return

	c = canvas.Canvas("results/" + name + ".pdf", pagesize=landscape(letter))

	#background
	img_path = 'images/background.jpg'
	c.drawImage(image=img_path,x=0.25*inch,y=0.25*inch,width=10.5*inch,height=8.0*inch, mask='auto')
	
	#gold border
	c.setStrokeColorRGB(0.999,0.799,0.066)
	c.setFillColor(Color(100,100,100, alpha=0.25))
	c.setLineWidth(3)
	c.rect(0.0625*inch,0.0625*inch,10.875*inch,8.375*inch,fill=1)
	c.setStrokeColorRGB(1.0,0.8,0.067)
	c.setFillColor(Color(100,100,100, alpha=0.1))
	c.setLineWidth(1)
	c.rect(0.125*inch,0.125*inch,10.75*inch,8.25*inch,fill=1)
	
	#title	
	c.setStrokeColorRGB(0.0,0.0,0.0)
	c.setFillColor(Color(0,0,0, alpha=1.0))
	c.setFont('Helvetica', 24)
	c.drawCentredString(half_x,7.5*inch, "CERTIFICATE OF ACHIEVEMENT")
	c.setStrokeColorRGB(0.9,0.0,0.0)
	c.setFillColorRGB(0.9,0.0,0.0)
	c.setFont('Kaiti', 36)
	c.drawCentredString(half_x,6.95*inch, title_cn)
	c.setFont('Helvetica', 24)
	c.drawCentredString(half_x,6.5*inch, title_en)

	#name
	c.setStrokeColorRGB(0.0,0.0,0.0)
	c.setFillColorRGB(0.0,0.0,0.0)
	c.setFont('STHeiti', 30)
	c.drawCentredString(half_x,4.75*inch,name_cn +"   " + name)

	#line
	c.setLineWidth(.3)
	c.line(3*inch,4.65*inch,8*inch,4.65*inch)
	c.line(3*inch,4.62*inch,8*inch,4.62*inch)

	#scoring logic
	c.setFont('STHeiti', 28)
	if level == '1':
		total_score = total_score_level_1
		level=level_1_cn
	elif level == '2':
		total_score = total_score_level_2
		level=level_2_cn

	if score / total_score >= 0.9:
		place = first_place
	elif 0.8 <= score / total_score < 0.9:
		place = second_place
	elif 0.7 <= score / total_score < 0.8:
		place = third_place
	else:
		place = completion
	c.drawCentredString(half_x,4.25*inch,level+place)

	#footer 
	c.setFont('Kaiti', 24)
	c.drawCentredString(half_x,2.33*inch,committee_cn)
	c.setFont('Helvetica', 20)
	c.drawCentredString(half_x,2.00*inch,committee_en)
	c.drawCentredString(half_x,1.67*inch,committee_en2)
	c.drawCentredString(half_x,1.33*inch,date_of_completion)

	#logo
	img_path = 'images/logo_transparent.png'
	c.drawImage(image=img_path,x=9*inch,y=1*inch,width=inch,height=inch, mask='auto')

	#stamp
	c.setStrokeColorRGB(0.8,0.0,0.0)
	c.setFillColorRGB(0.8,0.0,0.0)
	c.setFont('Helvetica', 14)
	c.drawCentredString(1.5*inch,2.3*inch,"DIRECTOR")
	c.drawCentredString(1.5*inch,2.05*inch,"JIMMY GAO")
	img_path = 'images/stamp_transparent.png'
	c.drawImage(image=img_path,x=1*inch,y=1*inch,width=inch,height=inch, mask='auto')
	 
	#output
	c.save()
 
#main
if __name__ == '__main__':
	pdfmetrics.registerFont(TTFont('STHeiti', 'STHeiti Medium.ttc')) 
	pdfmetrics.registerFont(TTFont('Kaiti', 'AR PL UKai CN, Regular.ttc'))

	with open(filename, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		# field names in first row 
		csvreader.__next__() 

		for row in csvreader: 
			generate_certificate(row)
