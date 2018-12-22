class Guest:
  def __init__(self, id, firstName, lastName, reservation):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.reservation = reservation

  def __str__(self):
    return "Guest Full Name: {0} {1}, Reservation Details: {2}".format(self.firstName, self.lastName, self.reservation)

  def fullName(self):
    return self.firstName + " " + self.lastName