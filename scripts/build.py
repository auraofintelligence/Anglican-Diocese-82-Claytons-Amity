"""Build the static site from the approved proposal without rewriting its words."""
from pathlib import Path
import re, html, json, hashlib

ROOT=Path(__file__).resolve().parent.parent
BASE='https://auraofintelligence.github.io/Anglican-Diocese-82-Claytons-Amity/'
PAGES=[
 ('index','Welcome','home','A future care and research pavilion surrounded by native gardens and trees.'),
 ('invitation','The invitation','invitation-v2','Generations in conversation on a garden verandah.'),
 ('vision','The wider vision','vision','A luminous globe connecting communities, knowledge and human purpose.'),
 ('community','Community wealth','fund-v2','Generations planting a native tree as a gift to the future.'),
 ('aura-geode','Aura Geode','geode','An imagined immersive capsule in a warm garden-facing research studio.'),
 ('aura-genesis','Aura Genesis','genesis','A person exploring an understandable digital representation of her life.'),
 ('dementia-care','Dementia care','care','A person and carer exploring memories and life stories together.'),
 ('c-hours','C-hours','contribution','Young volunteers and an older mentor creating useful community work.'),
 ('learning','Learning and work','learning','Shared tools, mentoring and practical learning in a community workshop.'),
 ('shared-horizon','Our shared horizon','horizon','An eclipse above Australian woodland, inviting science and discovery.'),
 ('references','References','library','A future research library bringing human knowledge and technology together.')]
chapters=(ROOT/'content/proposal.md').read_text('utf-8').strip().split('---PAGE---')
assert len(chapters)==11
docs=json.loads((ROOT/'content/documents.json').read_text('utf-8'))
websites=json.loads((ROOT/'content/websites.json').read_text('utf-8'))

def esc(s): return html.escape(s,quote=True)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s]+?)\)',lambda m:f'<a href="{esc(html.unescape(m[2]))}">{m[1]}</a>',s)
    s=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\[(\d+(?:,\s*\d+)*)\]',lambda m:'['+', '.join(f'<a class="citation" href="references.html#ref-{n.strip()}" aria-label="Reference {n.strip()}">{n.strip()}</a>' for n in m[1].split(','))+']',s)
    for p in [6,9]:
        s=s.replace(f'page {p}',f'<a href="{PAGES[p-1][0]}.html">page {p}</a>')
    return s

def md(text):
    parts=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        if block.startswith('|'):
            rows=[r.strip().strip('|').split('|') for r in block.splitlines()]
            head='<thead><tr>'+''.join('<th scope="col">'+inline(c.strip())+'</th>' for c in rows[0])+'</tr></thead>'
            body='<tbody>'+''.join('<tr>'+''.join('<td>'+inline(c.strip())+'</td>' for c in r)+'</tr>' for r in rows[2:])+'</tbody>'
            parts.append('<div class="table-wrap"><table>'+head+body+'</table></div>')
        elif block.startswith('#'):
            level=len(block)-len(block.lstrip('#')); label=block[level:].strip()
            parts.append(f'<h{level} id="{slug(label)}">{inline(label)}</h{level}>')
        elif block.startswith('- '):
            parts.append('<ul>'+''.join('<li>'+inline(x[2:])+'</li>' for x in block.splitlines())+'</ul>')
        else:
            ref=re.match(r'\*\*\[(\d+)\]',block)
            attr=f' id="ref-{ref[1]}" class="reference-entry"' if ref else ''
            parts.append(f'<p{attr}>'+inline(block.replace('\n',' '))+'</p>')
    return '\n'.join(parts)

def image(name,alt,cls='',eager=False):
    return f'<img class="{cls}" src="assets/images/{name}.webp" srcset="assets/images/{name}-800.webp 800w, assets/images/{name}.webp 1672w" sizes="100vw" alt="{esc(alt)}" width="1672" height="941" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'
def figure(name,alt):
    return '<figure class="visual-break">'+image(name,alt)+'<figcaption>GenAI concept artwork. '+esc(alt)+'</figcaption></figure>'
