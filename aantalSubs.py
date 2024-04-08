subsidiepot = {}

def reset_subsidiepot():
    global subsidiepot
    subsidiepot = {
        0: 10000000,
        1: 14400000,
        2: 71000000,
        3: 67000000,
        4: 58000000,
        5: 58000000,
        6: 58000000,
        7: 58000000,
        8: 58000000,
        0: 58000000
        }
    
    

def Tracking_Subs(model, subsidie, maand):
    count_subs = 0
    jaar = maand // 12

    if jaar in subsidiepot:
        beschikbaar_bedrag = subsidiepot[jaar]
        if beschikbaar_bedrag >= subsidie:
            subsidiepot[jaar] -= subsidie
            count_subs += 1
            return True
        
        else:
            return False
    

    else:
         return False 




