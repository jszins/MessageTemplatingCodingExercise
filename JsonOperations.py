import json
from Guest import Guest
from Reservation import Reservation
from Message import Message
from Company import Company

def loadMessageDict():
  messages = json.loads(open('./Messages.json').read())
  currentMessages = {}
  for message in messages:
    currentMessage = Message(message['id'], message['body'])
    currentMessages.update({currentMessage.id: currentMessage})
  return currentMessages

def loadGuestsDict():
  guests = json.loads(open('./Guests.json').read())
  currentGuests = {}
  for guest in guests:
    currentRes = Reservation(guest['reservation']['roomNumber'], \
                              guest['reservation']['startTimestamp'], \
                              guest['reservation']['endTimestamp'])
    newGuest = Guest(guest['id'], \
                      guest['firstName'], \
                      guest['lastName'], \
                      currentRes)
    currentGuests.update({newGuest.id: newGuest})
  return currentGuests

def loadCompaniesDict():
  companies = json.loads(open('./Companies.json').read())
  currentCompanies = {}
  for company in companies:
    currentCompany = Company(company['id'], \
                              company['company'], \
                              company['city'], \
                              company['timezone'])
    currentCompanies.update({currentCompany.id: currentCompany})
  return currentCompanies