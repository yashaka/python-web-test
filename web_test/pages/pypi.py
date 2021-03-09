from selene.support.shared import browser

url = 'https://pypi.org/'

search = browser.element('#search')
results = browser.all('.package-snippet')