def buttons():
    return '<div class="actions"><a class="button" href="invitation.html">Explore the invitation <span aria-hidden="true">↗</span></a><a class="button secondary" href="documents/82-Claytons-Road-Anglican-Partnership-Proposal.pdf">Read the 11-page proposal <span aria-hidden="true">↓</span></a><a class="button secondary" href="documents.html">All 31 source documents <span aria-hidden="true">↗</span></a></div>'
def source_archive():
    content='<section class="source-archive" id="all-documents"><h2>All 31 source documents</h2><p>Original documents supplied for the proposal, including the property research PDF. Select a title to open the original file, or use the <a href="documents.html">searchable document library</a>.</p><ol class="source-list">'
    for d in docs:
        content+=f'<li><a href="{d["file"]}">{esc(d["title"])}</a><span class="source-format">{d["format"]} · {d["bytes"]/1024:.0f} KB</span></li>'
    content+='</ol></section><section class="source-archive" id="supplied-websites"><h2>All 15 supplied websites</h2><p>The project websites shared during development, with repeated links listed once.</p><ul class="source-list">'
    for w in websites:
        content+=f'<li><a href="{esc(w["url"])}">{esc(w["title"])} ↗</a></li>'
    return content+'</ul></section>'

def research_sources():
    supplied={w['url'] for w in websites}
    seen=set(); content='<section class="source-archive" id="research-sources"><h2>Further sources cited in the proposal</h2><p>Published research, organisations, official guidance and additional project pages. The <a href="references.html#ref-1">numbered references</a> explain how each supports the invitation.</p><ul class="source-list">'
    for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s]+?)\)',chapters[-1]):
        if url in seen or url in supplied or url.startswith(BASE):continue
        seen.add(url)
        content+=f'<li><a href="{esc(url)}">{esc(label)} ↗</a></li>'
    return content+'</ul></section>'
def card(p,i):
    return f'<a class="chapter-card tilt" href="{p[0]}.html">'+image(p[2],p[3])+f'<div><span class="chapter-number">{i+1:02d}</span><h3>{esc(p[1])}</h3><span class="card-arrow" aria-hidden="true">↗</span></div></a>'
def shell(title,content,key,hero=None,prev=None,nxt=None):
    nav=''.join(f'<a href="{p[0]}.html"'+(' aria-current="page"' if key==p[0] else '')+'>'+esc(p[1])+'</a>' for p in PAGES)
    nav+='<a href="documents.html"'+(' aria-current="page"' if key=='documents' else '')+'>Document library</a><a href="other-proposals.html"'+(' aria-current="page"' if key=='other-proposals' else '')+'>Other Minjerribah proposals</a>'
    nav+='<a href="source-history.html"'+(' aria-current="page"' if key=='source-history' else '')+'>Source history</a>'
    paging='<nav class="page-turns" aria-label="Previous and next page">'
    if prev:paging+=f'<a class="turn tilt" href="{prev[0]}.html"><span>← Previous page</span><strong>{esc(prev[1])}</strong></a>'
    else:paging+='<a class="turn tilt" href="documents/82-Claytons-Road-Anglican-Partnership-Proposal.pdf"><span>Read offline ↓</span><strong>The complete proposal</strong></a>'
    if nxt:paging+=f'<a class="turn next tilt" href="{nxt[0]}.html"><span>Next page →</span><strong>{esc(nxt[1])}</strong></a>'
    paging+='</nav>'
    desc='A gift for generations: an invitation to Anglican Church Southern Queensland for 82 Claytons Road, Amity, connecting dementia care, research and community wealth.'
    hero_name=hero or 'home'
    return f'''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | A gift for generations</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#073d3d">
<link rel="canonical" href="{BASE}{'' if key=='index' else key+'.html'}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{key}.html"><meta property="og:image" content="{BASE}assets/images/{hero_name}.webp"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head>
<body id="top"><a class="skip" href="#main">Skip to content</a><div class="reading-progress" aria-hidden="true"></div>
<header class="site-header"><a class="brand" href="index.html"><img src="favicon-192.png" alt="" width="48" height="48"><span>A gift for generations<span class="brand-location">82 Claytons Road, Amity</span></span></a><div class="header-actions"><a class="header-pdf" href="documents/82-Claytons-Road-Anglican-Partnership-Proposal.pdf">Read the proposal ↓</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-menu">Explore <span aria-hidden="true">☰</span></button></div></header>
<nav id="site-menu" class="site-menu" aria-label="All pages" hidden>{nav}</nav>
<main id="main">{content}</main>{paging}
<footer class="site-footer"><div><a class="footer-brand" href="index.html">A gift for generations</a><p>Luke Nathan Hayes<br>Strange but True: tech, art and ideas that'll help</p><a href="mailto:auraofintelligence@gmail.com">auraofintelligence@gmail.com</a></div><nav aria-label="Footer"><a href="references.html">References</a><a href="documents.html">All documents</a><a href="source-history.html">Source history</a><a href="other-proposals.html">Other Minjerribah proposals</a><a href="licence.html">Strange But True licence</a><a href="https://github.com/auraofintelligence/Anglican-Diocese-82-Claytons-Amity">GitHub repository</a><a href="https://auraofintelligence.github.io/">Aura of Intelligence</a></nav><p class="footer-note">© 2026 Luke Nathan Hayes. Original concept artwork generated with AI. Supplied property maps retain their original attribution.</p></footer>
<a class="to-top" href="#top" aria-label="Back to top">↑</a></body></html>'''

