import cv2
import numpy as np
import PySimpleGUI as sg
import scipy.io.wavfile as sc

class Encode():
    
    def __init__(self):
        sg.ChangeLookAndFeel('GreenTan')
        layout = [
            [sg.Text('   Choose the type of Steganography!', font=("Helvetica", 25),auto_size_text=True)],
            [sg.Text(' '  * 25),
            sg.Radio('IMAGE', "RADIO1",auto_size_text=True,size = (15,1),font=("Helvetica", 15)),
            sg.Radio('AUDIO', "RADIO1",size = (20,1),auto_size_text=True,font=("Helvetica", 15))],
            [sg.Text('Main File', size=(10, 1), auto_size_text=False, justification='centre'),
            sg.InputText('Main File',size=(40,1),do_not_clear=True, key='_IN1_'),sg.FileBrowse(size=(20,1))],
            [sg.Text('Message', size=(10, 1),justification='centre'),
            sg.InputText('Message', size=(40,1),do_not_clear=True, key='_IN2_'),sg.FileBrowse(size=(20,1))],
            [sg.Text('_'  * 82)],
            [sg.Text(' '  * 50),sg.Submit("Encode"), sg.Cancel()]
            ]
        window = sg.Window('Encoder', default_element_size=(80,5)).Layout(layout)
        while True:
            event, values = window.Read()
            if event is None or event == 'Cancel':      
                break
            elif event == 'Encode':
                if values["_IN1_"] != None and values["_IN1_"]!= "Main File" or values["_IN2_"] != None and values["_IN2_"] != "Message":
                    if values[0] == True:
                        k = self.encode_text_in_img(values["_IN1_"],values["_IN2_"])
                        sg.Popup("Message has been encoded \n"+str(k)+" is the key.")
                    elif values[1] == True:
                        k = self.encode_text_in_wave(values["_IN1_"],values["_IN2_"])    
                        sg.Popup("Message has been encoded \n"+str(k)+" is the key.")
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
        for idx in range(len(string)/8):
            tmp = chr(int(string[idx*8:(idx+1)*8], 2))
            res += tmp
        return res

    def encode_text_in_img(self,mainfile,text):
        main_img = cv2.imread(mainfile)
        bitstream = self.to_bin(text)
        size = np.shape(main_img)
        row = size[0]
        column = size[1]
        k = 0
        r = -3
        c = -1
        key = int(len(bitstream)/8)
        for i in range(len(bitstream)):
            k = i%3
            if k == 0:
                c += 1
                if c >= 0:
                    c = c%column
            if c == 0:
                r += 1
                if r >= 0:
                    r = r%row
            if main_img[r,c,k]%2 == 0 and bitstream[i] == "1":
                main_img[r,c,k] += 1
            
            elif main_img[r,c,k]%2 == 1 and bitstream[i] == "0":
                main_img[r,c,k] -= 1
        cv2.imwrite("outputfile.png",main_img)
        while (1):
            cv2.imshow("outputfile.png",main_img)
            k = cv2.waitKey(33)
            if k==27:           
                cv2.destroyAllWindows()       
                break
        return key

    def encode_text_in_wave(self,file,text):
        wav = sc.read(file)
        ampvals = wav[1]
        bitstream = self.to_bin(text)
        key = len(text)
        for i in range(len(bitstream)):
            if ampvals[i]%2==1 and bitstream[i] == "0":
                ampvals[i] += 1
            elif ampvals[i]%2==0 and bitstream[i] == "1":
                ampvals[i] += 1
        sc.write("outputwav.wav",wav[0],ampvals)
        return key
        
              
    
obj = Encode()

        
        
        
