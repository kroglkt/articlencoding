import SeleniumScraper

def berlingske_multiple_authors():
    url = 'https://www.berlingske.dk/kultur/anne-sophia-hermansen-det-skal-du-laese-i-sommerferien'
    h,b,a = SeleniumScraper.get_content(url)
    
    assert len(a) == 2, len(a)
    assert a == ['Mathias Ørsborg Johansen', 'Marie Louise Poulsen'], a
    assert h == 'Anne Sophia Hermansen: Det skal du læse i sommerferien', h

def berlingske_single_author_mail():
    url = 'https://www.berlingske.dk/aok/en-af-meningsdannelsens-grand-old-ladies-fylder-rundt-anne-sophia-hermansen'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, type(a)
    assert a == "Anne Sophia Hermansen", a
    assert h == 'En af meningsdannelsens grand old ladies fylder rundt - Anne Sophia Hermansen portrætterer Sørine Gotfredsen', h


def berlingske_single_author():
    url = 'https://www.berlingske.dk/kulturkommentar/ash-da-jeg-saa-manu-sareen-loebe-ind-paa-scenen-i-aaben-skjorte-og'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, type(a)
    assert a == 'Anne Sophia Hermansen', a
    assert h == 'ASH: Da jeg så Manu Sareen løbe ind på scenen i åben skjorte og jamre »Juliøøøøeeee!«, var jeg nødt til at slukke', h

def eb_multiple_authors():
    url = 'https://ekstrabladet.dk/roskilde/nyheder/fraek-brydekamp-glitter-bare-babser-og-noegne-numser/7696270'
    h,b,a = SeleniumScraper.get_content(url)

    assert len(a) == 2, len(a)
    assert a == ['Nanna Bay Madsen', 'Maya Stoltze Westander'], a
    assert h == 'Fræk brydekamp: Glitter, bare babser og nøgne numser', h

def eb_single_author():
    url = 'https://ekstrabladet.dk/musik/intlalbum/hvor-hashtaagerne-aldrig-letter/4789353'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, a
    assert a == 'Thomas Treo', a
    assert h == 'Hvor hashtågerne aldrig letter', h

def eb_bad_authors():
    url = 'https://ekstrabladet.dk/underholdning/anmeldelser/article3088052.ece'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, a
    assert a == 'Thomas Treo', a
    assert h == 'U2 slår til igen', h

def berlingske_404():
    url = 'https://www.berlingske.dk/kultur/anne-sophia-hermansen-naar-adele-retraumatiserer'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, a
    assert a == '404', a
    assert h == '404', h
    assert b =='404', b

def eb_404():
    url = 'https://ekstrabladet.dk/smormu'
    h,b,a = SeleniumScraper.get_content(url)

    assert type(a) == str, a
    assert a == '404', a
    assert h == '404', h
    assert b =='404', b



berlingske_multiple_authors()
berlingske_single_author_mail()
berlingske_single_author()
eb_multiple_authors()
eb_single_author()
eb_bad_authors()
berlingske_404()
eb_404()

print("Tests passed")