breaks={1:['fund-v2','care'],2:['genesis','learning'],3:['towers','invitation-v2'],4:['genesis','memory'],5:['geode','memory'],6:['memory','geode'],7:['towers','learning'],8:['contribution','towers'],9:['learning','fund-v2']}
alts={p[2]:p[3] for p in PAGES}|{'memory':'A digital memory palace connecting familiar rooms, objects and life stories.','towers':'Vertical tower gardens bringing fresh food, learning and accessible participation together.'}
for i,(p,text) in enumerate(zip(PAGES,chapters)):
    text=text.strip(); title=text.splitlines()[0][2:]; body=text.split('\n',1)[1].strip()
    content='<section class="hero">'+image(p[2],p[3],eager=True)+'<span class="hero-caption">GenAI concept artwork</span></section>'
    content+=f'<div class="title-block"><div class="page-count">{i+1:02d} / 11</div><div data-proposal><h1>{inline(title)}</h1></div></div>'
    if i==10:
        content+='<nav class="section-links" aria-label="Source collections"><a href="#ref-1">Numbered references</a><a href="#all-documents">All 31 documents</a><a href="#supplied-websites">All 15 websites</a><a href="source-history.html">Development history</a></nav>'
    if i==0:
        content+='<section class="cover-copy"><div data-proposal>'+md(body)+'</div>'+buttons()+'</section>'
        content+='<section class="chapter-index"><h2>Explore the proposal</h2><div class="chapter-grid">'+''.join(card(q,j) for j,q in enumerate(PAGES[1:],1))+'</div></section>'
    else:
        sections=re.split(r'(?=^## )',body,flags=re.M)
        toc=''.join(f'<a href="#{slug(s.splitlines()[0][3:])}">{esc(s.splitlines()[0][3:])}</a>' for s in sections if s.startswith('## '))
        if toc:content+='<nav class="section-links" aria-label="On this page">'+toc+'</nav>'
        for j,s in enumerate(sections):
            content+='<section class="prose-section"><div class="prose" data-proposal>'+md(s)+'</div></section>'
            if i in breaks and j in [1,2] and j<len(sections)-1:
                name=breaks[i][j-1];content+=figure(name,alts[name])
            if i==1 and j==1:
                content+='''<section class="property-section"><div class="section-intro"><h2>The property</h2><p>Supplied satellite and working measurement images of 82 Claytons Road beside Claytons Road, Amity. Select either image to view it at full size.</p></div><div class="property-grid">'''
                for name,label in [('claytons-satellite','Supplied satellite reference'),('claytons-measurement','Supplied working boundary measurement')]:
                    content+=f'<figure><a href="assets/images/{name}.webp"><img src="assets/images/{name}.webp" alt="{label} of 82 Claytons Road" loading="lazy" width="1920" height="1200"></a><figcaption>{label}. Google Maps; original attribution retained.</figcaption></figure>'
                content+='</div><a class="button secondary" href="documents/'+docs[-1]['file'].split('/')[-1]+'">Read the original property document ↓</a></section>'
        if i==10:
            content+=source_archive()+'<section class="library-invitation"><h2>Follow the development of the proposal</h2><p>See how the source material and the decisions made during development shaped the invitation.</p><a class="button" href="source-history.html">Read the source history ↗</a></section>'
    if i in [0,3,8]:
        content+='<section class="library-invitation"><h2>Other proposals for the Indigenous community</h2><p>Explore related Minjerribah ideas for living, culture, recovery, safety, learning and useful work.</p><a class="button" href="other-proposals.html">Explore the wider Minjerribah proposals ↗</a></section>'
    (ROOT/(p[0]+'.html')).write_text(shell(title,content,p[0],p[2],PAGES[i-1] if i else None,PAGES[i+1] if i<10 else ('documents','Document library')),'utf-8')

