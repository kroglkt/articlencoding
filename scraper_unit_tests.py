import SeleniumScraper

def berlingske_multiple_authors():
    url = 'https://www.berlingske.dk/kultur/anne-sophia-hermansen-det-skal-du-laese-i-sommerferien'
    h,b,a = SeleniumScraper.get_content(url)
    
    assert a == ['Mathias Ørsborg Johansen', 'Marie Louise Poulsen'], a
    assert h == 'Anne Sophia Hermansen: Det skal du læse i sommerferien', h

def berlingske_single_author_mail():
    url = 'https://www.berlingske.dk/aok/en-af-meningsdannelsens-grand-old-ladies-fylder-rundt-anne-sophia-hermansen'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == "Anne Sophia Hermansen", a
    assert h == 'En af meningsdannelsens grand old ladies fylder rundt - Anne Sophia Hermansen portrætterer Sørine Gotfredsen', h


def berlingske_single_author():
    url = 'https://www.berlingske.dk/kulturkommentar/ash-da-jeg-saa-manu-sareen-loebe-ind-paa-scenen-i-aaben-skjorte-og'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == 'Anne Sophia Hermansen', a
    assert h == 'ASH: Da jeg så Manu Sareen løbe ind på scenen i åben skjorte og jamre »Juliøøøøeeee!«, var jeg nødt til at slukke', h

def eb_multiple_authors():
    url = 'https://ekstrabladet.dk/roskilde/nyheder/fraek-brydekamp-glitter-bare-babser-og-noegne-numser/7696270'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == ['Nanna Bay Madsen', 'Maya Stoltze Westander'], a
    assert h == 'Fræk brydekamp: Glitter, bare babser og nøgne numser', h

def eb_single_author():
    url = 'https://ekstrabladet.dk/musik/intlalbum/hvor-hashtaagerne-aldrig-letter/4789353'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == 'Thomas Treo', a
    assert h == 'Hvor hashtågerne aldrig letter', h

def eb_bad_authors():
    url = 'https://ekstrabladet.dk/underholdning/anmeldelser/article3088052.ece'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == 'Thomas Treo', a
    assert h == 'U2 slår til igen', h

def berlingske_404():
    url = 'https://www.berlingske.dk/kultur/anne-sophia-hermansen-naar-adele-retraumatiserer'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == '404', a
    assert h == '404', h
    assert b =='404', b

def eb_404():
    url = 'https://ekstrabladet.dk/smormu'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == '404', a
    assert h == '404', h
    assert b =='404', b

def bt_single_author():
    url = 'https://www.bt.dk/krimi/brand-udvikler-kraftig-roeg-paa-noerrebrogade-i-koebenhavn'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == 'Kicki Søs Bengtsen', a
    assert h == 'Brand udvikler kraftig røg på Nørrebrogade i København', h
    assert len(b) == 1492, len(b)

def bt_multiple_authors():
    url = 'https://www.bt.dk/motion/se-traeningen-du-skal-lave-hvis-du-er-loeber'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == ['JO BRAND ', ' CHRISTINA BØLLING'], a
    assert h == 'Se træningen du skal lave, hvis du er løber', h
    assert len(b) == 3459, len(b)

def bt_404():
    url = 'https://www.bt.dk/egu'
    h,b,a = SeleniumScraper.get_content(url)

    assert a == '404', a
    assert h == '404', h
    assert b == '404', b



for i in range(3):
    berlingske_multiple_authors()
    berlingske_single_author_mail()
    berlingske_single_author()
    berlingske_404()
    print("Passed Berlingske")

    eb_multiple_authors()
    eb_single_author()
    eb_bad_authors()
    eb_404()
    print("Passed BT")

    bt_single_author()
    bt_multiple_authors()
    bt_404()
    print("Passed BT")

print("Tests passed")
