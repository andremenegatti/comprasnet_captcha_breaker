import re

def check_for_supplementary_records(html_source: str):
    """Check if a given auction has supplementary records
    
    :param html_source: html source of main procurement records
    :return: a match object or None
    """
    xpath = '<td align="left"> Este pregão possui (\d)+.*Ata(s)? Complementar(es)?</td>'
    
    num_ata_complem = re.search(xpath, html_source)
    
    return(num_ata_complem)