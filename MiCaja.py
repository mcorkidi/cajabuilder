 # -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:08:30 2018

@author: Corkidi

to do: fix scroll when entering long caja to see entries
to do: fix currency formating throughout
to do: fix mail password security,* and encryption on save

"""

from tkinter import *
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
import csv
from prettytable import PrettyTable
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import arrow
import pickle
import os

mb = [] #list used for cta and abono in to enter into money, temporary
recibos = 0 #variable for incremental recibos entry
caja = [] #list that builds caja report
totalRec = 0.0
totalDep = 0.0
totalDif = 0.0
depositos = []    #  list o f depositos
lblList = []
window = Tk() #tkinter window instance
window.title("Epcot Caja Builder")
window.geometry('1200x600')
t = PrettyTable(['Cuenta', 'Cliente', 'Abono', 'Recibo'])
t.title = 'Caja'
t1 = PrettyTable(['Banco', 'Fecha', 'Monto'])
t.title = 'Recibos'
tableGastos = PrettyTable(['Descripcion', 'Monto'])
tableGastos.title = 'Gastos'


#load account numbers and client names into new directory from csv file
lista_file = 'clientes.csv'

def loadClientes():
    try:
        reader = csv.reader(open(lista_file, 'r'))
        d = {}  #empty dictionary
        for row in reader: 
           k, v = row
           d[k] = v
        return d
        reader.close()
    except:
        messagebox.showwarning('Error', 'Tu lista de clientes no fue cargada.')

clt = loadClientes()

def quit1():  #function for quiting using menu
    window.destroy()

def listaClientes():  #menu item to manage client list
    cwin = Tk()
    cwin.title('Lista de Clientes')
    cwin.geometry('300x400')
    listbox = Listbox(cwin)
    listbox.pack(side="left", fill="both", expand=True)
    listbox.insert(END, "Lista de Clientes")
    for item in clt:
        listbox.insert(END, item + ' : ' + clt[item])
   
def ingRec(event=None):  #function for pressing button Enter
    global recibos
    global money
    global totalRec
    global totalDif
    try:
        recibos = int(recibo.get()) 
        m = cta.get()  #get cuenta from entry box 
        if m == '':
            raise
        checkForNil(money)
        b = money.get()  #get money from entry box
        mb = [] #reset mb to create new entry
        mb.append(m)  #enter cuenta to mb which is list for caja
        mb.append(clt[m])
        mb.append(b)
        mb.append(recibos)
        caja.append(mb) #caja is a list of 4 parameters cta name money recibo
        recibos += 1
        recibo.delete(0, END)
        cta.delete(0, END)
        money.delete(0, END)
        recibo.insert(10, str(recibos))
        lblCta['text']='       '
        totalRec += float(b)
        displayCaja(caja)
        totalDif = totalRec - totalDep
        var2.set('Diferencia: $'+ str(totalDif))
        cta.focus()
    except:
        messagebox.showwarning('Error', 'Dato invalido ingresado.')
    
#function ingresar depositos
def ingDep(event=None):
    global depositos
    global totalDep
    global totalDif
    global totalRec
    depTemp = []
    try:
        f = fecha.get()
        b = banco.get()
        m = monto.get() 
        if m == '':
            raise
        depTemp.append(f)
        depTemp.append(b)
        depTemp.append(m)
        depositos.append(depTemp)
        totalDep += float(m)
        totalDif = totalRec - totalDep
        displayDep(depositos)    
        banco.delete(0, END)
        monto.delete(0, END)
        fecha.delete(0, END)
        fecha.focus()
    except:
        messagebox.showwarning('Error', 'Dato invalido ingresado.')
#function to display depositos

var1 = StringVar() 
var2 = StringVar()
def displayDep(d):   

    global totalDep
    global lblTotalDep
    global totalDif
    r1 = 3       
    for i in range(len(d)):
       for j in range(3):
            col = j +5 
            j = Label(frameDepositos, text=str(d[i][j]))
            j.grid(column=col, row=r1)
            lblList.append(j)
       r1+=1   
    var1.set('Total: $' + str(totalDep))  #variable for total line variable text
    lblTotDep.grid(column=7, row=r1+1)   #moves the total line downward    
    var2.set('Diferencia: $'+ str(round(totalDif, 2)))    
    lblDif.grid(column=7, row=r1+2)
        
#function to build labels showing caja report
var = StringVar()       
def displayCaja(caja):
    global totalRec
    global lblTotalRec
    ro = 3 #row counter for displaying caja     
    for i in range(len(caja)):
       for j in range(4):
            col = j
            j = Label(frameRecibos, text=str(caja[i][j]))
            j.grid(column=col, row=ro)
            lblList.append(j)          
       ro+=1            #row counter for total line
    var.set('Total: $' + str(totalRec))  #variable for total line variable text
    lblTotRec.grid(column=2, row=ro)   #moves the total line downward

#function to check if client is in CSV if not, creat it 
def checkCta(event): 
    global clt 
    try: 
        m = cta.get()
        lblCta['text'] = clt[m]
    except:        
        clienteNew = Toplevel(window)
        clienteNew.title("Cliente Nuevo")
        clienteNew.geometry('600x250')
        newC = Label(clienteNew, text ='Tu cliente no esta registrado. Aqui lo puedes crear.')
        newC.grid(column=0, row = 0)
        newCta = Entry(clienteNew, width=10)
        newCta.grid(column=0, row=2)
        newCta.insert(0, m)
        def on_entry_click(event):
            """function that gets called whenever entry is clicked"""
            if newName.get() == 'Ingresa el nombre del cliente':
               newName.selection_range(0, END) # delete all the text in the entry               
               newName.config(fg = 'black')
        def on_focusout(event):
            if newName.get() == '':
                newName.insert(0, 'Ingresa el nombre del cliente')
                newName.config(fg = 'grey')    
        def newClient():  #function to create new client and enter it to csv for later use
            j=''
            x = newName.get()
            y = newCta.get()
            clt[y]=x  #insert new client to dict
            lblCta['text'] = x
            j=y+','+x + '\n' 
            with open(lista_file,'a') as f:
                f.write(j)
                f.close()
            clienteNew.destroy()
        newName = Entry(clienteNew, width=30)
        newName.grid(column=1, row=2)
        newName.insert(0, 'Ingresa el nombre del cliente')
        newName.config(fg = 'grey')
        newName.bind('<FocusIn>', on_entry_click)
        newName.bind('<FocusOut>', on_focusout)
        newName.focus()
        btn3 = Button(clienteNew, text="Enter", command=newClient) #enter new client
        btn3.grid(column=2, row=2)
        btn3.bind('<Return>', newClient)
        def closeWindow():
            clienteNew.destroy()
        btn4 = Button(clienteNew, text="Cancel", command=closeWindow)
        btn4.grid(column=2, row=3)
    money.focus()

def emailMe():
    mailStat = Toplevel(window)
    mailStat.title("Email Status")
    mailStat.geometry('180x180')
    status = Label(mailStat, text ='Enviando tu Caja.')
    status.grid(column=0, row=0)
    def closeWindow():
        mailStat.destroy()
    try:
        with open('config.dat', 'rb') as f:
            outgoingServer, port, myEmail, outgoingEmail, myPassword = pickle.load(f)
        
    #    html = t.get_html_string() + '\n' + t1.get_html_string()
        text = buildTable()
        part1 = MIMEText(text, 'plain')
    #    part2 = MIMEText(html, 'html')
        user = myEmail 
        password = myPassword
        message = MIMEMultipart()
        message['From'] = myEmail
        message['To'] = outgoingEmail 
        message['Subject'] = 'Caja'
        message.attach(part1)
    #    message.attach(part2)        
        server = smtplib.SMTP_SSL(outgoingServer, port)
        server.ehlo()
        connected = Label(mailStat, text ='Coneccion establecida.')
        connected.grid(column=0, row=1)
        server.login(user, password)         
        server.sendmail(user, outgoingEmail, message.as_string())       
        server.quit()
        sentMail=Label(mailStat, text='Caja enviada correctamente. \n' + outgoingEmail )        
        sentMail.grid(column=0, row=2) 
        mailOk = Button(mailStat, text="OK", command=closeWindow)
        mailOk.grid(column=0, row=4)
    except:
        errorMail=Label(mailStat, text='Error, contacta a tu administrador.')
        errorMail.grid(column=0, row=3)        
        mailOk = Button(mailStat, text="OK", command=closeWindow)
        mailOk.grid(column=0, row=4)
            
def buildTable():
    global totalRec
    global totalDep
    global nombre
    global pais
    global dateTrip
    t.clear_rows()
    for i in range(len(caja)): #build table for Recibos
        t.add_row([caja[i][0],caja[i][1], caja[i][2], caja[i][3]])        
    t.add_row(['--','--', '--', '--'])
    t.add_row(['','Total', totalRec, ''])
    t1.clear_rows()             #build table for depositos
    for j in range(len(depositos)):
        t1.add_row([depositos[j][1], depositos[j][0], depositos[j][2]])
    t1.add_row(['--','--', '--'])
    t1.add_row(['','Total', totalDep])
    return nombre + '\n' + str(pais) + '\n' + str(dateTrip) + '\n' + 'Recibos'+ '\n' \
            + t.get_string() + '\n' + 'Depositos'+ '\n' +  t1.get_string()
    
def buildTableGasto():
    global nombre
    global pais
    global dateTrip
    global fondosAmountsList
    tableGastos.clear_rows() 
    for g in range(len(gastosAmounts)):  #build table for gastos by get from the entries
        if gastosAmounts[g].get() != '':
            if float(gastosAmounts[g].get()) > 0:            
                tableGastos.add_row([listGastoDesc[g].get(), gastosAmounts[g].get()])
    tableGastos.add_row(['--', '--'])
    tableGastos.add_row(['Total: ', totalGastos])
    return  nombre + '\n' + str(pais) + '\n' + str(dateTrip) + '\n' + 'Gastos'+ '\n'\
             + 'Fondos Epcot: ' + fondosAmountsList[0].get() + '\n' + 'Fondos Cobros: ' + \
             fondosAmountsList[1].get() + '\n' +  tableGastos.get_string()
    
def resetAll():
    if messagebox.askyesno("Reiniciar Caja", "Quieres borrar toda la caja?"):
        for label in lblList:
            label.destroy()    
        global mb
        global recibos
        global caja
        global totalRec
        global totalDep
        global totalDif
        global depositos
        global r
        global totalGastos
        totalGastos = 0.0
        r = 6
        mb = [] #list used for cta and abono in to enter into money, temporary
        recibos = 0 #variable for incremental recibos entry
        caja = [] #list that builds caja report
        totalRec = 0.0
        totalDep = 0.0
        totalDif = 0.0
        depositos = []    #  list of depositos
        var.set('Total: $0')  #variable for total line variable text
        var1.set('Total: $0')  #variable for total line variable text
        var2.set('Diferencia: $0')  
        recibo.delete(0,END)
#        for i in range(len(gastosAmounts)):
#            gastosAmounts[i].delete(0, END)
        buildGastosEntry(700, 0, commonGastos,u)
        var3.set('')
        var4.set('')
    else:     #happens when reset all is canceled.
        return 1  

def editRecDisp(): #editar recibos func
    editRecWin = Toplevel(window)
    editRecWin.title("Editar Recibos")
    editRecWin.geometry('800x500')
    editLbl = Label(editRecWin, text='Edicion de Caja')
    editLbl.grid(column=0, row=0)
    editLbl1 = Label(editRecWin, text='CTA')
    editLbl1.grid(column=0, row=1)
    editLbl2 = Label(editRecWin, text='CLIENTE')
    editLbl2.grid(column=1, row=1)
    editLbl3 = Label(editRecWin, text='ABONO')
    editLbl3.grid(column=2, row=1)
    editLbl4 = Label(editRecWin, text='RECIBO')
    editLbl4.grid(column=3, row=1)
    def editRec():
        global totalRec
        global totalDif
        totalRec = 0
        for i in range(len(caja)):
            for j in range(4):
                caja[i][j]=editEntryList[i][j].get()
                if j == 2:
                    totalRec+=float(editEntryList[i][j].get())
        for label in lblList:
            label.destroy() 
        totalDif = totalRec - totalDep
        displayCaja(caja)
        displayDep(depositos)        
        editRecWin.destroy()        
    r=2
    editEntryList =[]
    for i in range(len(caja)): #loop for creating entry boxes and buttons on edit
        tempEntry=[]
        for j in range(4):          
           m = str(caja[i][j])
           jf = Entry(editRecWin, width=25)
           jf.insert(0, m)                    
           jf.grid(column=j, row=r)
           tempEntry.append(jf)
           delButton = Button(editRecWin, text= 'x', command = lambda: deleteLine\
                              (i, caja, editRecWin, editRecDisp))
           delButton.grid(column = 4, row = r)
        r+=1
        editEntryList.append(tempEntry)
    jb = Button(editRecWin, text='Enter', command=editRec)     
    jb.grid(column=4, row=r)

def editDepDisp(): #editar depositos    
    editDepWin = Toplevel(window)
    editDepWin.title("Editar Depositos")
    editDepWin.geometry('550x400')
    editLbl = Label(editDepWin, text='Edicion de Depositos')
    editLbl.grid(column=0, row=0)
    editLbl1 = Label(editDepWin, text='FECHA')
    editLbl1.grid(column=0, row=1)
    editLbl2 = Label(editDepWin, text='BANCO')
    editLbl2.grid(column=1, row=1)
    editLbl3 = Label(editDepWin, text='MONTO')
    editLbl3.grid(column=2, row=1)
    editEntryList =[]
    def editDep():
        global totalDep
        global totalDif
        totalDep = 0
        for i in range(len(depositos)):
            for j in range(3):
                depositos[i][j]=editEntryList[i][j].get()
                if j == 2:
                    totalDep+=float(editEntryList[i][j].get())
        for label in lblList:
            label.destroy() 
        totalDif = totalRec - totalDep
        displayCaja(caja)
        displayDep(depositos)        
        editDepWin.destroy()    
    r=2
    for i in range(len(depositos)): #loop for creating entry boxes and buttons on edit
        tempEntry=[]
        for j in range(3):          
           m = str(depositos[i][j])
           jf = Entry(editDepWin, width=25)
           jf.insert(0, m)                    
           jf.grid(column=j, row=r)
           tempEntry.append(jf)
           delButton = Button(editDepWin, text= 'x', command = lambda: deleteLine\
                              (i, depositos, editDepWin, editDepDisp))
           delButton.grid(column = 3, row = r)
        r+=1
        editEntryList.append(tempEntry)
    jb = Button(editDepWin, text='Enter', command=editDep)     
    jb.grid(column=3, row=r)
    
def deleteLine(i, l, w, f):
    l.pop(i)
    w.destroy()
    f()
  
def enterEmail():   
    enterEmailWin = Toplevel(window)
    enterEmailWin.title("Ingresa tu Correo")
    enterEmailWin.geometry('350x150')
    lbl = Label(enterEmailWin, text='Confirma la direccion de correo para enviar.')
    with open('config.dat', 'rb') as f:
            outgoingServer, port, myEmail, outgoingEmail, myPassword = pickle.load(f)  
    f.close()
    email = Entry(enterEmailWin, width=25)
    email.focus()
    email.insert(0, outgoingEmail)
    def setEmail():
        outgoingEmail = email.get()
        with open('config.dat', 'wb') as f: #write new outgoing email and/or confirm
            pickle.dump((outgoingServer, port, myEmail, outgoingEmail, myPassword), f)
        f.close()        
        emailMe()
        enterEmailWin.destroy()
    btn = Button(enterEmailWin, text='Enter', command=setEmail)
    lbl.pack()
    email.pack()
    btn.pack()

def helpWin():
    helpWinOpen= Toplevel(window)
    helpWinOpen.title('Ayuda')
    helpWinOpen.geometry('400x350')
    lbl = Label(helpWinOpen, text='''Programa creado por: Moises Corkidi \n
Contacto: corkidi@gmail.com \n \n - Primero ingresa el numero de cuenta. \n
- <TAB> o <ENTER> te mostrara el nombre del cliente.\n
- Los numeros de recibo se incrementaran automaticamente. \n
- Puedes crear cuentas y clientes nuevos para uso en el futuro\n
ingresando el numero de CTA y apretando <Enter> o <TAB>\n
Te aparecera la ventana para ingresar nuevo nombre y almacenar.\n ''')
    lbl.pack()

outgoingServer = ''
port = 465
myEmail = ''
outgoingEmail = 'default@default.com'
myPassword = ''

    
def configWin():  #configuration window for setting up email account, headers, clients file
    configWindow = Toplevel(window)
    configWindow.title('Configuraciones')
    configWindow.geometry('350x250')
    emailConfigFrame = Frame(configWindow, width = 400, height = 200, bd = 5, relief = RAISED)
    emailConfigFrame.grid(column = 0, row = 0)
    configLbl = Label(emailConfigFrame, text = 'Email Configuration')
    configLbl.grid(column = 0, row = 0)
    
    configLbl1 = Label(emailConfigFrame, text = 'Outgoing eMail Server: ')
    configLbl1.grid(column = 0, row = 1)
    configEntry1 = Entry(emailConfigFrame, width = 30)
    configEntry1.grid(column = 1, row = 1)
    
    configLbl2 = Label(emailConfigFrame, text = 'Port: ')
    configLbl2.grid(column = 0, row = 2)
    configEntry2 = Entry(emailConfigFrame, width = 30)
    configEntry2.grid(column = 1, row = 2)
    
    configLbl3 = Label(emailConfigFrame, text = 'Password: ')
    configLbl3.grid(column = 0, row = 3)
    configEntry3 = Entry(emailConfigFrame, width = 30)
    configEntry3.grid(column = 1, row = 3)
    
    clientConfigFrame = Frame(configWindow, width = 400, height = 200, bd = 5, relief = RAISED)
    clientConfigFrame.grid(column = 0, row = 1)
    
    configLbl4 = Label(clientConfigFrame, text = 'Mi correo: ')
    configLbl4.grid(column = 0, row = 0)
    configEntry4 = Entry(clientConfigFrame, width = 30)
    configEntry4.grid(column = 1, row = 0)    
    
    configLbl5 = Label(clientConfigFrame, text = 'Enviar a: ')
    configLbl5.grid(column = 0, row = 1)
    configEntry5 = Entry(clientConfigFrame, width = 30)
    configEntry5.grid(column = 1, row = 1)    
    
    try:
        with open('config.dat', 'rb') as f:
            outgoingServer, port, myEmail, outgoingEmail, myPassword = pickle.load(f)
        f.close()
        configEntry1.insert(0, outgoingServer)
        configEntry2.insert(0, port)
        configEntry3.insert(0, myPassword)
        configEntry4.insert(0, myEmail)
        configEntry5.insert(0, outgoingEmail)
    except:
        pass
    
    def enterConfig():
        outgoingServer = configEntry1.get()
        port = configEntry2.get()
        myEmail = configEntry4.get()
        outgoingEmail = configEntry5.get()
        myPassword = configEntry3.get()
        with open('config.dat', 'wb') as f:
            pickle.dump((outgoingServer, port, myEmail, outgoingEmail, myPassword), f)
        f.close()
        configWindow.destroy()
    
    enterConfigBtn = Button(clientConfigFrame, text = 'Enter', command = enterConfig)
    enterConfigBtn.grid(row = 4, column = 3, padx = 15, pady = 10)    
    
    
        

nombre = ''
pais = ''
dateTrip = 'Ingresa Fechas de Viaje'    
def headerWin():
    global nombre
    global pais
    headWindow = Toplevel(window)
    headWindow.title('Encabezado')
    headWindow.geometry('400x300')
    headConfigFrame = Frame(headWindow, width = 400, height = 300, bd = 5, relief = SUNKEN)
    headConfigFrame.grid(column = 0, row = 0)
    nameLbl = Label(headConfigFrame, text = 'Nombre: ', padx = 15, pady = 10)
    paisLbl = Label(headConfigFrame, text = 'Pais: ', padx = 15, pady = 10)
    dateLbl = Label(headConfigFrame, text = 'Fecha de viaje: ', padx = 15, pady = 10)
    nameLbl.grid(column = 0, row = 1)
    paisLbl.grid(column = 0, row = 2)
    dateLbl.grid(column = 0, row = 3)
    nameEntry = Entry(headConfigFrame, width = 30)    
    paisEntry = Entry(headConfigFrame, width = 30)
    dateEntry = Entry(headConfigFrame, width = 30)
    nameEntry.grid(column = 1, row = 1, padx = 15, pady = 10)
    paisEntry.grid(column = 1, row = 2, padx = 15, pady = 10)
    dateEntry.grid(column = 1, row = 3, padx = 15, pady = 10)
    try:
        with open('head.dat', 'rb') as f:
            nombre, pais = pickle.load(f)
        nameEntry.insert(0, nombre)
        paisEntry.insert(0, pais) 
        f.close()
    except:
        pass
    def enterHeader():
        global nombre
        global pais
        global dateTrip
        nombre = nameEntry.get()
        pais = paisEntry.get()
        dateTrip = dateEntry.get()
        with open('head.dat', 'wb') as f:
            pickle.dump((nombre,pais), f)
        f.close()
        headWindow.destroy()
    enterHeadBtn = Button(headConfigFrame, text = 'Enter', command = enterHeader)
    enterHeadBtn.grid(row = 4, column = 3, padx = 15, pady = 10)
        
    
name = arrow.now().format('YYYY-MM-DD')
def export():
    with open(name + ' Caja.txt', 'w') as filehandle:        
        filehandle.writelines(buildTable()) 
    with open(name + ' Gasto.txt', 'w') as filehandle:        
        filehandle.writelines(buildTableGasto()) 
        
def save():
    global listGastoDesc
    global gastosAmounts
    gastosList = []
    for g in range(len(gastosAmounts)):  #build table for gastos by get from the entries
        if gastosAmounts[g].get() != '':
            if float(gastosAmounts[g].get()) > 0:            
                gastosList.append([listGastoDesc[g].get(), gastosAmounts[g].get()])
    fileNameSave = filedialog.asksaveasfile(mode='w', defaultextension=".caj")        
    with open(fileNameSave.name, "wb") as f:
        pickle.dump((caja, depositos, gastosList, fondosAmounts), f) 
    f.close()  
     
       
def load():
    global totalDep
    global totalRec
    global totalDif
    global caja
    global depositos
    global r
    global listGastoDesc
    global gastosAmounts
    global fondosAmountsList

    if resetAll() == 1:  #avoid reset all in case load action is canceled
        return
    fileName = filedialog.askopenfilename(title = "Select file",filetypes = (("Caja","*.caj"),("all files","*.*")))
    with open(fileName, 'rb') as f:
        caja, depositos, gastosList, fondosAmounts = pickle.load(f)
    f.close()
    gastosListUnpack = []  #unpack gastosList from Pickle to insert into Gastos
    gastosAmountsUnpack = []
    for j in range(len(gastosList)):
        gastosListUnpack.append(gastosList[j][0])
    for h in range(len(gastosList)):
        gastosAmountsUnpack.append(gastosList[h][1])
    for j in range(len(depositos)):
        totalDep += float(depositos[j][2])
    for r in range(len(caja)):
         totalRec += float(caja[r][2])
    totalDif = totalRec - totalDep
    displayCaja(caja)
    displayDep(depositos)
    for i in range(len(gastosListUnpack)):
        listGastoDesc[i].delete(0, END)
        listGastoDesc[i].insert(0, gastosListUnpack[i])
        gastosAmounts[i].insert(0, gastosAmountsUnpack[i])
    r = len(caja)
    fondosAmountsList[0].delete(0, END)
    fondosAmountsList[1].delete(0, END)
    fondosAmountsList[0].insert(0, fondosAmounts[0])
    fondosAmountsList[1].insert(0, fondosAmounts[1])

    
    
        
def printCaja():
    export()
    os.startfile(name + ' Caja.txt', "print")
    os.startfile(name + ' Gasto.txt', "print")
      
def previewTable(table):    
    previewWin = Tk()
    previewWin.title('Caja Preview')
    previewWin.geometry('600x500')
    report = table
    reportStr = Text(previewWin)
    reportStr.insert(INSERT, report)
    reportStr.pack()

#frames
frameRecibos = Frame(window, width = 500, height = 600, bd = 5, relief = RAISED)
frameRecibos.grid(row = 0, column = 0, sticky = NE, padx = 5)
frameDepositos = Frame(window, width = 500, height = 600, bd = 5, relief = RAISED)
frameDepositos.grid(row = 0, column = 1, sticky = NE, padx = 5)
frameGastos = Frame(window, width = 200, height = 600, bd = 5, relief = RAISED)
frameGastos.grid(row = 0, column = 2, sticky = NE, padx = 5)
  
#menu
menu = Menu(window) 
new_item = Menu(menu)
new_item.add_command(label='Export', command=export)
new_item.add_command(label='Print', command=printCaja)
new_item.add_command(label='Save', command = save)
new_item.add_command(label='Load', command = load)
new_item.add_command(label='Exit', command=quit1)
menu.add_cascade(label='File', menu=new_item)
editItem = Menu(menu)                                   #Edit Menu
menu.add_cascade(label='Edit', menu=editItem)
editItem.add_command(label='Reset', command=resetAll)
editItem.add_command(label='Editar Recibos', command=editRecDisp)
editItem.add_command(label='Editar Depositos', command=editDepDisp)
viewItem = Menu(menu)                     #preview Menu
menu.add_cascade(label='Ver', menu=viewItem)
viewItem.add_command(label='Caja', command=lambda: previewTable(buildTable()))
viewItem.add_command(label='Gasto', command=lambda: previewTable(buildTableGasto()))
viewItem.add_command(label='Clientes', command=listaClientes)
sendItem = Menu(menu)                     #send Menu
menu.add_cascade(label='Enviar', menu=sendItem)
sendItem.add_command(label='Email', command=enterEmail)
configItem = Menu(menu)                     #config menu
menu.add_cascade(label='Config', menu=configItem)
configItem.add_command(label='Config', command=configWin)
configItem.add_command(label='Encabezado', command=headerWin)
ayudaItem = Menu(menu)
menu.add_cascade(label='Ayuda', menu=ayudaItem)
ayudaItem.add_command(label='Ayuda', command=helpWin)
window.config(menu=menu)

#labels for recibos
lblRecibos = Label(frameRecibos, text = 'Recibos', font=("Helvetica", 16, 'underline'))
lblRecibos.grid(column = 1, row = 0)
lblR = Label(frameRecibos, text=" Cliente ")
lblR.grid(column=1, row=1)
lblC = Label(frameRecibos, text="Cta")
lblC.grid(column=0, row=1)
lblA = Label(frameRecibos, text="Abono")
lblA.grid(column=2, row=1)
lblRe = Label(frameRecibos, text="Recibos")
lblRe.grid(column=3, row=1)
lblS = Label(frameRecibos, text="                                           ")
lblS.grid(column=4, row=1)
lblTotRec = Label(frameRecibos, textvariable=var, width=12)        
lblTotRec.grid(column=1, row=3)

#labels for depositos
lblD = Label(frameDepositos, text="Depositos", font=("Helvetica", 16, 'underline'))
lblD.grid(column=6, row=0)
lblF = Label(frameDepositos, text="Fecha")
lblF.grid(column=5, row=1)
lblB = Label(frameDepositos, text="Banco")
lblB.grid(column=6, row=1) 
lblDe = Label(frameDepositos, text="Monto")
lblDe.grid(column=7, row=1)
lblTotDep = Label(frameDepositos, textvariable=var1, width=12)        
lblDif = Label(frameDepositos, textvariable=var2)  

#text input boxes recibos
cta = Entry(frameRecibos, width=10)
cta.grid(column=0, row=2)
cta.bind('<Tab>', checkCta)  #check if client exist in CSV, if not, creat input
cta.bind('<Return>', checkCta)
lblCta = Label(frameRecibos, text='  ', width=20)
lblCta.grid(column=1, row=2)
def returnEntry(event):
    recibo.focus()
money = Entry(frameRecibos, width=10)
money.grid(column=2, row=2)
money.bind('<Return>', returnEntry)
def returnEntry1(event):
    btn1.focus()
recibo = Entry(frameRecibos, width=10)
recibo.grid(column=3, row=2)
recibo.bind('<Return>', returnEntry1)

btn1 = Button(frameRecibos, text="Enter", command=ingRec) #enter Recibos
btn1.grid(column=4, row=2)
btn1.bind('<Return>', ingRec)

#text input for depositos
fecha = Entry(frameDepositos, width=10)
fecha.grid(column=5, row=2)
banco = Entry(frameDepositos, width=15)
banco.grid(column=6, row=2)
monto = Entry(frameDepositos, width=10)
monto.grid(column=7, row=2)

btn2 = Button(frameDepositos, text="Enter", command=ingDep) #enter depostios
btn2.grid(column=8, row=2)
btn2.bind('<Return>', ingDep)

#text input entries for gastos
lblListGastos = []
listGastoDesc = []
gastosAmounts = []
fondosAmounts = [700, 0] #a list to hold the values of epcot fondos and the funds from cobros
var3 = StringVar()
var4 = StringVar()
totalGastos = 0.0
commonGastos = ["Taxi", "Hotel", "Comida", "Celular", "Extra"]
u = []
def buildGastosEntry(x,y,z,u):
    global listGastoDesc
    global gastosAmounts
    global fondosAmountsList
    #labels and inputs for gastos
    fondosAmountsList = []
    listGastoDesc = []
    gastosAmounts = []
    lblG = Label(frameGastos, text="Gastos", font=("Helvetica", 16, 'underline'))
    lblG.grid(column=10, row=0)
    lblG1 = Label(frameGastos, text="        Descripcion")
    lblG1.grid(column=9, row=2)
    lblG2 = Label(frameGastos, text = 'Fondos Epcot')
    lblG2.grid(column = 9, row = 1)
    lblG3 = Label(frameGastos, text = 'Fondos Cobros')
    lblG3.grid(column = 9, row = 2)
    fondosEpcot = Entry(frameGastos, width = 15)
    fondosEpcot.grid(column = 10, row = 1)
    fondosEpcot.insert(0, x)
    fondosAmountsList.append(fondosEpcot)
    fondosCobros = Entry(frameGastos, width = 15) 
    fondosCobros.grid(column = 10, row = 2)
    fondosCobros.insert(0, y)
    fondosAmountsList.append(fondosCobros)
    lblG4 = Label(frameGastos, text = '--------------------')
    lblG4.grid(column = 9, row = 3)
    fondosAmounts[0] = fondosEpcot.get()
   
    r = 6
    r1 = 6        
    c = 0
    for g in range(10):    #build entries for Gastos Descriptions
       g = Entry(frameGastos, width = 15)
       g.grid(column = 9, row = r)
       r += 1
       try: 
           g.insert(0, z[c]) #insert default descriptions to gasto 
       except:
           pass
       c += 1
       listGastoDesc.append(g)
    for j in range(10):     #build entries for Gastos Amounts
       i = Entry(frameGastos, width = 15)
       i.grid(column = 10, row = r1)
       gastosAmounts.append(i)
       r1 += 1 
       try: #insert amounts from unpack incase of loading a caja
               i.insert(0,u[j])
       except:
           pass
    var3.set('Total:     $ ')
    lblG5 = Label(frameGastos, textvariable = var3, width=20)
    lblG5.grid(column = 10 , row = r1)
    
    def totGastos():  #function to total out the expense and calculate a difference if any         
        global totalGastos
        totalGastos = 0.0
        checkForNil(fondosCobros)
        checkForNil(fondosEpcot)                
        for i in lblListGastos:
            i.destroy()
        for t in gastosAmounts:
            try:
                if float(t.get()) > 0:
                    totalGastos += float(t.get())
            except: 
                pass
        var3.set('Total:      $ ' + str(totalGastos)) 
        
        fondosGastos = float(fondosEpcot.get()) + float(fondosCobros.get())
        difGastos = fondosGastos - totalGastos
        var4.set('Diferencia:  $' + str(difGastos) )
        lblG6 = Label(frameGastos, textvariable = var4, width=20)
        lblG6.grid(column = 10, row = r1 + 1)
        lblListGastos.append(lblG6)
        fondosAmounts[1] = fondosCobros.get()
        fondosAmounts[0] = fondosEpcot.get()
        
    btnGastosCalculate = Button(frameGastos, text = "Totalizar", command = totGastos)
    btnGastosCalculate.grid(column = 11, row = r1)
    
def checkForNil(a):  #func to be used to check for nil
    if a.get() == "":
        a.insert(0,0)    
   
buildGastosEntry(fondosAmounts[0], fondosAmounts[1], commonGastos,u)
try:
    with open('head.dat', 'rb') as f:
        nombre, pais = pickle.load(f)
    f.close()
except:
    pass
cta.focus()
window.mainloop()
