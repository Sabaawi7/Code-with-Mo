def pig_it(text):
    text_list = text.split()
    
    for i in range(len(text_list)):
        if text_list[i].isalpha():
            text_list[i] = text_list[i][1:] + text_list[i][0] + "ay"
    return " ".join(text_list)


print(pig_it("Hello World"))