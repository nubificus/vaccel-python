import vaccel

from vaccel.session import Session
from vaccel.noop import Noop

a = Session(flags=0)
b = Session(flags=1)

print(a.id(), b.id())

c = Noop.noop(a)
