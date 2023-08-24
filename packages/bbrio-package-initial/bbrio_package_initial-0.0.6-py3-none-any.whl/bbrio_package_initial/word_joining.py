class xyz:
  def __init__(self,x,k=4):
    self.string=x
    self.k=k
  def word_join(self):
    l=[]
    for i in range(1,self.k+1):
        v=' '.join(self.string[:i])
        if v.count(' ')<i-1:
            v=v+(" "+'NA')*(i-1)
        l.append(v)
    return l