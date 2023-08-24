from bs4 import BeautifulSoup
from bs4.element import Comment

def text_from_html(body):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def cutoff(items, eval, limit):
    token_usage  = 0
    results = []
    for item in items:
        cost = eval(item)
        if token_usage + cost > limit :
            break
        token_usage += cost
        results.append(item)
    return results