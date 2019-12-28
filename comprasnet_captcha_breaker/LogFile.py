import pandas as pd
import os


class LogFile():
    """
    Class for keeping web scraping logs and saving them to disk.
    
    """
    
    def __init__(self, file: str,
                 create_if_not_found=True,
                 zero_if_empty=False):
        """
        :param file: path of csv file
        
        :param create_if_not_found: if True, creates file it is not found
        
        :param zero_if_empty: sets self.last_iteration and self.last_auction
        to 0 if file does not exist of does not contain data
        
        
        :attr path: path of a csv file for writting logs in disk
        
        :attr data: pandas.DataFrame with two columns: 'iteration' and 'auction_id'
        
        :attr last_iteration: last entry from self.data.iteration; if self.data is
        empty, self.last_iteration is set to None, unless zero_if_empty=True,
        case in which self.last_iteration is set to 0.
        
        :attr last_auction: last entry from self.data.auctions_id; if self.data is
        empty, self.last_auction is set to None, unless zero_if_empty=True,
        case in which self.last_auction is set to 0.
        
        :attr iterations: numpy.array with values from self.data.iteration
        
        :attr auctions: numpy.array with values from self.data.auctions_id
        
        """
        if file[-4:] != '.csv':
            raise ValueError('file must be the path of a .csv file')
        
        if not(os.path.exists(file)) and create_if_not_found:
            
            with open(file, 'w+') as f:
                f.write('iteration,auction_id\n')
    
        self.path = file

        self.data = pd.read_csv(file, dtype = {'iteration': int,
                                               'auction_id': str})
        
        if self.data.empty:
            
            if zero_if_empty:
                self.last_iteration = 0
                self.last_auction = '0' * 16
            else:
                self.last_auction = None
                self.last_iteration = None
                
        else:
            self.last_iteration = self.data.iteration.values[-1]
            self.last_auction = self.data.auction_id.values[-1]
    
        self.last_update = None
        self.iterations = self.data.iteration.values
        self.auctions = self.data.auction_id.values

    def update(self, iteration: int, auction_id: str, write=True):
        """ Appends a new row in self.data with the provided arguments,
        and updates attributes accordingly. By default, it also updates
        the csv file in disk.
        
        :param iteration: (int) iteration counter
        :param auction id: (str) 16-digit string
        :param write: (bool) if True, updates csv file indicated in self.file
        """
        self.last_update = pd.DataFrame([[iteration, auction_id]],
                                        columns=['iteration', 'auction_id'])
        
        self.data = pd.concat([self.data, self.last_update])
        self.last_iteration = self.data.iteration.values[-1]
        self.last_auction = self.data.auction_id.values[-1]
        self.iterations = self.data.iteration.values
        self.auctions = self.data.auction_id.values
    
        if write:
            self.data.to_csv(self.path, index=False)