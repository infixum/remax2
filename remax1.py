"""
REMAX code exercise.
"""

import urllib2

from xml.etree import ElementTree  
import pprint

import sys

# Booj's test data URL.
XMLURL = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
XMLFILE = 'remax.xml'

# Required Fields.
# Root node:
LISTINGS = 'Listings'

# Node for each listing.
LISTINGX = 'Listing'

# Header for MlsId and others.
LISTINGDETAILS = 'ListingDetails'
# Subfields.
MLSID = 'MlsId'
MLSNAME = 'MlsName'
DATELISTED = 'DateListed'
PRICE = 'Price'

# Header for StreetAddress we want (more than one in XML feed).
LOCATION = 'Location'
# Subfields.
STREETADDR = 'StreetAddress'

# Header for Bedrooms.
BASICDETAILS = 'BasicDetails'
# Subfields.
BEDROOMS = 'Bedrooms'
BATHROOMS = 'Bathrooms'
DESCRIPTION = 'Description'

# Header for Appliances.
RICHDETAILS = 'RichDetails'
# Subfields.
ROOMS = 'Rooms'
# Sub-sub field.
ROOMX = 'Room'
APPLIANCES = 'Appliances'
# Sub-sub field.
APPLIANCEX = 'Appliance'

# Assignment
# 
# Write a script to download and parse the given XML feed, manipulate some of the data, and deliver a CSV of the required fields. You may use any additional libraries that you wish, please include a requirements.txt if you do.
# CSV Requirements:
# 
#     1) Contains only properties listed from 2016 [DateListed]
#     2) Contains only properties that contain the word "and" in the Description field
#     3) CSV ordered by DateListed
#     4) Required fields:
#         a) MlsId
#         b) MlsName
#         c) DateListed
#         d) StreetAddress
#         e) Price
#         f) Bedrooms
#         g) Bathrooms
#         h) Appliances (all sub-nodes comma joined)
#         i) Rooms (all sub-nodes comma joined)
#         j) Description (the first 200 characters)
# 
# Technical Requirements
# 
#     5) Interpreter version: python 2.7
#     6) Reasonable unit test coverage
#     7) All libraries used must be documented in requirements.txt
#         We will be using pip install -r requirements.txt prior to running your code
#     8) Raw information to parse / feed url
#         http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml
#         a) This feed must be downloaded from with in the script, raw data must not be downloaded manually
# 
# Submission Requirements
# 
#     9) Work should be tracked with Git
#     10) Submit final product by submitting a pull request
# 
# Purpose
# 
# A lot of the work in our department is parsing and manipulating data from a variety of sources. The given example is one of our XML files that we send to Zillow for property syndication. Our goal in this test is to see how you will approach the processing of this feed. Your solution should take into the account that there will be other XML feeds that need parsing as well, so how modular/reusable you make the code is very important.
# 
# Time Considerations
# 
# This assignment is expect to take a few hours. We ask that you do not spend too much time on this solution. If you are stuck or have questions, feel free to reach out and we will answer quickly.

def getdatafromweb():
    """
    Grab data from website.

    Returns text.
    """
    print 'Connecting to page via urllib2 . . .'
    response = urllib2.urlopen(XMLURL)
    print 'Getting xml . . .'
    return response.read()

def writexmltofile(text):
    """
    Writes xml text to a file.
    """
    print 'Writing data from web to xml file locally . . .'
    with open(XMLFILE, 'w') as f:
        print 'Writing xml to file . . .'
        print >> f, text
        f.close()

def writeoutxmlstructure(root):
    """
    Write out data indented in a way
    that is easier to visualize than
    XML tagged data.

    root is an ElementTree object.
    """
    # Get feel for data structure / schema in XML.
    with open('xmlstructure.txt', 'w') as f2:
        print >> f2, root.tag
        for n in xrange(len(root)):
            print >> f2, '    ' + root[n].tag
            for o in xrange(len(root[n])):
                print >> f2, '        ' + root[n][o].tag
                for p in xrange(len(root[n][o])):
                    print >> f2, '            ' + root[n][o][p].tag
                    # Get appliances.
                    for q in xrange(len(root[n][o][p])):
                        print >> f2, '                ' + root[n][o][p][q].tag

