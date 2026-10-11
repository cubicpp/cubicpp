"""Refresh profile SVGs using public GitHub data; no personal token required."""
from pathlib import Path
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
USER = 'cubicpp'
COLORS = {
    'dark': {'bg': '00000000', 'text': 'c9d1d9', 'accent': '58a6ff', 'ink': 'c9d1d9', 'grid': '30363d'},
    'light': {'bg': '00000000', 'text': '434d58', 'accent': '2f80ed', 'ink': '434d58', 'grid': 'd1d9e0'},
}

def request(url):
    headers = {'User-Agent': 'cubicpp-profile', 'Accept': '*/*'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read()

def save_svg(name, raw):
    root = ET.fromstring(raw)
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Invalid SVG response: ' + name)
    for node in root.iter():
        if node.tag.rsplit('}', 1)[-1] in ('script', 'foreignObject'):
            raise ValueError('Unsafe SVG response: ' + name)
        if any(key.lower().startswith('on') for key in node.attrib):
            raise ValueError('Unsafe SVG attribute: ' + name)
        if any(key.rsplit('}', 1)[-1] == 'href' and not value.startswith('#') for key, value in node.attrib.items()):
            raise ValueError('External SVG reference: ' + name)
    text = raw.decode('utf-8')
    if any(message in text.lower() for message in ('something went wrong', 'deployment_disabled', 'could not fetch', 'rate limit exceeded')):
        raise ValueError('Data service returned an error: ' + name)
    # Data labels must be immediately readable, including reduced-motion views.
    if name.startswith(('stats-', 'languages-', 'streak-')):
        override = '<style>*{animation:none!important;animation-delay:0s!important}.header,.stagger,text[style],g[style],circle[style]{opacity:1!important}</style>'
        text = text.replace('</svg>', override + '</svg>')
        if name.startswith('languages-'):
            text = text.replace('height="165"', 'height="195"').replace('viewBox="0 0 467 165"', 'viewBox="0 0 467 195"')
            text = text.replace('transform="translate(0, 55)"', 'transform="translate(0, 70)"')
        raw = text.encode('utf-8')
    destination = ROOT / 'assets' / name
    temporary = destination.with_suffix('.tmp')
    temporary.write_bytes(raw)
    temporary.replace(destination)

def main():
    for theme, c in COLORS.items():
        common = {'hide_border': 'true', 'bg_color': c['bg'], 'theme': 'github_dark' if theme == 'dark' else 'default', 'disable_animations': 'true'}
        endpoints = {
            'stats': ('https://github-readme-stats.vercel.app/api', {**common, 'username': USER, 'show_icons': 'true', 'hide_rank': 'true', 'card_width': '467'}),
            'languages': ('https://github-readme-stats.vercel.app/api/top-langs/', {**common, 'username': USER, 'layout': 'compact', 'card_width': '467', 'langs_count': '6'}),
            'streak': ('https://streak-stats.demolab.com/', {'user': USER, 'hide_border': 'true', 'background': c['bg'], 'ring': c['accent'], 'fire': c['accent'], 'currStreakLabel': c['accent'], 'sideLabels': c['text'], 'currStreakNum': c['ink'], 'sideNums': c['ink'], 'dates': c['text'], 'stroke': c['grid'], 'border_radius': '12'}),
            'trophies': ('https://trophy.ryglcloud.net/', {'username': USER, 'theme': 'tokyonight' if theme == 'dark' else 'flat', 'no-frame': 'true', 'no-bg': 'true', 'column': '6', 'margin-w': '12', 'margin-h': '12'}),
            'capsule-header': ('https://capsule-render.vercel.app/api', {'type': 'waving', 'height': '120', 'section': 'header', 'color': 'gradient', 'animation': 'twinkling'}),
            'capsule-footer': ('https://capsule-render.vercel.app/api', {'type': 'waving', 'height': '100', 'section': 'footer', 'color': 'gradient', 'animation': 'twinkling'}),
        }
        for name, (base, params) in endpoints.items():
            save_svg(f'{name}-{theme}.svg', request(base + '?' + urllib.parse.urlencode(params)))
            print('Updated ' + name + '-' + theme)
    print('Updated standard GitHub data cards')

if __name__ == '__main__':
    main()
