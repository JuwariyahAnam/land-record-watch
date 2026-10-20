"""Translate a finished registry page into Kannada or Hindi.

The visible text of the page is matched against translations.py. Text with no match stays English,
so a missing line never breaks anything. Scripts, styles, form values and the public watch page are never touched."""
import re

from bs4 import BeautifulSoup, NavigableString

from .translations import PATTERNS, TEXT

LANGS = ("en", "kn", "hi")
_SKIP_PARENTS = {"script", "style", "textarea", "pre", "code"}
_COMPILED = [(re.compile(p), t) for p, t in PATTERNS]


def _norm(s):
    return " ".join(s.split())


def translate_text(text, lang, _depth=0):
    """Return the translation of a piece of text, or None if there is none."""
    key = _norm(text)
    if not key or lang not in ("kn", "hi"):
        return None
    hit = TEXT.get(key)
    if hit:
        return hit[lang]
    if _depth > 1:
        return None
    for rx, tpl in _COMPILED:
        m = rx.fullmatch(key)
        if m:
            parts = {str(i): (translate_text(g, lang, _depth + 1) or g) if g else "" for i, g in enumerate(m.groups(), 1)}
            out = tpl[lang]
            for k, v in parts.items():
                out = out.replace("{" + k + "}", v)
            return out
    return None


def translate_html(html, lang):
    if lang not in ("kn", "hi"):
        return html
    soup = BeautifulSoup(html, "html.parser")
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or node.parent is None or node.parent.name in _SKIP_PARENTS:
            continue
        if type(node).__name__ in ("Comment", "Doctype", "Declaration"):
            continue
        new = translate_text(str(node), lang)
        if new:
            lead = str(node)[: len(str(node)) - len(str(node).lstrip())]
            tail = str(node)[len(str(node).rstrip()):]
            node.replace_with(lead + new + tail)
    for tag in soup.find_all(["input", "textarea"]):
        ph = tag.get("placeholder")
        if ph:
            new = translate_text(ph, lang)
            if new:
                tag["placeholder"] = new
    html_tag = soup.find("html")
    if html_tag is not None:
        html_tag["lang"] = lang
    return str(soup)
