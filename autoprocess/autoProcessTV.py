# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.


import sys
import urllib
import os.path

class AuthURLOpener(urllib.FancyURLopener):
    def __init__(self, user, pw):
        self.username = user
        self.password = pw
        self.numTries = 0
        urllib.FancyURLopener.__init__(self)
    
    def prompt_user_passwd(self, host, realm):
        if self.numTries == 0:
            self.numTries = 1
            return (self.username, self.password)
        else:
            return ('', '')

    def openit(self, url):
        self.numTries = 0
        return urllib.FancyURLopener.open(self, url)


def processEpisode(dirName, settings, nzbName=None):
    
    host = settings.Sickbeard['host']
    port = settings.Sickbeard['port']
    username = settings.Sickbeard['user']
    password = settings.Sickbeard['pass']
    try:
        ssl = int(settings.Sickbeard['ssl'])
    except:
        ssl = 0
    
    try:
        web_root = settings.Sickbeard['web_root']
    except:
        web_root = ""
    
    params = {}
    
    params['quiet'] = 1

    params['dir'] = dirName
    if nzbName != None:
        params['nzbName'] = nzbName
        
    myOpener = AuthURLOpener(username, password)
    
    if ssl:
        protocol = "https://"
    else:
        protocol = "http://"

    url = protocol + host + ":" + port + web_root + "/home/postprocess/processEpisode?" + urllib.urlencode(params)
    
    print "Opening URL:", url
    
    try:
        urlObj = myOpener.openit(url)
    except IOError, e:
        print "Unable to open URL: ", str(e)
        sys.exit(1)
    
    result = urlObj.readlines()
    for line in result:
        print line
        