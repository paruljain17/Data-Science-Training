#string is immutable means not changeable
#demoted by ' '," ",""" """ 
name = 'upflairs'
print(name)
print(type(name))


#accessing methods 
name='uPfalirspvt'
print(name.upper())
print(name.lower())
print(name.title())
print(name.capitalize())
print(name.casefold())
print(name.swapcase())
print(name.strip()) #string k andar whitespace ho usko remove krne k liye
print(name.rstrip()) #left k whitespace 
print(name.lstrip()) #right k whitespace
print(name.replace("pvt","ltd")) #kisi bhi chiz chracter ko replace krna hai nye words se
print(name.split("i")) #isme seperator ko show ni krega
print(name.partition("o")) #iske andar voh seperator ko bhi show krega part krke
print(name.startswith("u"))
print(name.endswith("i"))
#is wale sare methods condition check krne k liye kaam aate hai
print(name.isalpha())
print(name.isalnum())
print(name.isdigit())
print(name.islower())
print(name.encode('utf-8'))
print(name.encode('ascii'))
print(name.zfill(20))   #manlo extra characters chahiye toh voh additional char add krdeta hai left me
print(name.center(30,"1"))
print(name.ljust(30,"2"))
print(name.rjust(30,"*")) #isme apn single character hi fill kr skte hai only 


#indexing and slicing
#indexing is accessing single character from the string
#slicing is accessing multiple character from the string

# h e l l o isme har ek charcater ko ek number se index kiya jata hai
# 0 1 2 3 4  postive 
# -1 -2 -3 -4 -5  negative

name = 'upfalirs'
print(name[0])
print(name[-2])


name = 'upfalirs'
print(name[0:8])

##formatted string //f.string
#age = 10
#text = f"my age is {age}"
#print(text)

text = "my name is "



