class Reservation:
  def __init__(self, roomNumber, checkIn, checkOut):
    self.roomNumber = roomNumber
    self.checkIn = checkIn
    self.checkOut = checkOut

  def __str__(self):
    return "Room Number: {0}, Check In Time: {1}, Check Out Time: {2}".format(self.roomNumber, self.checkIn, self.checkOut)