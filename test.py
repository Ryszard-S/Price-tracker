name = "CUKIERNIA P. CHOJECKI Ciasto bananowe"
name = name.split(" ")
brand: str = ""
title: str = ""
for i in name:
    print(i)
    if i.isupper():
        brand += i + " "
    else:
        title += i + " "

brand = brand.strip()
title = title.strip()
print(brand, title, sep="\n")
