# This python scrip is the libery for python
# SIMON LE BERRE
# 21/08/2023
# pip install ilo
version = "0.13"
#-----------------------------------------------------------------------------

print("ilo robot library version ", version)
print("For any help or support contact us on our website, ilorobot.com ")
print(" ")

#-----------------------------------------------------------------------------
import socket,time,keyboard #,sys

#-----------------------------------------------------------------------------
'''
if 'ilo' in sys.modules:
    print ('ilo library is already imported')
else:    
    print('ilo library is importing ...')
'''    

global IP,Port,s,preview_stop,connect
IP = '192.168.4.1'
preview_stop = True
connect = False

#-------------------------------------------------------------------------
def info():
    print("Ilo robot is an education robot controlable by direct python command")
    print("To know every fonction available with ilo,  use ilo.list_function() command")
    print("You are using the version ", version)

def list_function():
    print("info()                                        -> print info about ilorobot")
    print(" ")
    print("connection()                                  -> connection your machine to ilorobot")
    print(" ")
    print("step(direction)                               -> move by step ilorobot with selected direction during 2 seconds")
    print("                                                 direction is a string and should be (front, back, left, right, rot_trigo or rot_clock)")
    print(" ")
    print("move(direction, speed, time)                  -> move ilorobot with selected direction speed and time control")
    print("                                                 direction is a string and should be (front, back, left or right)")
    print("                                                 speed is an integer from 0 to 100 as a pourcentage ")
    print(" ")
    print("direct_contol(axial, radial, rotation, stop)) -> control ilorobot with full control ")
    print("                                                 axial, radial and roation are 3 integer from 0 to 255")
    print("                                                 value from 0 to 128 are negative, value from 128 to 255 are positve")
    print("                                                 stop is a boolean value, to don't stop after the command the robot use stop==False")                                
    print(" ")
    print("calculatrice(ilo_calcul)                      -> ilo will execute your calculus, ilo_calcul is a string")
    print("                                                 example of calcul: '3+2-1.5' ")
    print(" ")
    print("list_order(ilo_list)                          -> ilo will execute a list of displacment define my your ilo_list")
    print("                                                 example of list ['front', 'left', 'front', 'rot_trigo', 'back'] ")
    print("                                                 value of ilo_list are a string")
    print(" ")
    print("game()                                        -> control ilo using arrow or numb pad of your keyboard")
    print("                                                 avaible keyboard touch: 8,2,4,6,1,3   space = stop    esc = quit")
    print(" ")
    print("detection()                                   -> return list of state captor as [capteur_front, capteur_back, capteur_left, capteur_right]")
    print(" ")

#-----------------------------------------------------------------------------
def socket_send(msg):
    #print(msg)
    global s, IP, Port, connect
    try:
        s = socket.socket()
        s.connect((IP, Port))
        s.send(msg.encode())
        time.sleep(0.1)           #  10Hz
        return True
    except:
        print('Error of connection with ilo')
        connect = False
        return False
    
#-----------------------------------------------------------------------------
def connection():
    # idea of improvement, be able to connect to witch ilo you want function of is name, or color
    global IP,Port,connect, preview_stop,deviceIP
    preview_stop = True
    
    if connect == True:
        print('ilo already connected')
        return None
    
    else:
        print('Connecting...')
        try:
            Port = 80
            ping = socket.socket()
            ping.connect((IP, Port))         
            deviceIP = ping.getsockname()[0]     # IP of the machine
            #print('deviceIP', deviceIP)
            msg="ilo"
            ping.send(msg.encode())
            ping.close()
    
            inform = socket.socket()
            inform.bind((deviceIP, Port)) 

            time.sleep(1)
    
            s = socket.socket() 
            msg="io"
            s.connect((IP, Port))
            s.send(msg.encode())
            print('Connected to ilo')
            
            time.sleep(1)
        except:
            print("Error connection: you have to be connect to the ilo wifi network")
            print(" --> If the disfonction continu, switch off and switch on ilo")

#-----------------------------------------------------------------------------
def stop():
    socket_send("io")
    time.sleep(0.1)

def test_connection():
    return socket_send("io")
#------------------------------------------- ---------------------------------
def step(direction):
    
    #ilo.step('front')
    
    if isinstance(direction, str) == False:
        print ('direction should be an string as front, back, left, rot_trigo, rot_clock','stop')
        return None
    
    if direction == 'front':
        socket_send("iavpx110yro")
    elif direction == 'back':
        socket_send("iavpx010yro")
    elif direction == 'left':
        socket_send("iavpxy010ro")
    elif direction == 'right':
        socket_send("iavpxy110ro")
    elif direction == 'rot_trigo':
        socket_send("iavpxyr090o")
    elif direction == 'rot_clock':
        socket_send("iavpxyr190o")
    elif direction == 'stop':
        stop()
    else:
        print('direction name is not correct')
    
#-----------------------------------------------------------------------------
def list_order(ilo_list):
    
    if isinstance(ilo_list, list) == False:
        print ('the variable should be a list, with inside string as front, back, left, rot_trigo, rot_clock')
        return None

    for i in range(len(ilo_list)):
        step(ilo_list[i])   
        
