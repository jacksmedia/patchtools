def string_splitter (text, length):
    return [text[i:i+length] for i in range(0,
     len(text), length)]

string = "abcdefghiklmnopqrstuvwxyz"
sub_str_length = 9
result = string_splitter(string, sub_str_length)
print(result)
# ['abcdefghi',klmnopqrs',tuvwxyz']