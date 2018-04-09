class State:
  def __init__(self,state,parent,cost,move_list):
    self.state = state
    self.parent = parent
    self.cost = cost

    if self.state:
      self.str_state = ''.join(str(e) for e in self.state)
    
    if move_list is not None:
      self.move_list = move_list
    else:
      self.move_list = []
  
  def __eq__(self, other):
    if type(self) is type(other):
      return self.state == other.state
    else:
      return False