import time

class Message:
  def __init__(self, id, body):
    self.id = id
    self.body = body
    self.createdOn = time.time()
    self._customGreeting()
    

  def _customGreeting(self):
    hour = int(time.strftime("%H", time.localtime(self.createdOn)))
    if hour < 12:
      self.body = "Good Morning! " + self.body
    if hour > 12 and hour < 17:
      self.body = "Good Afternoon! " + self.body
    if hour > 17:
      self.body = "Good Evening! " + self.body
    

  

  
  
