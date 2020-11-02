# comprasnet_captcha_breaker

This python module allows the user to automate the process of downloading multiple auction reports from Comprasnet. The solution relies on using Convolutional Neural Networks to solve CAPTCHAs and ``selenium`` to interact with the web browser. The user must provide a list containing the 16-digit codes identifying the auctions of interest.

## Comprasnet and public procurement data in Brazil

In Brazil, Federal-level public procurements for ordinary goods and services must take place as online auctions. One of the most used platforms for such procurement auctions is [Comprasnet](https://comprasgovernamentais.gov.br/index.php/comprasnet-siasg).

There is an useful [API](http://compras.dados.gov.br/docs/home.html) for accessing data regarding procurement auctions, such as relevant dates, winning bids, and data regarding purchased goods and services, including detailed description and quantities.

Nevertheless, many other important information cannot be accessed via the API, and are available only in the procurement records (_atas_). Such information include the complete list of bids, with value, bidder and timestamps, detailed information about the auction phases and events, as well as all communication between bidders and the procurement official (_pregoeiro_).

The procurement records are available online as html pages on a different [address](http://comprasnet.gov.br/acesso.asp?url=/livre/pregao/ata0.asp), outside the API. If one wants to access information regarding a procurement auction, she must type in the search parameteres, navigate through several pages and, more importantly, solve a CAPTCHA. The process must be entirely repeated for every procurement auction.

This is not aligned with the principles of government transparency and makes it harder to analyze data from multiple procurement auctions.

## Types of captchas

After the user types in the search parameters and navigates through some pages, she must solve one five different types of captchas appear alternately in the webpage preceding a procurement report. These are:

bubble         | bubble_cut    | dotted         | dotted_wave  | wave          |
:-------------:|:-------------:|:-------------:|:-------------:|:-------------:
![alt text](https://github.com/andremenegatti/comprasnet_captcha_models/blob/master/captchas/test/bubble/1Q4CwZ_564.png "bubble captcha") | ![alt text](https://github.com/andremenegatti/comprasnet_captcha_models/blob/master/captchas/test/bubble_cut/14VXad_731.png "bubble_cut captcha") |![alt text](https://github.com/andremenegatti/comprasnet_captcha_models/blob/master/captchas/test/dotted/bTw31n_699.png "dotted captcha") | ![alt text](https://github.com/andremenegatti/comprasnet_captcha_models/blob/master/captchas/test/dotted_wave/Captcha000002.png "dotted_wave captcha") | ![alt text](https://github.com/andremenegatti/comprasnet_captcha_models/blob/master/captchas/test/wave/16CWaQ_701.png "wave captcha")

## Convolutional Neural Networks (CNNs)
### Character Recognition
The package includes 4 trained CNNs designed to predict characters from a specific captcha type. As of now, _dotted_wave_ captchas are not supported.

### Captcha classification
In addition to the models that perform character recognition, the repository also contains a CNN to classify captchas according to the 5 types listed above.

The idea is to use this model to predict a captcha's type, which allows the selection of the suitable character recognition CNN.

## Character segmentation
Since the models are trained to predict individual characters, character segmentation must be performed beforehand. Thus, the repository also includes python modules and functions with simple algorithms for isolating the characters in captcha images.

The algorithms are specific to each captcha-type (with the exception of _bubble_ and _bubble_cut_, which are handled by a single algorithm/function).

Currently there is no algorithm for splitting _dotted_wave_ captchas, and this is the reason why there is no model for this captcha class. Help in this regard would be much appreciated.

## Web scraping
The package relies on selenium and [Chromedriver](https://chromedriver.chromium.org/downloads) to interact with the pages, type in search parameters, break the captchas and save html sources.

## Reading captchas from browser into python session
It is not possible to save image directly from its URL. Each time the URL is accessed, a new captcha is generated. Thus, if opens the browser, gets to the captcha page and then uses the image URL to store it in disk or load into the python session, the retrieved image will not match the one that must be solved.

In order to circumvent this, we use selenium to simulate a right click on the captcha image, open the context menu, and then simulate keystrokes to select the option that copies it to the clipboard. Once in clipboard, the image can be easily loaded into the python session.

The main disavantage of this approach is that computer cannot be used while web scraping, since the simulated keystrokes are processed in the open window. A solution to this is running the program on a virtual machine.

Finally, in Linux systems the keystrokes are simulated with the `xte` command, from `xautomation`.
