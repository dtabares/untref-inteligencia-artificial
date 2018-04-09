class Result:
  def __init__(self,node,cost,cutoff,solved):
    self.node = node
    self.cost = cost
    self.cutoff = cutoff
    self.solved = solved