from pathlib import Path

class code:

	@property
	def val(self) -> str:
		return self._val
	
	@val.setter
	def val(self, val):
		self._val = val

	@property
	def soundFile(self):
		return self._sndF
	
	@soundFile.setter
	def soundFile(self, val):
		self._sndF = val

	def __init__(self, code, file):
		self.val = code
		self.soundFile = file

	def createFileFromList(file:str, lst:list):
		# The files for the doorbell program will be stored in the home folder
		fileHandle = open(f"{Path.home()}/doorbell/settings/" + file, "bw+")

		# Create file header with SETS magic code and the number of codes in the file
		fileHandle.write(bytes("SETS", "ASCII"))
		fileHandle.write(int.to_bytes(len(lst), 4))

		# Iterate through each code in the list and serialize it
		for cd in lst:
			if (type(cd) != code):
				fileHandle.close()
				raise TypeError("The list contains a type other than a code.")
			fileHandle.write(int.to_bytes(cd.val, 8))
			fileHandle.write(bytes(cd.soundFile, "ASCII"))
			fileHandle.write(bytes([0]))
			
		fileHandle.close()

	def createListFromFile(file:str) -> list[code]:
		# The files for the doorbell program will be stored in the home folder
		fileHandle = open(f"{Path.home()}/doorbell/settings/" + file, "br")
		contents = fileHandle.read()

		# Check for invalid file header
		if (len(contents) < 8):
			print("Invalid code file.")
			fileHandle.close()
			return
		if (contents[0:4] != bytes("SETS", "ASCII")):
			print("Invalid code file.")
			fileHandle.close()
			return
		
		codeCount = int.from_bytes(contents[4:8])
		codes = []
		index = 8

		# Iterate through each code in the file and add it to the list
		while (codeCount > 0):
			val = int.from_bytes(contents[index:index+8])
			index = index + 8
			startIdx = index
			while (contents[index] != 0):
				index += 1
			index += 1
			file = str(contents[startIdx:index], "ASCII")

			codes.append(code(val, file))
			codeCount -= 1


		fileHandle.close()
		return
