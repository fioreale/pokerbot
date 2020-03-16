#import Input_file_parser as NewP

if __name__ == '__main__':
    #print(NewP.parse_line('node /C:JQ player 1 actions c r'))
    #asd = 'JK=1.000000 QJ=1.000000 QK=1.000000 KJ=1.000000'
    #print(asd.split())
    a = ['99=2.000', 'KJ=1.000']
    for i in a:
        splitted_values = i.split('=')
        print(splitted_values)