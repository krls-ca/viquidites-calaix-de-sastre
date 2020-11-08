# -*- coding: utf-8 -*-

'''
Copyright 2020 Carles Paredes Lanau <carlesparedes@gmail.com>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pywikibot
import re
from itertools import *

def main():
	output_page = {u'Dita': 'Template:NUMBEROFPROVERBS', u'Frase feta' : u'Template:NUMBEROFSETPHRASES', u'Cita': 'Template:NUMBEROFQUOTES', u'Endevinalla': 'Template:NUMBEROFRIDDLES'}
	templates = [u'Dita', u'Frase feta' , u'Cita', u'Endevinalla']
	site = pywikibot.Site("ca", "wikiquote")
	for template in templates:
		page = pywikibot.Page(site, u'Template:{0}'.format(template))
		text = page.get()
		it = page.embeddedin(namespaces=0, content=True)
		array = list(it)
		total = 0
		eval_sentence = u'(?:{0}|{1})(.*?)'.format(template, template.lower())
		regex = '\{{2}' + eval_sentence + '\}{2}'
		for pg in array:
			pg.text = re.sub(r'\{{2}sfn\|(?:.*?)\}{2}', '', pg.text)
			template_uses = re.findall(regex, pg.text, re.S)
			total = total + len(template_uses)
			for use in template_uses:
				template_uses = re.findall('[v|V]ariant[0-9]{0,2}\s*=\s*(.+?)\n', use, re.S)
				total = total + len(template_uses)
		if output_page[template]:
			output = output_page[template]
			page = pywikibot.Page(site, output)
			text = page.get()
			page.put(total, comment=u'Actualitzant el nombre d\'inclusions de la plantilla', minorEdit = True)
if __name__ == '__main__':
	main()
