import requests
from bs4 import BeautifulSoup
from db import *
from models import Website

Base.metadata.create_all(engine)


def main():
    session = Session()
    start_url = "https://register.start.bg"
    queue = [start_url]
    visited = [start_url]

    while len(queue):
        current_url = queue.pop(0)
        re = requests.get(current_url, timeout=10)
        server = re.headers['Server']

        website = Website(url=current_url, server=server)
        result = session.query(Website).filter(Website.url == current_url).first()
        if result is None:
            session.add(website)
            session.commit()

        try:
            doc_html = re.content.decode('utf-8')
        except UnicodeDecodeError:
            pass

        soup = BeautifulSoup(doc_html, 'html.parser')


        for link in soup.find_all('a'):
            site = str(link.get('href'))
            if site.startswith("http") or site.startswith("https"):
                if site is not None and not site.startswith('#'):
                    if '.bg' in site and site not in visited:
                        print(f'                   ')
                        print(site)
                        queue.append(site)
                        visited.append(site)

if __name__ == '__main__':
    main()