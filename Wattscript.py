import requests,sys,os

def chaplist(html_s):
	caps = {}
	for i in range(len(html_s)):
		if 'Get notified when' in html_s[i]:
			break
		elif 'new-part-icon' in html_s[i]:
			capName = html_s[i+3].split('<')[0]
			capUrl = html_s[i-3].split('"')[1]
			caps[capName] = capUrl

	if caps=={}:
		return False

	return caps

# começo do programa
headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'}
cookies = {'wp_id':'120acbd0-70d2-4f60-9f6a-70f579fa6cbe',
	'sn__time':'j%3Anull',
	'locale':'pt_PT',
	'lang':'6',
	'fs__exp':'1',
	'RT':'',
}

baseurl = 'https://www.wattpad.com'
#url = 'https://www.wattpad.com/story/164450444-democracinha-ciro-x-haddad'

url = input('-> url do wattpad (url da historia toda e nao de um capitulo):https://www.wattpad.com/story/229634756?utm_source=android&utm_medium=link&utm_content=story_info&wp_page=story_details_button&wp_uname=ReskiAmelia272&wp_originator=Se6WzqfNotvKZzYkjmRudK08aCWX7qoeLf%2BTa7IYOtyca6CKpAEvbpVE5oUnVVP9cUy2oR2Eq6lEc%2FktHpXSGuan66IdwKJlXoswPSar4miIpx%2BgHrNehx%2F2PR3HbrTL ')
fanfic_title = input('\n -> titulo da historia para salvar: The Bringer of Destruction').strip()

if url=='' or fanfic_title=='':
	exit(3)

chapters_url = []

html = requests.get(url,headers=headers,cookies=cookies).text
html_s = html.split('>')

# nome dos capitulos:
chapters = chaplist(html_s)
default_chapname = False

print('\n[*] downloading %s'%fanfic_title)

if chapters==False:
	sys.stderr.write('[!] nao foi possivel pegar a lista de capitulos\n')
	sys.exit(404)

all_fanfic = '<head><meta charset="utf-8"/><style rel="stylesheet"> h1 {font-size:33} h2 {font-size:29.5} body {padding:6px} p {font-size:25;} </style></head> <body> <h1 style="text-align:center">%s</h1>'%fanfic_title.title()

#if not default_chapname:
	#all_fanfic += '<h2 style="text-align:center">%s</h2>'%chapters_name[0]

cont = 0
for chapter in chapters:
	chap = chapters[chapter]
	cont_page = 1
	
	all_fanfic += '<h2 style="text-align:center">'+chapter+'</h2><span style="text-align:justify">'

	chaphtml = ''
	while True: # busca todas as paginas de cada capitulo
		chap_pag = chap+'/page/%d'%cont_page
		chaphtml_ = requests.get(chap_pag,headers=headers,cookies=cookies).text
		
		# verifica se é o ultima pag do capitulo
		if 'data-p-id="' in chaphtml_:
			chaphtml = chaphtml_
		else:
			break

		cont_page += 1
		all_fanfic += chaphtml[chaphtml.index('<pre>')+5 : chaphtml.index('</pre>')]
	
	cont += 1

all_fanfic += '</span></body>'

with open('%s.html'%fanfic_title,'w',encoding="utf-8") as f:
	f.write(all_fanfic)

print('[*] gerando pdf')
r = os.system(f'wkhtmltox\\bin\\wkhtmltopdf.exe {fanfic_title}.html {fanfic_title}.pdf 2> nul')
downloadUrl = ''

if r==0:
    downloadUrl = os.popen(f'curl -s --upload-file {fanfic_title}.pdf https://free.keep.sh').read().rstrip()+'/download'
    os.remove('%s.html'%fanfic_title)
else:
    print('[!] Erro ao converter para pdf')
    print('[*] Arquivo Baixado: %s.html\n'%fanfic_title)
    os.system('pause')
    sys.exit(3)

print('[*] Convertido com sucesso\n')
print('[*] Arquivo Baixado: %s.pdf'%fanfic_title)
print('[*] Arquivo para Download: %s\n'%downloadUrl)
os.system('pause')