def putessentialdataintodictionary(root):
    """
    Gets essential data for the assignment
    into a dictionary keyed on MLSId.

    root is an ElementTree object.

    Returns a dictionary.
    """
    numlistings = 0
    listings = {}
    # Check that Listings is top node.
    if root.tag == LISTINGS:
        for n in xrange(len(root)):
            # Inidivdual listing.
            requireddata = {}
            if root[n].tag == LISTINGX:
                numlistings += 1
                for o in xrange(len(root[n])):
                    # Listing Details.
                    if root[n][o].tag == LISTINGDETAILS:
                        for p in xrange(len(root[n][o])):
                            # MLSId.
                            if root[n][o][p].tag == MLSID:
                                requireddata[MLSID] = root[n][o][p].text
                            # MLSName.
                            elif root[n][o][p].tag == MLSNAME:
                                requireddata[MLSNAME] = root[n][o][p].text
                            # DateListed.
                            elif root[n][o][p].tag == DATELISTED:
                                requireddata[DATELISTED] = root[n][o][p].text
                            # Price.
                            elif root[n][o][p].tag == PRICE:
                                requireddata[PRICE] = root[n][o][p].text
                    elif root[n][o].tag == LOCATION:
                        for p in xrange(len(root[n][o])):
                            # StreetAddress.
                            if root[n][o][p].tag == STREETADDR:
                                requireddata[STREETADDR] = root[n][o][p].text
                    elif root[n][o].tag == BASICDETAILS:
                        for p in xrange(len(root[n][o])):
                            # Bedrooms.
                            if root[n][o][p].tag == BEDROOMS:
                                requireddata[BEDROOMS] = root[n][o][p].text
                            # Bathrooms.
                            elif root[n][o][p].tag == BATHROOMS:
                                requireddata[BATHROOMS] = root[n][o][p].text
                            # Description.
                            elif root[n][o][p].tag == DESCRIPTION:
                                requireddata[DESCRIPTION] = root[n][o][p].text
                    elif root[n][o].tag == RICHDETAILS:
                        for p in xrange(len(root[n][o])):
                            # Appliances.
                            if root[n][o][p].tag == APPLIANCES:
                                quotedtexttojoin = []
                                for q in xrange(len(root[n][o][p])):
                                    quotedtexttojoin.append(root[n][o][p][q].text)
                                requireddata[APPLIANCES] = quotedtexttojoin
                            # The room thing seems to always be two - 
                            # bedrooms / bathroom.
                            elif root[n][o][p].tag == ROOMS:
                                quotedtexttojoin = []
                                for q in xrange(len(root[n][o][p])):
                                    quotedtexttojoin.append(root[n][o][p][q].text)
                                requireddata[ROOMS] = quotedtexttojoin
                # Get date listed and mlsid in tuple as key.
                listings[(requireddata[DATELISTED], requireddata[MLSID])] = requireddata 
    return listings

text = getdatafromweb()
# Not essential but helpful for debugging.
writexmltofile(text)
# Not part of required solution, but key
# key to getting solution set up and useful
# for debugging.
root = ElementTree.fromstring(text)
writeoutxmlstructure(root)
listings = putessentialdataintodictionary(root)

with open('listingsdictionary.py', 'w') as f3:
    pprint.pprint(listings, stream=f3)

# General strategy:
#
# 1) loop through listings.
#
# 2) make sure all required fields are there, note indices.
#
# 3) filter on 
#
#        a) DateListed
#
#        b) full word "and" in Description.
#
#        c) sort by time interpretation of DateListed string.

print 'Done'
