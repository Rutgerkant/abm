# deze file wordt niet gebruikt in het model. Dit was niet helemaal uitgewerkt
# we hebben een andere manier gebruikt om inzicht te krijgen over de kosten van subsidies


subsidiepot = {}

def reset_subsidiepot():
    print("Hij wordt aangeroepen")
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
        10: 58000000
        }
    
    print("Hij is gereset")
    

def Tracking_Subs(subsidie, maand):
    count_subs = 0
    jaar = maand // 12

    if maand % 12 == 0:
        if jaar in subsidiepot:
            print("Volle pot")
            beschikbaar_bedrag = subsidiepot[jaar]
            if beschikbaar_bedrag >= subsidie:
                subsidiepot[jaar] -= subsidie
                count_subs += 1
                return True
        
            else:
                print("Potje is op")
                print(jaar)
                return False
    

        else:
            return False
    else:
        return False




