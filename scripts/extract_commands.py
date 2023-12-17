"A low-fi but currently useful way to extract Commands from the audacity HTML documentation."

from pathlib import Path
import sys
import bs4

TEMPLATE = '''
@register_command
class {command_name}(Command):
    """{doc}
    """
    # {args}
    pass

'''

soup = bs4.BeautifulSoup(Path(sys.argv[1]).read_text())
for table in soup.find_all('table')[1:]:
    for row in table.find_all('tr')[1:]:
        command_name = row.find_all('td')[0].find('b').text[:-1]
        args = row.find_all('td')[2].text
        doc = row.find_all('td')[3].text
        print(TEMPLATE.format(command_name=command_name, doc=doc.strip(), args=args))
