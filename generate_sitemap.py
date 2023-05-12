from datetime import date

p_codes = {
    "Agile" : "A",
    "Cosy" : "C",
    "Flux" : "F",
    "Go" : "G",
    "Tracker" : "T",
    "Intelligent" : "I"
}

r_codes = {
    "East England": 'A',
    "East Midlands": 'B',
    "London": 'C',
    "Merseyside and North Wales": 'D',
    "West Midlands": 'E',
    "North-East England": 'F',
    "North-West England": 'G',
    "South England": 'H',
    "South-East England": 'J',
    "South Wales": 'K',
    "South-West England": 'L',
    "Yorkshire": 'M',
    "South Scotland": 'N',
    "North Scotland": 'P'
}

def generate_map():
    urls = ""

    for x in p_codes.keys():
        for y in r_codes.values():
            urls+=(f'''
  <url>
    <loc>https://smartenergydashboard.co.uk/{y}/{x}</loc>
    <lastmod>{date.today().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>always</changefreq>
    <priority>0.9</priority>
  </url>''')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://smartenergydashboard.co.uk/</loc>
    <lastmod>{date.today().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>1.0</priority>
  </url>''' + \
    urls + \
    '''
</urlset>
'''

f = open("static/sitemap.xml", 'w')
f.write(generate_map())
f.close()
