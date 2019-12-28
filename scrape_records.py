import time
import pandas as pd
from glob import glob
from selenium import webdriver
from keras.models import load_model
import comprasnet_captcha_breaker as ccb

OUTPUT_FOLDER = 'atas'
SUPPLEMENTARY_OUTPUT_FOLDER = 'atas_comp'
SCRAPE_SUPPLEMENTARY_RECORDS = True

# Loading models
model_filenames = sorted(glob('models/*.hdf5'))
labels_filenames = sorted(glob('models/labels/*.dat'))

model_list = [*map(load_model, model_filenames)]
labels_list = [*map(ccb.load_labels, labels_filenames)]

# Loading pandas dataframe with auction data
# Dataframe must contain the following columns:
## 1) auction_id: 16 digits (uasg_id + auction_number)
## 2) auction_number: 10 digits
## 3) uasg_id: 6 digits
df_ids = pd.read_csv('coffee_auctions.csv', dtype = str)

# Number of auctions to scrape
total = df_ids.shape[0]
total = 20

# Initializing lists for handling errors
error_control = [1, 2, 3]
critical_error_control = [1, 2, 3, 5]

# Loading log files as instances of LogFile class
# If csv logs does not exist, they will be created in disk
ProgressLog = ccb.LogFile(file='logs/progress.csv', zero_if_empty=True)
SkippedLog = ccb.LogFile(file='logs/skipped.csv')
ServerErrorLog = ccb.LogFile(file='logs/server_error.csv')
MaxAttemptsLog = ccb.LogFile(file='logs/max_attempts.csv')

# Starting index (df_ids row from which to start)
# Last successfully processed index is stored in ProgressLog.last_iteration
# If there wasn't a progress log, last_iteration is set to 0
i = ProgressLog.last_iteration

# Initializing webdriver
browser = webdriver.Chrome("chromedriver")

# Iterating
while i <= total:
    print(f'\n{i+1}/{total}')
    
    # Defining search parameters
    auction_id = df_ids['auction_id'][i]
    uasg_id = df_ids['uasg_id'][i]
    auction_number = df_ids['auction_number'][i]
    print(f'UASG: {uasg_id}   Auction number: {auction_number}')
    
    try:
        # Searching for UASG and auction number
        ccb.search_auction(browser, uasg_id, auction_number)
        html_source = browser.page_source
        
        
        # Looping until CAPTCHA is solved
        html_source = ccb.break_captcha(browser, html_source,
                                        model_list, labels_list,
                                        max_attempts=20)
        
        if html_source == 'max_attempts':
            print('Too many unsuccessfull attempts: skipping...')
            time.sleep(2)
            MaxAttemptsLog.update(i, auction_id)
            SkippedLog.update(i, auction_id)
            # Shut down if there has been more than 5 consecutive errors
            if ccb.check_consec_errors(MaxAttemptsLog.iterations, n=5):
                break
            # Increasing iteration counter (moving on to the next auction)
            i += 1
            continue
        
        # Dealing with potential server error
        if '500 - Internal server error' in html_source[0:300]:
            print('500 - Internal server error')
            time.sleep(10)
            ServerErrorLog.update(i, auction_id)
            SkippedLog.update(i, auction_id)
            # Shut down if there has been more than 5 consecutive errors
            if ccb.check_consec_errors(ServerErrorLog.iterations, n=5):
                break
            # Increasing iteration counter (moving on to the next auction)
            i += 1
            continue
        
        # Saving html file
        ccb.save_auction_summary(html_source, OUTPUT_FOLDER, auction_id)
        time.sleep(1)
        
        # Checking for supplementary records
        n_supp_records = ccb.check_for_supplementary_records(html_source)
        
        if n_supp_records and SCRAPE_SUPPLEMENTARY_RECORDS:
            
            # Iterating over detected supplementary records
            for ata in range(1, int(n_supp_records.group(1)) + 1):
                
                print(f'Ata Complementar n.{ata}')
                ccb.click_see_next_entry(browser)
                
                html_source = browser.page_source
                
                # Looping until CAPTCHA is solved
                html_source = ccb.break_captcha(browser, html_source,
                                                model_list, labels_list,
                                                max_attempts=20)
                
                if html_source == 'max_attempts':
                    print('Too many unsuccessfull attempts: skipping...')
                    time.sleep(2)
                    MaxAttemptsLog.update(i, auction_id)
                    SkippedLog.update(i, auction_id)
                    # Shut down if more than 5 consecutive errors
                    if ccb.check_consec_errors(MaxAttemptsLog.iterations, n=5):
                        break
                    # Increasing counter (moving on to the next auction)
                    i += 1
                    continue
                
                # Dealing with potential server error
                if '500 - Internal server error' in html_source[0:300]:
                    print('500 - Internal server error')
                    ServerErrorLog.update(i, auction_id)
                    SkippedLog.update(i, auction_id)
                    # Shut down if more than 5 consecutive server errors
                    if ccb.check_consec_errors(ServerErrorLog.iterations, n=5):
                        break
                    # Increasing counter (moving on to the next auction)
                    i += 1
                    continue
                
                # Saving html file
                ccb.save_auction_summary(html_source, OUTPUT_FOLDER,
                                         auction_id, num_doc=ata)
                time.sleep(1)
        
        # Updating log and moving on to next auction
        ProgressLog.update(i, auction_id)
        i += 1
        time.sleep(1)
        
    except:
        print('Error!')
        error_control.append(i)
        time.sleep(1)
        
        # Try again if there has been less than 3 consecutive errors
        if not(ccb.check_consec_errors(error_control, n=3)):
            continue
        
        # Otherwise: critical error
        else:
            print('Critical error! Restarting webdriver...')
            browser.close()
            browser = webdriver.Chrome('chromedriver')
            
            # Updating critical error list
            critical_error_control.append(i)
            
            # Retry if there has been less than 3 consecutive critical errors
            if not(ccb.check_consec_errors(critical_error_control, n=3)):
                error_control.append(0) ; error_control.append(0)
                continue
            
            # Skip auction if there has been 3 consecutive errors
            else:
                SkippedLog.update(i, auction_id)
                ProgressLog.update(i, auction_id)
                
                # Increasing iteration counter
                i += 1
                
                # Break if 3 consecutive auctions have been skipped
                if ccb.check_consec_errors(SkippedLog.iterations, n=3):
                    break
                else:
                    continue

# Updating logs
ProgressLog.update(i, auction_id)
SkippedLog.update(i, auction_id)
ServerErrorLog.update(i, auction_id)

# Shutting down webdriver
browser.close()
