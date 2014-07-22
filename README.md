BitLendingClub Data Extractor
=============================

Login to a BitLendingClub account and extract key financial data for reporting.

See [first working demo](http://youtu.be/1ObVUZWKNQw).

^ above video of first cut of this, script is now fully functional in outputting a CSV of your BLC investments.

See an example of the output it currently generates [here](https://docs.google.com/spreadsheets/d/1kiGPd49o_Qf-Oy1MqMCeVCFTUEnVKw_mbpCu9NnVsVk/edit?usp=sharinga)

A few things left to be desired, such as auto-linking of the loan title to the BLC page, adding author column, etc. If you have any other requests, please create an issue for this, here on Github: [Feature requests here](https://github.com/leonstafford/blcdataextractor/issues).

##Installation:

    git clone git@github.com:leonstafford/blcdataextractor.git
    cd blcdataextractor
    cp rename_this_file_to_config.yaml config.yaml # and put some values in the config file!
    #pip install -r requirements.txt (not yet created, just try to run and install anything it says is missing!)
    python blc_data_extractor.py

It will automate the process of logging into BLC and generating a CSV in the same folder containing all your investment informations. It currently expects you to be using 2FA and will prompt you in the shell to input it when it gets to the appropriate stage of logging in. (all of this happens on your local computer, there is no "phone home" or such nefarious behavior within this source code, which you may read in one file to confirm :).

