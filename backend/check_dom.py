import bs4

html = open('adilet_test.html', encoding='utf-8').read()
soup = bs4.BeautifulSoup(html, 'lxml')

forms = soup.find_all('form')
for form in forms:
    print("Form action:", form.get('action'))
    for inp in form.find_all('input'):
        print(f"  Input name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")

