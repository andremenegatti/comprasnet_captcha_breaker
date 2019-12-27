def search_auction(browser, co_uasg, num_preg):
    """ Insert search parameters and navigates to CAPTCHA page
    
    :param browser: a Selenium webdriver instance
    :param co_uasg: a 6-digit search parameter
    :param num_preg: a 10-digit search parameter
    """
    browser.get('http://comprasnet.gov.br/livre/pregao/ata0.asp')
    browser.find_element_by_id(id_ = 'co_uasg').send_keys(co_uasg)
    browser.find_element_by_id(id_ = 'numprp').send_keys(int(num_preg))
    browser.find_element_by_name(name = 'ok').click()
    browser.find_element_by_xpath(
            '/html/body/table[1]/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[1]/a').click()
    browser.find_element_by_xpath('/html/body/table[1]/tbody/tr[5]/td[2]/a').click()