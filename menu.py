#Christopher García 20541 
#Isabel Solano 20504
#Gabriel Vicente 20498
#Jessica Ortiz 20192
#Algoritmos y estructura de datos CC2003
#Sección 10

def Vacio(campo):
    while campo == None or campo == "" or campo.isspace():
        campo = input('No se puede dejar un campo vacío: ')
    return campo

def no_option(Verificacion):
    print ('La opción que ingresó no existe')
    Verificacion = False
    
print('______________________-----------------------------------______________________')
print('______________________----------Sistema ChrIGaJ----------______________________')
print('______________________-----------------------------------______________________')

Verificador = False
Palabra_clave = ''

while Verificador != True:
    try:
        print ('Elija la accion que desea hacer con la base de datos creada')
        print ('   Elegir juego ...')
        print ('1) Por Tipo / Genero')
        print ('2) Por Compania')
        print ('3) Por Tipo / Genero')
        print ('4) Online')
        print ('5) Offline')
        print ('6) Ser Multiplayer')
        print ('7) Ser Singleplayer')
        print ('   Otras opciones ...')
        print ('8) Agregar relacion')
        print ('9) Quitar relacion')
        print ('10) Salir')
        print ()
        
        Menu = int(input('Ingrese una opción: '))
            
        if Menu == 1:
            try:
                print ('Que genero desea?')
                print ('1) FPS')
                print ('2) ARPG')
                print ('3) MOBA')
                print ('4) Mundo abierto')
                print ('5) Carreras')
                print ('6) Party')
                print ('7) Estrategia')
                print ('8) Deportes')
                print ('9) Accion')
                print ('10) Aventura')
                print ('11) Peleas')
                
                genero = int(input('Ingrese una opción: '))
                if genero == 1:
                    Palabra_clave = 'FPS'
                elif genero == 2:
                    Palabra_clave = 'ARPG'
                elif genero == 3:
                    Palabra_clave = 'MOBA'
                elif genero == 4:
                    Palabra_clave = 'Mundo abierto'
                elif genero == 5:
                    Palabra_clave = 'Carreras'
                elif genero == 6:
                    Palabra_clave = 'Party'
                elif genero == 7:
                    Palabra_clave = 'Estrategia'
                elif genero == 8:
                    Palabra_clave = 'Deportes'
                elif genero == 9:
                    Palabra_clave = 'Accion'
                elif genero == 10:
                    Palabra_clave = 'Aventura'
                elif genero == 11:
                    Palabra_clave = 'Peleas'
                else:
                    print ()
                    print ('Genero no encontrado')
                    print ()
                    no_option(Verificador)
                    Palabra_clave = ''
                #aqui va el metodo
                if Palabra_clave != '':
                    print(Palabra_clave)
                else:
                    print('esto no esta en la base')
                
            except:
                print ('La opción que ingresó no existe')
                print ()
                Verificador = False
            
        elif Menu == 2:
            try:
                print ('Que compania desea?')
                print ('1) Riot Games')
                print ('2) Supercell')
                print ('3) Epic Games')
                print ('4) Nintendo')
                print ('5) miHoyo')
                print ('6) InnerSloth')
                print ('7) Activision')
                print ('8) Mediatonic')
                print ('9) Mojang Studios')
                print ('10) Rockstar Games')
                print ('11) Psyonix')
                print ('12) Electronics Arts')
                
                ceo = int(input('Ingrese una opción: '))
                if ceo == 1:
                    Palabra_clave = 'Riot Games'
                elif ceo == 2:
                    Palabra_clave = 'Supercell'
                elif ceo == 3:
                    Palabra_clave = 'Epic Games'
                elif ceo == 4:
                    Palabra_clave = 'Nintendo'
                elif ceo == 5:
                    Palabra_clave = 'miHoyo'
                elif ceo == 6:
                    Palabra_clave = 'InnerSloth'
                elif ceo == 7:
                    Palabra_clave = 'Activision'
                elif ceo == 8:
                    Palabra_clave = 'Mediatonic'
                elif ceo == 9:
                    Palabra_clave = 'Mojang Studios'
                elif ceo == 10:
                    Palabra_clave = 'Rockstar Games'
                elif ceo == 11:
                    Palabra_clave = 'Psyonix'
                elif ceo == 12:
                    Palabra_clave = 'Electronics Arts'
                else:
                    print ()
                    print ('Compania no encontrado')
                    print ()
                    no_option(Verificador)
                    Palabra_clave = ''
                #aqui va el metodo
                if Palabra_clave != '':
                    print(Palabra_clave)
                else:
                    print('esto no esta en la base')
                
            except:
                print ('La opción que ingresó no existe')
                print ()
                Verificador = False
            
        elif Menu == 3:
            try:
                print ('En que dispositivo?')
                print ('1) Playstation 4-5')
                print ('2) Xbox One S-Series X')
                print ('3) Android/IOS')
                print ('4) PC')
                print ('5) Nintendo Switch')

                
                disp = int(input('Ingrese una opción: '))
                if disp == 1:
                    Palabra_clave = 'Playstation 4-5'
                elif disp == 2:
                    Palabra_clave = 'Xbox One S-Series X'
                elif disp == 3:
                    Palabra_clave = 'Android/IOS'
                elif disp == 4:
                    Palabra_clave = 'PC'
                elif disp == 5:
                    Palabra_clave = 'Nintendo Switch'
                else:
                    print ()
                    print ('Dispositivo no encontrado')
                    print ()
                    no_option(Verificador)
                    Palabra_clave = ''
                    
                #aqui va el metodo
                if Palabra_clave != '':
                    print(Palabra_clave)
                else:
                    print('esto no esta en la base')
                
            except:
                print ('La opción que ingresó no existe')
                print ()
                Verificador = False
            
            Verificador = False
            
        elif Menu == 4:
            Palabra_clave = 'Online'
            #metodo aqui
            print(Palabra_clave)
            
            Verificador = False
        
        elif Menu == 5:
            Palabra_clave = 'Offline'
            #metodo aqui
            print(Palabra_clave)
            
            Verificador = False
            
        elif Menu == 6:
            Palabra_clave = 'Multiplayer'
            #metodo aqui
            print(Palabra_clave)
            
            Verificador = False
        elif Menu == 7:
            Palabra_clave = 'Singleplayer'
            #metodo aqui
            print(Palabra_clave)
            
            Verificador = False
        elif Menu == 8:
            print('esta es la opcion de crear relacion')
            
            Verificador = False
        elif Menu == 9:
            print('esta es la opcion de eliminar')
            
            Verificador = False
        elif Menu == 10:
            print ('Adios!')
            Verificador = True

        else:
            print ()
            print ('La opción que ingresó no existe')
            print ()
            no_option(Verificador)        
    except:
        print ('La opción que ingresó no existe')
        print ()
        Verificador = False