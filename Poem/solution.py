import os
import re
import glob
import time
from collections import defaultdict
from os import path


# preprocess a string by leaving only letters, spaces and new lines
def preprocess(text):
		text = text.lower()
		text = text.lstrip().rstrip()
		text = ''.join([c for c in text if c.isalpha() or c == ' ' or c == '\n'])
		return text

# split the file Poem-collection.txt into separate files for each poem and preprocess the text
def preprocess_collection():
		poem_collection = open('Poem-collection.txt').read()
		poem_numbers = [int(s) for s in poem_collection.split() if s.isdigit()]
		poem_docs = re.sub("\d+", "#", poem_collection).split('#')[1:]
		
		if not os.path.exists('docs'):
				os.makedirs('docs')
		
		for i in range(len(poem_docs)):
				doc = preprocess(poem_docs[i])
				id = poem_numbers[i]
				filename = "docs/doc" + str(id) + ".txt"
				file = open(filename, "w")
				file.write(doc)
				file.close() 


# trie node data structure
class TrieNode:

	def __init__(self):
		self.children = defaultdict()
		self.docs = {}
		self.terminating = False # indicates if the current node ends some word in our vocabulary or not

# trie data structure which consists of trie nodes
class Trie:

	def __init__(self):
		self.root = self.get_node()

	def get_node(self):
		return TrieNode()

	def get_index(self, ch):
		return ord(ch) - ord('a')

	def insert(self, word, doc_id):
		root = self.root
		len1 = len(word)

		for i in range(len1):
			index = self.get_index(word[i])

			if index not in root.children:
				root.children[index] = self.get_node()
			root = root.children.get(index)
			if not doc_id in root.docs:
				root.docs[doc_id] = 1
			else:
				root.docs[doc_id] += 1 # increment the frequency count
		root.terminating = True

	def search(self, word):
		root = self.root
		len1 = len(word)

		for i in range(len1):
			index = self.get_index(word[i])
			if not root:
				return False
			root = root.children.get(index)
		return root.docs if root and root.terminating else []


# inverted index data structure
class InvertedIndex:

		def __init__(self):
				self.vocab = Trie()
				self.documents = {}
				self.load()

		def find(self, word):
				word = preprocess(word)
				return self.vocab.search(word)

		def add(self, document, id):
				for word in document.split():
						self.vocab.insert(word, id)
				self.documents[id] = document

		# load the text files into the local documents array before we start using them
		def load(self):
				filenames = os.listdir("docs")
				filenames.sort()
				for fn in filenames:
						doc = open("docs/" + fn).read()
						id = int(re.findall(r'\d+', fn)[0])
						self.add(doc, id)


# BMHS class
class BMHS:

		def __init__(self):
				self.documents = {}
				self.load()

		# function to run the search in all poem texts
		def find(self, word):
				results = {}
				for id in self.documents:
						tmp = self.strStr(self.documents[id], word)
						if (tmp != -1):
								results[id] = tmp
				return results

		# the main BMHS algorithm function
		def strStr(self, haystack: str, needle: str):
				if haystack is None or needle is None:
						return -1
				elif needle == "":
						return 0
				else:
						lens, lenp = len(haystack), len(needle)
						if lens < lenp:
								return -1
						else:
								i = j = 0
								while i < lens and j < lenp:
										# Char matches between string and pattern
										if haystack[i] == needle[j]:
												 i += 1
												 j += 1
										else:
												# Mismatch, get index of next char in string as pin
												pin = i + lenp - j
												# Pin overhead, must be no matches any more
												if pin >= lens:
														return -1
												else:
														# Find occurrence of haystack[pin] in pattern
														k = lenp - 1
														while k >= 0 and needle[k] != haystack[pin]:
																k -= 1
														# Update i and j for next loop
														# Align two strings
														i, j = pin - k, 0
								# Note: if match, result index should be i - j
								return i - j if j == lenp else -1

		# load the text files into the local documents array before we start using them
		def load(self):
				filenames = os.listdir("docs")
				filenames.sort()
				for fn in filenames:
						doc = open("docs/" + fn).read()
						id = int(re.findall(r'\d+', fn)[0])
						self.documents[id] = doc

		

# launch the preprocessing to generate the doc files in the directory docs/
preprocess_collection()

# extract all words from collection to use them for successful search testing
text = preprocess(open("Poem-collection.txt").read())
text = text.replace("\n", " ")
words = ''.join([c for c in text if c.isalpha() or c == ' ']).split()


# testing for successful searches, 10 searches for each algorithm
print("Successful:\n")
print("Inverted Index:")

# set the starting time to use it as a reference
start_time = time.time() * 1000
inverted_index = InvertedIndex()
for n in range(1, 11):
		for j in range(n):
				inverted_index.find(words[j % 1136])
		current_time = time.time() * 1000 - start_time
		print("n = %d, time = %f" %(n, current_time))


print("\nBMHS:")
# set the starting time to use it as a reference
start_time = time.time() * 1000
bmhs = BMHS()
for n in range(1, 11):
		for j in range(n):
				bmhs.find(words[j % 1136])
		current_time = time.time() * 1000 - start_time
		print("n = %d, time = %f" %(n, current_time))


# testing for unsuccessful searches, 10 searches for each algorithm
print("\nUnsuccessful:\n")
print("Inverted Index:")

# set the starting time to use it as a reference
start_time = time.time() * 1000
inverted_index = InvertedIndex()		
for n in range(1, 11):
		for j in range(n):
				inverted_index.find("unsuccessful")
		current_time = time.time() * 1000 - start_time
		print("n = %d, time = %f" %(n, current_time))
		

print("\nBMHS:")
# set the starting time to use it as a reference
start_time = time.time() * 1000
bmhs = BMHS()
for n in range(1, 11):
		for j in range(n):
				bmhs.find("unsuccessful")
		current_time = time.time() * 1000 - start_time
		print("n = %d, time = %f" %(n, current_time))
		
		
		
		lalalalalla