#------------------------------------------- ---------------------------------
def correction_command(list_course):
    
    #convert a list of 3 elements to a sendable string
    
    if int(list_course[0]) >= 100:
        list_course[0] = str(list_course[0])   
    elif 100 > int(list_course[0]) >= 10:
        list_course[0] = str('0') + str(list_course[0])
    elif 10 > int(list_course[0]) >= 1:
        list_course[0] = str('00') + str(list_course[0])
    else:
        list_course[0] = str('000')

    if int(list_course[1]) >= 100:
        list_course[1] = str(list_course[1])     
    elif 100 > int(list_course[1]) >= 10:
        list_course[1] = str('0') + str(list_course[1])
    elif 10  > int(list_course[1]) >= 1:
        list_course[1] = str('00') + str(list_course[1])
    else:
        list_course[1] = str('000')
        
    if int(list_course[2]) >= 100:
        list_course[2] = str(list_course[2])     
    elif 100 > int(list_course[2]) >= 10:
        list_course[2] = str('0') + str(list_course[2])
    elif 10  > int(list_course[2]) >= 1:
        list_course[2] = str('00') + str(list_course[2])
    else:
        list_course[2] = str('000')
        
    new_command = []
    str_command = str(list_course[0] + list_course[1] + list_course[2])
    new_command = "iav" + str_command +"pxyro"
    return new_command
    
def move(direction, speed, wait_time):
    
    #ilo.move('front', 50, 3)
    
    #global preview_stop
    #preview_stop = True
    
    if isinstance(direction, str) == False:
        print ('direction should be an string as front, back, left, rot_trigo, rot_clock')
        return None
    if isinstance(speed, int) == False:
        print ('speed should be an integer between 0 to 100')
        return None
    if speed > 100:
        print ('speed should be an integer between 0 to 100')
        return None
    if speed < 0:
        print ('speed should be an integer between 0 to 100')
        return None
    if isinstance(wait_time, int) == False:
        print ('time should be an integer')
        return None

    if direction == 'front':
        command = [int((speed*1.28)+128),128,128]
    elif direction == 'back':
        command = [int(-(speed*1.28))+128,128,128]
    elif direction == 'leftt':
        command = [128,int((speed*1.28)+128),128]
    elif direction == 'right':
        command = [128,int(-(speed*1.28)+128),128]
    elif direction == 'rot_trigo':
        command = [128,128,int((speed*1.28)+128)]
    elif direction == 'rot_clock':
        command = [128,128,int(-(speed*1.28)+128)]
    else:
        print('direction is not correct')
        return None
    
    corrected_command = correction_command(command)
    stop()
    socket_send(corrected_command)
    time.sleep(wait_time)   #have to be avoid, set a chronos starting at this point
    stop()

def direct_control(axial, radial, rotation):

    if isinstance(axial, int) == False:
        print ('axial should be an interger')
        return None
    if axial> 255 or axial<0:
        print ('axial should be include between 0 and 255')
        return None
    if isinstance(radial, int) == False:
        print ('Radial should be an interger')
        return None
    if radial> 255 or radial<0:
        print ('Radial should be include between 0 and 255')
        return None
    if isinstance(rotation, int) == False:
        print ('rotation should be an interger')
        return None
    if rotation> 255 or rotation<0:
        print ('rotation should be include between 0 and 255')
        return None

    command = [axial, radial, rotation]
    corrected_command = correction_command(command)
    socket_send(corrected_command)
    
#-----------------------------------------------------------------------------  
def game():
 
    if test_connection() == True:
        axial_value = 128
        radial_value = 128
        rotation_value = 128
        stop()
        new_keyboard_instruction = False
        
        print('Game mode start, use keyboard arrow to control ilo')
        print("Press echap to leave the game mode")
        
        while (True):
            if keyboard.is_pressed("8"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                axial_value = axial_value + 5
                if axial_value > 255:
                    axial_value = 255     
            elif keyboard.is_pressed("2"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                axial_value = axial_value - 5
                if axial_value < 1:
                    axial_value = 0
            elif keyboard.is_pressed("6"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                radial_value = radial_value + 5
                if radial_value > 255:
                    radial_value = 255  
            elif keyboard.is_pressed("4"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                radial_value = radial_value - 5
                if radial_value < 1:
                    radial_value = 0
            elif keyboard.is_pressed("3"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                rotation_value = rotation_value + 5
                if rotation_value > 255:
                    rotation_value = 255  
            elif keyboard.is_pressed("1"):
                new_keyboard_instruction = True
                time.sleep(0.05)
                rotation_value = rotation_value - 5
                if rotation_value < 1:
                    rotation_value = 0  
            elif keyboard.is_pressed("space"):
                stop
                axial_value = 128
                radial_value = 128
                rotation_value = 128
            elif keyboard.is_pressed("esc"):
                stop()
                break
            
            if new_keyboard_instruction == True:
                direct_control(axial_value, radial_value, rotation_value)
                new_keyboard_instruction = False
    else:
        print("You have to be connected to ILO before play with it, use ilo.connection()")

#-----------------------------------------------------------------------------        
def get_distance():
    # return 
    pass

def get_led_color():
    pass

def set_led_color(color):
    pass

def get_color_floor(position):
    #position = rigth, left, center
    pass

def get_acceleration():
    pass

def set_acceleration(acc):
    pass

def get_vmax():
    pass

def set_vmax(vmax):
    pass
        
            