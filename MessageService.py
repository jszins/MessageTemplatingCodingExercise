import time
import pytz
from datetime import datetime, timezone
import JsonOperations
from Guest import Guest
from Reservation import Reservation
from Message import Message
from Company import Company

class MessageService:
    def __init__(self):
      self.guests = JsonOperations.loadGuestsDict()
      self.messages = JsonOperations.loadMessageDict()
      self.companies = JsonOperations.loadCompaniesDict()

    #  The driver of the program, uses helper methods to choose a guest and company, 
    #  then runs the method chooseMessage with the guest and company and returns the templated message
    #  with dynamic variables filled in  
    def execute(self):
        userInput = input("Hello, welcome to my Kipsu Coding Exercise!\nPlease type -m to create a message!\n")
        if userInput == "-m":
          guestNumber = self._chooseGuest()
          while guestNumber < 1 or guestNumber > 6:
            guestNumber = self._chooseGuest(False)
          companyNumber = self._chooseCompany()
          while companyNumber < 1 or companyNumber > 6:
            companyNumber = self._chooseCompany(False)
          selectedGuest = self.guests[guestNumber]
          selectedCompany = self.companies[companyNumber]
          chosenMessage = self._chooseMessage(selectedGuest, selectedCompany)
          print(chosenMessage)
        else:
          self.execute()

    #  Method to choose guests from a list provided by JSON data. Boolean flag for re-running based on
    #  invalid input
    def _chooseGuest(self, tryAgain=True):
      guestString = ""
      for id, guest in self.guests.items():
        guestString += "{0}: ".format(id) + guest.fullName() + "\n"
      if tryAgain != True:
        guestNumber = input("Looks like you entered an invalid option. Here's the list of guests\n" \
        "{0}".format(guestString))
      else:
        guestNumber = input("To start, select a guest to send a message to.\n"
          "Here are the current guests available to send a message to:\n"
          "{0}"
          "Type the number preceding their name:\n".format(guestString)) 
      return int(guestNumber)

    #  Method to choose companies from a list provided by JSON data. Boolean flag for re-running based on
    #  invalid input
    def _chooseCompany(self, tryAgain=True):
      companyString = ""
      for id, company in self.companies.items():
        companyString += "{0}: ".format(id) + company.name + "\n"
      if tryAgain != True:
        companyNumber = input("Looks like you entered an invalid option. Here's the list of companies\n"
        "{0}".format(companyString))
      else:
        companyNumber = input("Now, select your company\n"
        "{0}"
        "Type the number preceding your name:\n".format(companyString)) 
      return int(companyNumber) 

    #  Method for choosing from templated messages. The dynamic spots are prefixed and suffixed with underscores
    #  Runs format message to do final formatting before returning
    def _chooseMessage(self, guest, company):
      messageOne = "1: Room _Room Number_ is now ready for you. Enjoy your stay, and let us know if you need anything!\n"
      messageTwo = "2: Hello _Guest_. This is a reminder that your checkout time is _Checkout Time_. Please have your room " \
      "ready for checkout at this time\n"
      messageThree = "3: At _Company_, we appreciate our guests. Feel free to come down anytime for " \
      "information on the surrounding area\n"
      messageFour = "4: Hi _Guest_. Your checkin time is _Checkin Time_. We'll have your room ready by then. " \
      "Here at _Company_, we pride ourselves on prompt service!\n"
      messageNumber = input("Now, select a message from our templates, or create your own.\n"
      "Greetings will be personalized depending on the time you send your message!\n" +
      messageOne + 
      messageTwo + 
      messageThree +
      messageFour + 
      "5: Create your own template\n"
      )
      formattedMessage = self._formatMessage(int(messageNumber), guest, company) 
      return formattedMessage

    #  Conditional statements to decide what templated message was chosen and fill in appropriate data
    #  Also formats the checkout time depending on the timezone of specific company
    def _formatMessage(self, number, guest, company):
      if number != 1 and number != 2 and number != 3 and number != 4 and number != 5:
        print("Invalid number chosen!\n")
        self._chooseMessage(guest, company)
      checkInDT = self._formatTimeZone(guest.reservation.checkIn, company)
      checkOutDT = self._formatTimeZone(guest.reservation.checkOut, company)
      checkInTimeFormatted = checkInDT.strftime("%D %I:%M %p")
      checkOutTimeFormatted = checkOutDT.strftime("%D %I:%M %p")
      if number == 1:
        message = self.messages[number].body.format(guest.reservation.roomNumber)
        return message
      if number == 2:
        message = self.messages[number].body.format(guest.fullName(), checkOutTimeFormatted)
        return message 
      if number == 3:
        message = self.messages[number].body.format(company.name)
        return message
      if number == 4:
        message = self.messages[number].body.format(guest.fullName(), checkInTimeFormatted, company.name)
        return message
      else:
        return self._setupTemplateMessage(guest, company)

    #  Function that creates a templated message with specified dynamic content. Content MUST be prefixed and suffixed
    #  with one underscore in order to be rendered, in addition to having the correct options specified. The while loop 
    #  loops through the options, and if it finds an underscore, it then scans ahead to find the matching underscore.
    #  when this is found, it is able to splice the string and insert in the desired data based on chosen guest and company.
    #  Wrapped in a try/except block to print a generic error message based on something wrong in the string or the options
    def _createTemplateMessage(self, message, options, guest, company):
      try:
        i = 0
        while options:
          if message[i] == "_":
            j = i+1
            while message[j] != "_":
              j += 1
            if options[0] == "1":
              message = message[:i] + guest.fullName() + message[j+1:]
              del options[0]
              i = j
              continue
            if options[0] == "2":
              message = message[:i] + str(guest.reservation.roomNumber) + message[j+1:]
              del options[0]
              i = j
              continue 
            if options[0] == "3":
              message = message[:i] + str(guest.reservation.checkIn) + message[j+1:]
              del options[0]
              i = j
              continue       
            if options[0] == "4":
              message = message[:i] + str(guest.reservation.checkOut) + message[j+1:]
              del options[0]
              i = j
              continue
            if options[0] == "5":
              message = message[:i] + company.name + message[j+1:]
              del options[0]
              i = j
              continue
          i += 1
        newId = max(self.messages.keys()) + 1
        newTemplate = Message(newId, message)
        return newTemplate
      except:
        print("Something wasn't right with the information you entered\n")
        return self._setupTemplateMessage(guest, company)

    #  Method to read in customer options for dynamic content. 5 dynamic choices to render. Dynamic choices are made by placing
    #  One underscore both before and after the text. The text in the underscores is irrelevant. The options are what actually
    #  makes the content dynamic. 
    def _setupTemplateMessage(self, guest, company):
      choice = ""
      options = []
      dynamicContent = "1: Guest Full Name\n" \
      "2: Room Number\n" \
      "3: Checkin Time\n" \
      "4: Checkout Time\n" \
      "5: Company Name\n"
      message = input("Type in a template message like the ones above.\n" \
      "Data available for dynamic rendering:\n" \
      "{0}" \
      "To render dynamic content, use 1 underscore preceding and following what you'd like to appear there.\n" \
      "For example: Your Room Number is _Room Number_\n".format(dynamicContent))
      choice = input("Now, enter in the numbers of the content you'd like to fill in dynamically.\n"
      "{0}"
      "Type 'end' to finish adding dynamic content\n".format(dynamicContent))
      if choice != "end":
        options.append(choice)
        nextChoice = ""
        while nextChoice!= "end":
          nextChoice = input("")
          if nextChoice != "end":
            options.append(nextChoice)
      return self._createTemplateMessage(message, options, guest, company)
    
    # Helper method to format timezone from JSON data provided to pytz timezones
    def _formatTimeZone(self, utcTime, company):
      if company.timezone == "US/Central":
        local_tz = pytz.timezone("America/Chicago")
        utc_dt = datetime.fromtimestamp(utcTime, timezone.utc)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)
      if company.timezone == "US/Pacific":
        local_tz = pytz.timezone("America/Los_Angeles")
        utc_dt = datetime.fromtimestamp(utcTime, timezone.utc)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)
      if company.timezone == "US/Eastern":
        local_tz = pytz.timezone("America/New_York")
        utc_dt = datetime.fromtimestamp(utcTime, timezone.utc)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)
