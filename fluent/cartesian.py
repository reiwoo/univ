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

#colors = ['black', 'white']
#sizes = ['S', 'M', 'L']
#tshirts = [(color, size) for color in colors for size in sizes]
#print(tshirts)
#for color in colors:
#    for size in sizes:
#        print((color, size))
#tshirts = [(color, size) for size in sizes
#                         for color in colors]
#print(tshirts)

#print(tuple(ord(s) for s in symbols))
#import array
#print(array.array('I', (ord(s) for s in symbols)))
#colors = ['black', 'white']
#sizes = ['S', 'M', 'L']
#for tshirt in (f'{c}-{s}' for c in colors for s in sizes): print(tshirt)

#lax_coordinates = (33.9425, -118.408056) 
#city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)
#traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
#for passport in sorted(traveler_ids):
#    print('%s/%s' % passport)

#import os
#file = os.path.split('/home/luciano/.ssh/id_rsa.pub')
#print(file)
#a, *b, c, d, e = range(6)
#print(a, b, c, d, e)
#def fun(a, b, c, d, *rest):
#    return a, b, c, d, *rest
#print(fun(*range(4,20)))
#print([*range(4), 4])
#print({*range(4), 4, *(5,6,7)})
metro_areas = [
 ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)), 
 ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
 ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
 ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
 ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
#def main():
#    print(f'{"City":^15} | {"latitude":^9} | {"longitude":^9}')
#    for name, _, _, (lat, lon) in metro_areas:
#        if lon <= 0:
#            print(f'{name:^15} | {lat:^9.4f} | {lon:^9.4f}')
#if __name__ == "__main__":
#    main()
#def main():
# print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
# for record in metro_areas:
#    match record: 
#        case [name, _, _, (lat, lon)] if lon >= 0: 
#            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')
#if __name__ == "__main__":
#    main()  
#case [str(name), *_, (float(lat), float(lon))]:

#def evaluate(exp: Expression, env: Environment) -> Any:
#    "Evaluate an expression in an environment."
#    match exp:
#        case ['quote', x]:
#            return x
#        case ['if', test, consequence, alternative]: 
#            if evaluate(test, env):
#                return evaluate(consequence, env)
#            else:
#                return evaluate(alternative, env)
#        case ['lambda', [*parms], *body] if body:
#            return Procedure(parms, body, env)
#        case ['define', Symbol() as name, value_exp]:
#            env[name] = evaluate(value_exp, env)
#        # ... еще несколько строк опущено
#        case _:
#            raise SyntaxError(lispstr(exp))
#s = 'bicycle'
#print(s[0:7:3])

invoice = """
 0.....6.................................40........52...55........
 1909    Pimoroni PiBrella                  $17.50    3     $52.50
 1489    6mm Tactile Switch x20             $4.95     2     $9.90
 1510    Panavise Jr. - PV-201              $28.00    1     $28.00
 1601    PiTFT Mini Kit 320x240             $34.95    1     $34.95
 """

SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
QUANTITY = slice(52, 55)
ITEM_TOTAL = slice(55, None)
line_items = invoice.split('\n')[2:][:-1]
for item in line_items:
    print(item)