content='<section class="hero">'+image('library',alts['library'],eager=True)+'<span class="hero-caption">GenAI concept artwork</span></section><div class="title-block"><h1>Document library</h1></div><section class="library-intro"><p>All 31 supplied documents, including the original property PDF. These documents trace the development of the ideas; the approved proposal brings them together in their current form.</p><div class="actions"><a class="button" href="documents/82-Claytons-Road-Anglican-Partnership-Proposal.pdf">Read the complete 11-page proposal ↓</a><a class="button secondary" href="documents/31-82-claytons-road-amity-minjerribah.pdf">82 Claytons Road: title search and property research ↗</a></div><div class="library-tools"><label for="document-search">Find a document</label><input id="document-search" type="search" placeholder="Try dementia, C-hour, property or UNGA81"><p id="document-count" role="status" aria-live="polite">31 documents</p></div></section><section class="document-grid" aria-label="Source documents">'
for d in docs:
    search=(d['title']+' '+('property claytons amity title search plan' if 'Clayton' in d['title'] else '')).lower()
    content+=f'<article class="document-card tilt" data-search="{esc(search)}"><span class="format">{d["format"]} · {d["bytes"]/1024:.0f} KB</span><h2>{esc(d["title"])}</h2><a class="button secondary" href="{d["file"]}" download>Download document ↓</a>'
    if d['format']=='PDF': content+=f'<a class="text-link" href="{d["file"]}">Read PDF ↗</a>'
    content+='</article>'
