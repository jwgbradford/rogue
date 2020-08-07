def convert_to_binary(doors):
    doors_dec = doors
    doors_bin  = [0, 0, 0, 0]
    if doors_dec % 2 == 1:
        doors_bin[3] = '1'
        doors_dec -= 1
    if doors_dec % 2 == 0 and doors_dec > 0:
        doors_bin[2] = '1'
        doors_dec -= 2
    if doors_dec % 4 == 0 and doors_dec > 0:
        doors_bin[1] = '1'
        doors_dec -= 4
    if doors_dec % 8 == 0 and doors_dec > 0:
        doors_bin[0] = '1'
        doors_dec -= 8
    return doors_bin
if True:

    again = input('Would you like another qestion (q), or to exit (x)?')
    if again.lower() == 'x':
        playing = False