#!/usr/local/bin/python
# coding: utf-8
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import csv

#string variables
filename = "example_input.csv"
bg_img_path = 'images/library_bg3.png'
logo_img_path = 'images/logo_transparent.png'
stamp_img_path = "images/stamp_transparent.png"

title_cn = "第十届黄河杯中文有奖阅读竞赛"
title_en = "THE 10TH YELLOW RIVER CUP CHINESE READING CONTEST"

committee_cn="北美黄河杯中文竞赛委员会"
committee_en=["NORTH AMERICAN YELLOW RIVER CUP","CHINESE CONTEST COMMITTEE"]
date_of_completion="09/15/2021"

#string constants
level_1_cn="初级"
level_2_cn="中级"
level_3_cn="高级"
level_1_en="BEGINNER"
level_2_en="INTERMEDIATE"
level_3_en="ADVANCED"

places=["完成 COMPLETION","一等奖 FIRST PLACE","二等奖 SECOND PLACE","三等奖 THIRD PLACE", "鼓励奖 ENCOURAGEMENT AWARD","荣誉奖 HONORARY AWARD"]

#calculations
half_x = 5.5*inch
# total_score_level_1 = 1643
# total_score_level_2 = 1360
# total_num_essays_level_1 = '123'
# total_num_essays_level_2 = '88'

##############################################################################

def generate_certificate(entry):
	level = entry[0]
	name = entry[1].strip()
	name_cn = entry[2].strip()
	# score = int(entry[4])
	# finished = entry[6]
	award_level = entry[7]

	#only process students who completed all essays or passed by 70%
	# commented out because of award_level column
	# place = ''
	# if level == '1' and finished.split(" ")[0] != total_num_essays_level_1:
	# 	if .7 <= score / total_score_level_1:
	# 		place=places[4]
	# 	else:
	# 		return
	# elif level == '2' and finished.split(" ")[0] != total_num_essays_level_2:
	# 	if .7 <= score / total_score_level_2:
	# 		place=places[4]
	# 	else:
	# 		return
	place = places[0]
	if award_level == '0':
		return # no award
	elif award_level == '1':
		place = places[1] # 一等奖 FIRST PLACE
	elif award_level == '2':
		place = places[2] # 二等奖 SECOND PLACE
	elif award_level == '3':
		place = places[3] # 三等奖 THIRD PLACE
	elif award_level == '4':
		place = places[4] # 鼓励奖 ENCOURAGEMENT AWARD
	elif award_level == '5':
		place = places[5] # 荣誉奖 HONORARY AWARD

	lvl_en=''
	if level == '1':
		#total_score = total_score_level_1
		level=level_1_cn
		lvl_en=level_1_en
	elif level == '2':
		#total_score = total_score_level_2
		level=level_2_cn
		lvl_en=level_2_en
	elif level == '3':
		#total_score = total_score_level_3
		level=level_3_cn
		lvl_en=level_3_en

	# create canvas
	c = canvas.Canvas("results/" +str(i)+"_"+lvl_en+"_"+ name + ".pdf", pagesize=landscape(letter))
	draw_static_elements(c)

	# certificate type
	c.setStrokeColor(black)
	c.setFillColor(Color(0,0,0, alpha=1.0))
	c.setFont('Helvetica', 24)
	# if place != places[4]:
	# 	c.drawCentredString(half_x,7.5*inch, "CERTIFICATE OF ACHIEVEMENT")
	# else:
	# 	c.drawCentredString(half_x,7.5*inch, "CERTIFICATE OF ENCOURAGEMENT")

	#awardee name
	c.setFont('STHeiti', 30)
	c.drawCentredString(half_x,4.75*inch,name_cn +"   " + name)

	c.setFont('STHeiti', 28)
	c.drawCentredString(half_x,4.25*inch,level+place)
	 
	#output
	c.save()

def draw_static_elements(c):
	#background
	c.drawImage(image=bg_img_path,x=0.25*inch,y=0.25*inch,width=10.5*inch,height=8.0*inch, mask='auto')
	
	#gold border
	c.setStrokeColorRGB(0.999,0.799,0.066)
	c.setFillColor(Color(100,100,100, alpha=0.25))
	c.setLineWidth(3)
	c.rect(0.0625*inch,0.0625*inch,10.875*inch,8.375*inch,fill=1)
	c.setStrokeColorRGB(1.0,0.8,0.067)
	c.setFillColor(Color(100,100,100, alpha=0.25))
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
	c.drawCentredString(half_x,1.33*inch,date_of_completion)

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
	pdfmetrics.registerFont(TTFont('STHeiti', 'STHeiti Medium.ttc')) 
	pdfmetrics.registerFont(TTFont('Kaiti', 'AR PL UKai CN, Regular.ttc'))

	with open(filename, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		# field names in first row 
		csvreader.__next__() 

		for row in csvreader: 
			print(row[1].strip())
			generate_certificate(row)
