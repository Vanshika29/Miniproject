import cv2
import numpy as np
import PySimpleGUI as sg
import scipy.io.wavfile as sc

class Decode():
    
    def __init__(self):
        sg.ChangeLookAndFeel('GreenTan')
        layout = [
            [sg.Text('   Choose the type of Steganography!', font=("Helvetica", 25),auto_size_text=True)],
            [sg.Text(' '  * 25),
            sg.Radio('IMAGE', "RADIO1",auto_size_text=True,size = (15,1),font=("Helvetica", 15)),
            sg.Radio('AUDIO', "RADIO1",size = (20,1),auto_size_text=True,font=("Helvetica", 15))],
            [sg.Text('Main File', size=(10, 1), auto_size_text=False, justification='centre'),
            sg.InputText('Main File',size=(40,1),do_not_clear=True, key='_IN1_'),sg.FileBrowse(size=(20,1))],
            [sg.Text('Key', size=(10, 1),justification='centre'),
            sg.InputText('Must be integer', size=(40,1),do_not_clear=True, key='_IN2_')],
            [sg.Text('_'  * 82)],
            [sg.Text(' '  * 50),sg.Submit("Decode"), sg.Cancel()]
        ]

        window = sg.Window('Decoder', default_element_size=(80,5)).Layout(layout)
        while True:
            event, values = window.Read()
            if event is None or event == 'Cancel':      
                break
            elif event == 'Decode':
                if values["_IN1_"] != None and values["_IN1_"]!= "Main File" or values["_IN2_"] != None and values["_IN2_"] != "Message":
                    if values[0] == True:
                        k = self.decode_text_in_img(values["_IN1_"],values["_IN2_"])
                        sg.Window("Congratulations").Layout(sg.Popup("Message has been Decoded \n"+k+" is the message."))
                    elif values[1] == True:
                        k = self.decode_text_in_wave(values["_IN1_"],values["_IN2_"])    
                        sg.Popup("Message has been Decoded \n"+k+" is the message.")
                print(values) 

            window.Close()


    def to_bin(self,string):
        res = ''
        for char in string:
            tmp = bin(ord(char))[2:]
            tmp = '%08d' %int(tmp)
            res += tmp
        return res

    def to_str(self,string):
        res = ''
        for idx in range(int(len(string)/8)):
            tmp = chr(int(string[idx*8:(idx+1)*8], 2))
            res += tmp
        return res

    def decode_text_in_img(self,file,key):
        main_img = cv2.imread(file)
        bitstream = ""
        key = int(key)
        size = np.shape(main_img)
        row = size[0]
        column = size[1]
        k = 0
        r = -3
        c = -1
        for i in range(key*8):
            k = i%3
            if k == 0:
                c += 1
                if c >= 0:
                    c = c%column
            if c == 0:
                r += 1
                if r >= 0:
                    r = r%row
            if main_img[r,c,k]%2==0:
                bitstream += "0"
            elif main_img[r,c,k]%2==1:
                bitstream += "1"
        
        string = self.to_str(bitstream)
        return string

    def decode_text_in_wave(self,file,key):
        wav = sc.read(file)
        ampvals = wav[1]
        bitstream = ""
        key = int(key)
        for i in range(key*8):
            if ampvals[i]%2==0:
                bitstream+="0"
            elif ampvals[i]%2==1:
                bitstream+="1"
        string = self.to_str(bitstream)
        return string

obj = Decode()