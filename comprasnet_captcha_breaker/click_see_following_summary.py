def click_see_next_summary(browser):
    """ Clicks on the button to access the next summary of the an auction
    
    :param browser: a Selenium webdriver instance
    
    """
    xpath = \
    "//body/table[2]/tbody[1]/tr[1]/td[2]/*[contains(text(), 'Ver Ata Posterior')]"
    
    browser.find_elements_by_xpath(xpath)[0].click()