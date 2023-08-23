def binary_octal(binary):
    lisr=[]
    while len(binary) % 3 != 0:
        binary = '0' + binary

    octal = ''
    i = 0
    while i < len(binary):
        
        three_digits = binary[i:i+3]
        decimal = int(three_digits, 2)
        octal = oct(decimal)[2:] 
        lisr.append(octal)
        i+=3
    hg=""
    for i in lisr:
        hg=hg+i
    return hg

