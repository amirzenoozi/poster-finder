__author__ = "Amirhossein Douzendeh Zenoozi"
__license__ = "MIT"
__version__ = "1.5"

from bs4 import BeautifulSoup
import urllib
import urllib.request as req
import requests
import re
import platform
import time

BASE_URL = 'http://www.impawards.com/'
OS_NAME = platform.system()
IS_SINGLE = False

def findTitle( url ):
    result = url.replace( BASE_URL , '')
    result = result.replace('.html', '')
    result = result.split('/')[-1]
    result = result.replace('_', ' ')
    return result

def generateImageUrl( url ):
    pattern = re.compile("^([0-9]{4})")
    rawUrl = url.replace( BASE_URL , '')
    rawUrl = rawUrl.replace( '_ver1' , '')
    rawUrl = rawUrl.replace('.html', '')
    parts = rawUrl.split('/')
    finalUrl = BASE_URL[:-1];

    for part in parts:
        finalUrl += '/'
        finalUrl += part
        if( pattern.match(part) ):
            finalUrl += '/posters'
    return finalUrl

def findImageList( url ):
    global IS_SINGLE
    _PAGE_ = requests.get( url )
    _SOUP_ = BeautifulSoup( _PAGE_.content, 'html.parser' )

    #Check Empty List
    if ( _SOUP_.find_all(id='altdesigns') ):
        _TOTAL_SIZE_ = len( _SOUP_.find_all(id='altdesigns')[0].contents )
        IS_SINGLE = False
    else:
        _TOTAL_SIZE_ = 1
        IS_SINGLE = True

    return _TOTAL_SIZE_

def downloadImageFile( imageUrl, targetName ):
    try:
        req.urlretrieve( imageUrl+'.jpg', targetName+'.jpg')
    except urllib.error.HTTPError as err:
        print('\n')
        print('========================')
        print(f'Error Code: {err.getcode()}')
        print(f'Target URL: {imageUrl}.jpg' )
        print('========================')
        print('\n')
    return True

def checkUrlFormat( url ):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if( pattern.match( url ) ):
        return True
    else:
        return False

def init():
    _TARGET_ = ''
    while( True ):
        _TARGET_ = input('Please Inter Movie Page URL: ')
        if( _TARGET_ == 'end' ):
            break
        else:
            if( checkUrlFormat( _TARGET_ ) ):
                _TITLE_ = findTitle( _TARGET_ )
                _COUNT_ = findImageList( _TARGET_ )

                targetImageUrl = generateImageUrl( _TARGET_ )
                for i in range(0, _COUNT_):
                    #Check Posters Item
                    if( i == 0 and not IS_SINGLE ):
                        SavedName = _TITLE_.title() + ' Poster ' + str(i)
                        downloadImageFile( targetImageUrl + '_ver' + str(i+1), SavedName )
                    elif( i == 0 and IS_SINGLE ):
                        SavedName = _TITLE_.title() + ' Poster ' + str(i)
                        downloadImageFile( targetImageUrl, SavedName )
                    else:
                        SavedName = _TITLE_.title() + ' Poster ' + str(i).zfill(2)
                        downloadImageFile( targetImageUrl + '_ver' + str(i+1), SavedName )

                    #Print Loading In Single Line in Linux OS
                    if( OS_NAME != 'Windows' ):
                        print(f'Poster Number {str(i+1).zfill(2)}/{ _COUNT_ } Saved!', flush=True, end='\r')
                    else:
                        print(f'Poster Number {str(i+1).zfill(2)}/{ _COUNT_ } Saved!\n', flush=True, end='')
                    time.sleep(0.5) 
                print('\n')
            else:
                print('\n')
                print('========================')
                print('Please Inter Valid URL!!')
                print('========================')
                print('\n')

    
if __name__ == '__main__':
    init()
else:
    print(__name__)
