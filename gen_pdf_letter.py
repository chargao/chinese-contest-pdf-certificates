#!/usr/local/bin/python
# coding: utf-8
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, portrait
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import csv
styles = getSampleStyleSheet()

#string variables
# filename = "sample_results_raw.csv"
filename = "2022.csv"
logo_img_path = 'images/logo_transparent.png'
stamp_img_path = "images/stamp_transparent.png"

title_cn = "给第十一届黄河杯中文阅读竞赛获奖学生的贺信"
title_en = "Congratulations to the winners of the 11th Yellow River Cup Chinese Reading Competition"

header= "亲爱的 %s %s 同学："

bodyp1 = """恭喜你在“第十一届北美黄河杯中文阅读竞赛”中获得了%s%s！在这一次竞赛
中，你读了%d篇文章，共%d万字的阅读量；回答了%d道题目，获得了%d分，正确率
%s%% 的好成绩，是本届竞赛%s第%d高分！特别值得表扬和鼓励。"""
body_prize = "你将获得$%d奖金，以资鼓励。"
body = ["",
"""学习语言的四个关键是听、说、读、写。目前，你的中文阅读已经达到了一定的水平
，希望你中文的写作水平也能得到相应的提高。eWriteChinese.com团队专门为北美学生们
设计了网上中文的读写课程，如果你想选修一期eWrite 写作课程、中文AP 或者中华文化
online 课程，你可以享受5% 的优惠。你的优惠编码为2023eW，也可以转送给你的两位朋
友或同学，有效期截止到2023年3月31日。""",
"""“第十二届北美黄河杯中文有奖阅读竞赛”仍分初级、中级和高级，将在2023年暑假
进行。初级阅读材料为《群星闪烁》，中级阅读材料为《山西故事•成语传说》，高级阅
读材料为中国四大名著之一《红楼梦》。阅读竞赛预定于明年5月1日开始报名，8月31
日答题结束。""",
"""本竞赛规定凡是在初级、中级阅读竞赛中，分别获得了两次前三名的学生，不再参加
同级的竞赛。预祝你在今后的学习中取得更大的进步！"""]

footer = ["NORTH AMERICAN YELLOW RIVER CUP",
	"CHINESE CONTEST COMMITTEE",
	"主任 Director：高继国 Jimmy Gao"]

date="2022年9月15日"

max_essays=[99,95,40]
word_totals=[6,7,21]
num_questions=[990,950,800 ]
max_scores=[1643,1455,1317]

#constants
bodystyle = ParagraphStyle('bodystyle',
	fontName="STHeiti",
	fontSize=12,
	parent=styles['Normal'],
	alignment=4, # justify
	leading=16, # spacing between lines
	spaceAfter=6, # spacing after paragraph
	firstLineIndent=24,
	wordWrap='CJK')

footerstyle = ParagraphStyle('footerstyle',
	fontName="STHeiti",
	fontSize=10,
	parent=styles['Normal'],
	alignment=2, # right
	leading=12, # spacing between lines
	spaceAfter=2, # spacing after paragraph
	wordWrap='CJK')

#string constants
levels_cn=["初级","中级","高级"]
awards=["完成","一等奖","二等奖","三等奖", "鼓励奖","荣誉奖"]
prize_amounts = [50,25,15]
prize_winners = [[1,2,10],[1,2,3],[1,1,1]]

##############################################################################

def generate_letter(row):
	level = int(row[0])
	name = row[1].strip()
	name_cn = row[2].strip()
	score = int(row[4])
	place = int(row[5])
	finished_essays = int(row[6].split(" ")[0])
	awarded = int(row[7])
	
	if awarded == 0:
		return # no award
	award = awards[awarded]

	word_total = word_totals[level-1]
	max_score = max_scores[level-1]
	total_essays = max_essays[level-1]
	level_cn = levels_cn[level-1]
	
	# prize amount computation
	prize_amount = prize_amounts[level-1]
	prize_amount = int(row[8]) #temporary, for this time around

	# bodyp1 = """恭喜你在“第十届北美黄河杯中文阅读竞赛”中获得了%s%s！在这一次竞赛
	# 中，你读了%d篇文章，共%d万字的阅读量；回答了%d道题目，获得了%d分，正确率
	# %s% 的好成绩，是本届竞赛初级第%d高分！特别值得表扬和鼓励。"""

	body[0] = bodyp1 % (level_cn,award,finished_essays,word_total,finished_essays*10,score,str(round((score/max_score)*100,1)),level_cn,place)

	if prize_amount != 0:
		body[0] = body[0] + (body_prize % prize_amount)

	build_doc(name,name_cn)

def build_doc(name,name_cn):
	doc = SimpleDocTemplate("results/"+name+" letter.pdf", pagesize = letter)
	Story = [Spacer(1,2*inch)]

	# header
	p = Paragraph("<para firstLineIndent=0>"+ header % (name, name_cn) + "</para>", bodystyle)
	Story.extend([p,Spacer(1,0.2*inch)])

	# fuck with body[0] here
	for para in body:
		p = Paragraph(para, bodystyle)
		Story.extend([p,Spacer(1,0.2*inch)])
	
	#footer
	Story.append(Spacer(1,0.5*inch)) 
	p = Paragraph("<para fontSize=14>北美黄河杯中文竞赛委员会</para>",footerstyle)
	Story.extend([p,Spacer(1,0.1*inch)])
	for line in footer:
		p = Paragraph(line, footerstyle)
		Story.append(p)

	doc.build(Story, onFirstPage=static_elements)

def static_elements(c, doc):
	c.saveState()
	c.drawImage(
		image=logo_img_path,
		x=3.75*inch,y=9.5*inch,
		width=inch,height=inch, 
		mask='auto')
	c.setFont('STHeiti',18)
	c.drawCentredString(4.25*inch, 9*inch, title_cn)
	c.setFont('Helvetica', 12)
	c.drawCentredString(4.25*inch, 8.7*inch, title_en)
	c.setFont('STHeiti',9)
	c.drawString(5.6*inch, 1.4*inch, date)
	c.drawImage(
		image=stamp_img_path,
		x=6.6*inch,y=0.75*inch,
		width=0.75*inch,height=0.75*inch, 
		mask='auto')
	c.restoreState()

#main
if __name__ == '__main__':
	pdfmetrics.registerFont(TTFont('STHeiti', 'STHeiti Medium.ttc'))

	with open(filename, 'r') as csvfile: 
		csvreader = csv.reader(csvfile) 
		
		# field names in first row 
		csvreader.__next__() 

		for row in csvreader: 
			print(row[1].strip())
			generate_letter(row)
