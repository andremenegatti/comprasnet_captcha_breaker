import time
import pandas as pd
from glob import glob
from selenium import webdriver
from keras.models import load_model
import comprasnet_captcha_breaker as ccb

OUTPUT_FOLDER = 'atas'
SUPPLEMENTARY_OUTPUT_FOLDER = 'atas_comp'

# Loading models
model_filenames = sorted(glob('models/*.hdf5'))
labels_filenames = sorted(glob('models/labels/*.dat'))

model_list = [*map(load_model, model_filenames)]
labels_list = [*map(ccb.load_labels, labels_filenames)]

# Loading pandas dataframe with auction data
df_ids = pd.read_csv('todos_pregoes_exceto_cafe.csv', dtype = str)

# Number of auctions to scrape
#total = df_ids.shape[0]
total = 20
i = 1

error_control = [1, 2, 3]
critical_error_control = [1, 2, 3, 5]

# Reading log files
#i = ccb.read_log_file('logs/last_iteration.txt')[0]
skipped_index = ccb.read_log_file('logs/skipped_index.txt')
skipped = ccb.read_log_file('logs/skipped_history.txt')
server_error_index = ccb.read_log_file('logs/server_error_index.txt')
server_error = ccb.read_log_file('logs/server_error_history.txt')

# Initializing webdriver
browser = webdriver.Chrome("chromedriver")

# Iterating
while i <= total:
    print(f'\n{i+1}/{total}')
    # Defining search parameters
    auction_id = df_ids['id_pregao'][i]
    co_uasg = df_ids['co_uasg'][i]
    num_preg = df_ids['num_preg'][i]
    print(f'UASG: {co_uasg}   Auction number: {num_preg}')
    
    try:
        # Searching for UASG and auction number
        browser = webdriver.Chrome("chromedriver")
        ccb.search_auction(browser, co_uasg, num_preg)
        html_source = browser.page_source
        
        # Looping until CAPTCHA is solved
        html_source = ccb.break_captcha(browser, html_source,
                                        model_list, labels_list)
        
        # Dealing with potential server error
        if '500 - Internal server error' in html_source[0:300]:
            print('500 - Internal server error')
            time.sleep(10)
            server_error.append(auction_id)
            server_error_index.append(i)
            skipped.append(auction_id)
            skipped_index.append(i)
            ccb.save_log(skipped_index, 'logs/skipped_index.txt')
            ccb.save_log(skipped, 'logs/skipped_history.txt')
            ccb.save_log(server_error, 'logs/server_error_history.txt')
            ccb.save_log(server_error_index, 'logs/server_error_index.txt')
            # Shut down if there has been more than 5 consecutive server errors
            if len(server_error) > 5:
                if server_error_index[-1] == (server_error_index[-5] + 4):
                    break
            # Increasing iteration counter (moving on to the next auction)
            i += 1
            continue
        
        # Saving html file
        ccb.save_auction_summary(html_source, OUTPUT_FOLDER, auction_id)
        time.sleep(1)
        
        # Checking for supplementary summaries
        num_ata_complem = ccb.check_for_supplementary_summary(html_source)
        
        if num_ata_complem:
            
            for ata in range(1, int(num_ata_complem.group(1)) + 1):
                
                print(f'Ata Complementar n.{ata}')
                ccb.click_see_following_summary(browser)
                
                html_source = browser.page_source
                
                # Looping until CAPTCHA is solved
                html_source = ccb.break_captcha(browser, html_source,
                                                model_list, labels_list)
                
                # Dealing with potential server error
                if '500 - Internal server error' in html_source[0:300]:
                    print('500 - Internal server error')
                    time.sleep(10)
                    server_error.append(auction_id)
                    server_error_index.append(i)
                    skipped.append(auction_id)
                    skipped_index.append(i)
                    ccb.save_log(skipped_index, 'logs/skipped_index.txt')
                    ccb.save_log(skipped, 'logs/skipped_history.txt')
                    ccb.save_log(server_error, 'logs/server_error_history.txt')
                    ccb.save_log(server_error_index,
                                 'logs/server_error_index.txt')
                    # Shut down if more than 5 consecutive server errors
                    if len(server_error) > 5:
                        if server_error_index[-1] == \
                        (server_error_index[-5] + 4):
                            break
                    # Increasing counter (moving on to the next auction)
                    i += 1
                    continue
                
                # Saving html file
                ccb.save_auction_summary(html_source, OUTPUT_FOLDER,
                                         auction_id, num_doc=ata)
                time.sleep(1)
        
        # Moving on to next auction
        ccb.save_log(i, 'logs/last_iteration.txt')
        
        i += 1
        time.sleep(1)
        
    except:
        print('Error!')
        error_control.append(i)
        time.sleep(1)
        
        # Try again if there has been less than 3 consecutive errors
        if error_control[-3] != error_control[-1]:
            continue
        
        # Otherwise: critical error
        else:
            print('Critical error! Restarting webdriver...')
            browser.close()
            browser = webdriver.Chrome('chromedriver')
            
            # Updating critical error list
            critical_error_control.append(i)
            
            # Retry if there has been less than 3 consecutive critical errors
            three_consecutive_critical_errors = \
            critical_error_control[-3] == critical_error_control[-2] \
            == (critical_error_control[-1])
            
            if not(three_consecutive_critical_errors):
                error_control.append(0)
                error_control.append(0)
                continue
            
            # Skip auction if there has been 3 consecutive errors
            else:
                skipped_index.append(i)
                skipped.append(auction_id)
                
                # Saving logs
                try:
                    ccb.save_log(i, 'logs/last_iteration.txt')
                    ccb.save_log(skipped_index, 'logs/skipped_index.txt')
                    ccb.save_log(skipped, 'logs/skipped_history.txt')
                except:
                    print('An error occurred while saving error log files...')
                
                # Increasing iteration counter
                i += 1
                
                # Break if 3 consecutive auctions have been skipped
                three_consecutive_skipped = \
                (skipped_index[-3] + 2) == (skipped_index[-2] + 1) \
                == skipped_index[-1]
                
                if three_consecutive_skipped:
                    break
                else:
                    continue

# Updating logs
ccb.save_log(i, 'logs/last_iteration.txt')
ccb.save_log(skipped_index, 'logs/skipped_index.txt')
ccb.save_log(skipped, 'logs/skipped_history.txt')
ccb.save_log(server_error, 'logs/server_error_history.txt')
ccb.save_log(server_error_index, 'logs/server_error_index.txt')

# Shutting down webdriver
browser.close()
