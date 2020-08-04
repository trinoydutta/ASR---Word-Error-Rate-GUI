
import numpy

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d

def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0: 
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]

def alignedPrint(list, r, h, result):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    print("REF:", end=" ")
    out = []
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(" "*(len(h[index])), end=" ")
            out.append([" "*(len(h[index])) + ' '])
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print(r[index1] + " " * (len(h[index2])-len(r[index1])), end=" ")
                out.append([r[index1] + " " * (len(h[index2])-len(r[index1])) + ' '])
            else:
                print(r[index1], end=" "),
                out.append([r[index1]+" "])
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(r[index], end=" "),
            out.append([r[index]+" "])
    print("\nHYP:", end=" ")
    out1=[]
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
            out1.append([" " * (len(r[index])) + " "])
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print(h[index2] + " " * (len(r[index1])-len(h[index2])), end=" ")
                out1.append([h[index2] + " " * (len(r[index1])-len(h[index2])) + " "])
            else:
                print(h[index2], end=" ")
                out1.append([h[index2] + " "])
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(h[index], end=" ")
            out1.append([h[index] + " "])
    print("\nEVA:", end=" ")
    out2 = []
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(r[index])-1), end=" ")
            out2.append(["D" + " " * (len(r[index])-1) + " "])
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(h[index])-1), end=" ")
            out2.append(["I" + " " * (len(h[index])-1) + " "])
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print("S" + " " * (len(r[index1])-1), end=" ")
                out2.append(["S" + " " * (len(r[index1])-1) + " "])
            else:
                print("S" + " " * (len(h[index2])-1), end=" ")
                out2.append(["S" + " " * (len(h[index2])-1) + " "])
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
            out2.append([" " * (len(r[index])) + " "])
    print("\nWER: " + result)

    return out , out1, out2

def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """
    # build the matrix
    d = editDistance(r, h)

    # find out the manipulation steps
    list = getStepList(r, h, d)

    # print the result in aligned way
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"
    A_r, A_h, A_eva = alignedPrint(list, r, h, result)
    return result, A_r, A_h, A_eva


import PySimpleGUI as sg
import asr_evaluation

sg.theme('Light Blue 2')

leftcol = [[sg.Text('Ground Truth' , size=(35, 1),font=('Helvetica', 20))],
          [sg.Text('Enter Ground Truth', size=(35, 1),font=('Arial', 16),justification='left')],
          [sg.In(default_text='', size=(100, 1),font=('Times New Roman', 14))],
          #[sg.Text('Ground Truth File (.txt)',size=(16, 1),justification='left'),sg.In(), sg.FileBrowse()],
          [sg.Text('Ground Truth Entered', size=(35, 1),font=('Arial', 16),justification='left')],
          [sg.Text('', size=(100, 1),font=("Times New Roman", 14,"italic"), justification='left',key = 'gt')]]   
          

rightcol = [[sg.Text('Hypothesis',  size=(35, 1),font=('Helvetica', 20))],
           [sg.Text('Enter Hypothesis', size=(35, 1),font=('Arial', 16),justification='left')],
           [sg.In(default_text='', size=(100, 1),font=('Times New Roman', 14))],
           #[sg.Text('Hypothesis File (.txt)', size=(16, 1),justification='left'),sg.In(), sg.FileBrowse()],
           [sg.Text('Hypothesis Entered', size=(35, 1),font=('Arial', 16),justification='left')],
           [sg.Text('', size=(100, 1),font=("Times New Roman", 14,"italic"),justification='left',key = 'h')]]

layout = [[sg.Column(leftcol, element_justification='l')],
          [sg.Column(rightcol, element_justification='l')],
          [sg.Text('_'  * 100)],
          [sg.Button('Load'),sg.Button("Calculate"), sg.Button("Close")],
          #[sg.Text("Word Error Rate : ",justification='left')],
          [sg.Text("Word Error Rate : ",size = (15,1),justification='right'),sg.Text("",size=(80, 1),justification='left',key = 'wer')],
          [sg.Text("Reference : ",size = (15,1),justification='right'),sg.Text(" ",size=(80, 1),font = ("courier"),justification='left',key = 'r1')],
          [sg.Text("Hypothesis : ",size = (15,1),justification='right'),sg.Text(" ",size=(80, 1),font = ("courier"),justification='left',key = 'h1')],
          [sg.Text("EVA : ",size = (15,1),justification='right'), sg.Text(" ",size=(80, 1),font = ("courier"),justification='left',key = 'eva1')]]

window = sg.Window('Word Error Rate', layout)

while True:
    event, values = window.read()
    
    if event == "Load":         
        window['gt'].update(values[0])  
        window['h'].update(values[1])              

    elif event == sg.WIN_CLOSED or event == 'Close':
        print("Cancelled")
        break
    else:
        if __name__ == '__main__':
    
            r = values[0]
            h = values[1]
            ans1, ans2, ans3, ans4 = wer(r, h) 

        
        ans2 = " ".join([" ".join(e) for e in ans2])
        ans3 = " ".join([" ".join(e) for e in ans3])
        ans4 = " ".join([" ".join(e) for e in ans4])
        print(len(ans2),len(ans3),len(ans4))
        window['wer'].update(ans1)
        window['r1'].update(ans2)
        window['h1'].update(ans3)
        window['eva1'].update(ans4)


#pyinstaller --hidden-import=pkg_resources.py2_warn --onefile --noconsole Word_Error_Rate.py


   
   