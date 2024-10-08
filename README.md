# chinese-contest-pdf-certificates

Small Python script for automating the process of generating PDF certificates for the [Yellow River Cup Reading Contest](http://ewritechinese.com/contestFAQ/)

## How to Use
Invokation:
```
	source venv/bin/activate	# assuming venv is being used
	python3 gen_pdf_cert.py		# for generating certificates
	python3 gen_pdf_letter.py	# for generating award letters

```

Each script starts with some variable strings, make sure to modify them appropriately for each contest. Maybe in future versions this can be automated, but for now this is fine. :fire:

Fonts may not be pre-installed. If fonts are not present, they can be downloaded online. 

## Input format

_You can also reference `example_input.csv`_

Level|Name|Chinese Name|Email|Score|Place|Number Essays Finished|Award
|-|-|-|-|-|-|-|-|
1|Alice Zhang|张三|a.zhang@fake.edu|1599|1|99 of 99|1
1|Bob Li|李四|b.li@fake.edu|1399|2|99 of 99|2
1|Claire Wang|王五|c.wang@fake.edu|1299|3|99 of 99|3
1|David Zhao|赵六|d.zhao@fake.edu|1099|4|99 of 99|3
2|Emily Sun|孙七|e.sun@fake.edu|1355|1|90 of 90|1
2|Frank Zhou|周八|f.zhou@fake.edu|1199|2|90 of 90|2
2|Grace Wu|吴九|g.wu@fake.edu|1299|3|89 of 90|3
2|Henry Zheng|郑十|h.zheng@fake.edu|199|4|10 of 90|5

## Output
![Example Certificate](/images/example_certificate.png)