#from collections import abc
#print(issubclass(tuple, abc.Sequence))
#print(issubclass(list,  abc.MutableSequence))
#print(issubclass(tuple, abc.MutableSequence))

symbols = '$¢£¥€¤'

#codes = []
#for symbol in symbols:
#    codes.append(ord(symbol))
#print(codes)

#print(codes2 := [ord(symbol) for symbol in symbols])
#print(codes2)


#x = 'ABC'
#codes = [ord(x) for x in x]
#print(x, codes)
#codes = [last := ord(c) for c in x]
#print(last, x)

#numbers = [1,2,3,4,6]
#results = [result for x in numbers if (result := x**2) % 2 == 0]
#print(results)

#beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
#print(beyond_ascii)
#beyond_ascii = list(filter(lambda c: c>127, map(ord, symbols)))
#print(beyond_ascii)