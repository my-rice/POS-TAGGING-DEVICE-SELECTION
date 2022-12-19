from .queue import Queue

class Empty(Exception):
  pass

class ArrayQueue(Queue):
  """Implementazione di ADT Queue basata sul tipo list di Python usato dome array circolare."""
  DEFAULT_CAPACITY = 10          # dimensione di default di nuove code

  def __init__(self):
    """Crea una coda vuota."""
    self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
    self._size = 0
    self._front = 0

  def __len__(self):
    """Restituisce il numero di elementi nella coda."""
    return self._size

  def is_empty(self):
    """Restituisce True se la coda è vuota."""
    return self._size == 0

  def first(self):
    """Restituisce (m anon rimuove) l'elemento al front della coda.
       Raise Empty exception se la coda è vuota.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    return self._data[self._front]

  def dequeue(self):
    """Rimuove e restituisce l'elemento al front della coda.
       Raise Empty exception se la coda è vuota.
    """
    if self.is_empty():
      raise Empty('Queue is empty')
    answer = self._data[self._front]
    self._data[self._front] = None         # favorisce garbage collection
    self._front = (self._front + 1) % len(self._data)
    self._size -= 1
    return answer

  def enqueue(self, e):
    """Aggiunge un elemento al back della coda."""
    if self._size == len(self._data):
      self._resize(2 * len(self._data))     # raddoppia la dimensione dell'array se pieno
    avail = (self._front + self._size) % len(self._data)
    self._data[avail] = e
    self._size += 1

  def _resize(self, cap):                  # we assume cap >= len(self)
    """Ridimensiona l'array portandolo a lunghezza cap."""
    old = self._data                       # conserva la vecchia copia dell'array
    self._data = [None] * cap              # alloca una nuova list di dimensione cap
    j = self._front
    for k in range(self._size):
      self._data[k] = old[j]               # shifta gli indici per riallinearli
      j = (j + 1) % len(old)               # usa la vecchia dimensione come modulo
    self._front = 0                        # front riallineato a 0


