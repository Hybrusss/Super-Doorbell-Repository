class rqPacket:
	def __init__(self, data:bytes):
		self.backingData = data

	@property
	def kind(self) -> int:
		return int.from_bytes(self._data[0:4])
	
	@kind.setter
	def kind(self, val:int):
		newBytes = val.to_bytes(4)
		self._data = bytes(newBytes + self._data[12:self.size])

	@property
	def size(self) -> int:
		return int.from_bytes(self._data[4:12])
	
	@size.setter
	def size(self, val:int):
		newBytes = val.to_bytes(8)
		self._data = bytes(self._data[0:4] + newBytes + self._data[12:self.size])
	
	@property
	def mainData(self) -> bytes:
		return self._data[12:self.size]
	
	@mainData.setter
	def mainData(self, data:bytes):
		self._data = bytes(self._data[0:12] + data)
			
	@property
	def backingData(self) -> bytes:
		return self._data
	
	@backingData.setter
	def backingData(self, data:bytes):
		self._data = data