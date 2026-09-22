from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.copy=[]; self.links=[]; self.ids=[]; self.images=[]; self.h1=0; self.main=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='img':self.images.append(a)
        for attr in ['href','src']:
            if attr in a:self.links.append(a[attr])
        if 'srcset' in a:self.links.extend(x.strip().split()[0] for x in a['srcset'].split(','))
        active=('data-proposal' in a) or bool(self.stack and self.stack[-1][1])
        if tag not in ['img','meta','link','input','br','hr']: self.stack.append((tag,active))
        if active and tag in ['h1','h2','h3','p','td','th']:self.copy.append(' ')
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                if self.stack[i][1] and tag in ['h1','h2','h3','p','td','th']:self.copy.append(' ')
                del self.stack[i:];break
    def handle_data(self,data):
        if self.stack and self.stack[-1][1]: self.copy.append(data)

pages={p.name:Page() for p in ROOT.glob('*.html')}
for name,parsed in pages.items():parsed.feed((ROOT/name).read_text('utf-8'))
errors=[]
for name,p in pages.items():
    if p.h1!=1:errors.append(f'{name}: expected one h1, got {p.h1}')
    if p.main!=1:errors.append(f'{name}: expected main')
    if len(p.ids)!=len(set(p.ids)):errors.append(f'{name}: duplicate IDs')
    for im in p.images:
        if 'alt' not in im:errors.append(f'{name}: missing alt')
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=unquote(u.path) or name
        if not (ROOT/target).exists():errors.append(f'{name}: missing {target}')
        if u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{name}: broken anchor {link}')

slugs=['index','invitation','vision','community','aura-geode','aura-genesis','dementia-care','c-hours','learning','shared-horizon','references']
source=(ROOT/'content/proposal.md').read_text('utf-8').strip().split('---PAGE---')
def norm(s):return re.sub(r'\s+',' ',s).strip()
def plain(s):
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s]+?)\)',r'\1',s)
    s=re.sub(r'^\|[-| ]+\|\s*$', '',s,flags=re.M)
    s=re.sub(r'^#+\s*','',s,flags=re.M).replace('**','').replace('|',' ')
    return norm(s)
for key,s in zip(slugs,source):
    expected=plain(s);actual=norm(''.join(pages[key+'.html'].copy))
    if expected!=actual:
        first=next((i for i,(a,b) in enumerate(zip(expected,actual)) if a!=b),min(len(expected),len(actual)))
        errors.append(f'{key}: wording mismatch at {first}: {expected[first:first+90]!r} / {actual[first:first+90]!r}')
docs=json.loads((ROOT/'content/documents.json').read_text('utf-8'))
reference_links=pages['references.html'].links
for d in docs:
    if d['id'] in [31,17,8,26,7,28,27,29,30,18,24,25]:
        if not any(urlsplit(link).path.endswith('/'+d['file']) for link in reference_links):
            errors.append(f'Unlinked named reference document: {d["title"]}')
for d in docs:
    if hashlib.sha256((ROOT/d['file']).read_bytes()).hexdigest()!=d['sha256']:errors.append(f'Changed original: {d["file"]}')
assert len(docs)==31
assert not errors,'\n'.join(errors)
print(f'PASS: {len(pages)} HTML pages, 11 word-for-word proposal sections, 31 original document hashes, local links, anchors and images.')