content+='</section><p class="no-results" hidden>No matching documents. Try another word.</p>'
content+='<section class="library-invitation"><h2>Websites and development history</h2><p>Explore all 15 supplied websites, further research references and the decisions that shaped the proposal.</p><a class="button" href="source-history.html">Explore the complete source history ↗</a></section>'
(ROOT/'documents.html').write_text(shell('Document library',content,'documents','library',PAGES[-1],('source-history','Source history')),'utf-8')
history=(ROOT/'content/history.md').read_text('utf-8').strip()
content='<section class="hero">'+image('library',alts['library'],eager=True)+'<span class="hero-caption">GenAI concept artwork</span></section><div class="title-block"><h1>Source history</h1></div><section class="library-intro"><p>The complete source archive and the development of the invitation: 31 documents, 15 supplied websites and the further sources cited in the proposal.</p></section><nav class="section-links" aria-label="On this page"><a href="#how-the-proposal-developed">Development history</a><a href="#all-documents">All 31 documents</a><a href="#supplied-websites">All 15 websites</a><a href="#research-sources">Further cited sources</a></nav>'
history=history.replace('# How the proposal developed','## How the proposal developed',1)
content+='<section class="prose-section"><div class="prose development-history">'+md(history)+'</div></section>'+source_archive()+research_sources()
(ROOT/'source-history.html').write_text(shell('Source history',content,'source-history','library',('documents','Document library'),('other-proposals','Other Minjerribah proposals')),'utf-8')
network='https://auraofintelligence.github.io/multi-site-Minjerribah-network/'
related=[
 ('seven-mile.html','7 Mile living and residency proposal','Living, residencies, visitors, ceremony, gardens, making and retained scrub.','towers'),
 ('ballow-road.html','9 Ballow Road public hub','A proposed Dunwich base for technology help, training, media, meetings and coordination.','learning'),
 ('mens-recovery.html',"Men’s alcohol and drug free camp",'Culture, mentoring, daily rhythm, food, gardens, useful work and support beyond each stay.','fund-v2'),
 ('women-children.html','A safe place for women and children','A proposal to explore with relevant women around location, leadership and everyday support.','invitation-v2'),
 ('housing.html','Housing for different stages of life','Connections between immediate shelter, supported transition, stable homes and ageing in place.','home'),
 ('ageing-longevity.html','Aged care and longevity research','Everyday quality of life, ageing in place, Aura digital twins and future research.','care'),
 ('sand-screen.html','Sand and Screen for all ages','Sand sport, outdoor cinema, local screen work, gathering and practical roles.','contribution')]
content='<section class="hero">'+image('towers',alts['towers'],eager=True)+'<span class="hero-caption">GenAI concept artwork</span></section><div class="title-block"><h1>Other proposals for the Indigenous community</h1></div><section class="library-intro"><p>The wider Minjerribah network brings together proposals for living, culture, recovery, safety, housing, care, learning and useful work. Each opens a conversation about what could serve local people and how they would like to shape it.</p><a class="button" href="'+network+'index.html">Visit the Minjerribah site and service ideas ↗</a></section><section class="related-grid">'
for url,title,summary,art in related:
    content+='<a class="related-card tilt" href="'+network+url+'">'+image(art,alts.get(art,art))+'<div><h2>'+esc(title)+'</h2><p>'+esc(summary)+'</p><span>Explore this proposal ↗</span></div></a>'
content+='</section><section class="prose-section"><div class="prose"><h2>Explore how the ideas connect</h2><p>The network also brings together <a href="'+network+'organisation-builder.html">organisation setup</a>, <a href="'+network+'structure.html">funding and operating approaches</a> and the <a href="'+network+'sources.html">source trail</a>.</p></div></section>'
(ROOT/'other-proposals.html').write_text(shell('Other proposals for the Indigenous community',content,'other-proposals','towers',('documents','Document library'),('index','A gift for generations')),'utf-8')
licence=(ROOT/'LICENCE.md').read_text('utf-8')
content='<section class="licence-page prose">'+md(licence)+'</section>'
(ROOT/'licence.html').write_text(shell('Strange But True Public Source Licence',content,'licence',prev=('documents','Document library'),nxt=('index','A gift for generations')),'utf-8')
(ROOT/'404.html').write_text(shell('Page not found','<section class="prose licence-page"><h1>Let’s find your place</h1><p>This page could not be found.</p><a class="button" href="'+BASE+'">Return to the proposal ↗</a></section>','404'),'utf-8')
(ROOT/'site.webmanifest').write_text(json.dumps({'name':'A gift for generations','short_name':'A gift','start_url':'./','display':'browser','background_color':'#f8f7f0','theme_color':'#073d3d','icons':[{'src':'favicon-192.png','sizes':'192x192','type':'image/png'},{'src':'favicon-512.png','sizes':'512x512','type':'image/png'}]},indent=2),'utf-8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n','utf-8')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+k+'.html</loc></url>' for k in [p[0] for p in PAGES]+['documents','source-history','licence','other-proposals'])+'</urlset>','utf-8')
print('Built 11 proposal pages, document library, source history, related proposals, licence and 404 page.')
