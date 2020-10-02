import maindex

delay = 12

maindex.delay = delay
url_list = maindex.main()

for entry in url_list:
    maindex.starting_url = entry
    maindex.delay = delay
    tempo_links = maindex.main()
