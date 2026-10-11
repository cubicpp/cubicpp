"""Refresh decorative capsule SVGs; no personal token required."""
from pathlib import Path
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

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
    destination = ROOT / 'assets' / name
    temporary = destination.with_suffix('.tmp')
    temporary.write_bytes(raw)
    temporary.replace(destination)

def main():
    for theme in ('dark', 'light'):
        endpoints = {
            'capsule-header': ('https://capsule-render.vercel.app/api', {'type': 'waving', 'height': '120', 'section': 'header', 'color': 'gradient', 'animation': 'twinkling'}),
            'capsule-footer': ('https://capsule-render.vercel.app/api', {'type': 'waving', 'height': '100', 'section': 'footer', 'color': 'gradient', 'animation': 'twinkling'}),
        }
        for name, (base, params) in endpoints.items():
            save_svg(f'{name}-{theme}.svg', request(base + '?' + urllib.parse.urlencode(params)))
            print('Updated ' + name + '-' + theme)
    print('Updated decorative capsule SVGs')

if __name__ == '__main__':
    main()
