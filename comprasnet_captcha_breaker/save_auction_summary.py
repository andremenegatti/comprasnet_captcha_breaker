def save_auction_summary(html_source: str, output_folder: str, auction_id: str, num_doc=0):
    """ Saves html source of an auction summary in disk
    
    :param html_source: html source of the page to be saved
    :param output_folder: directory where the file will be saved
    :param auction_id: string with the 16-digit auction id
    """
    filename = f'/{auction_id}_ata{str(num_doc).zfill(3)}.html'
    
    with open(output_folder + filename, 'w', encoding = 'utf-8') as html_file:
        html_file.write(html_source)
        print('Done!')