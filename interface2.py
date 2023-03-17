from tkinter import *
from tkinter import font
from tkinter.tix import ButtonBox
import dbf

#--------incorporación dbf a tabla------/
table=dbf.Table(filename='sources\MGW10008.dbf')
table.open(dbf.READ_WRITE)
#------------------------------------------------------------root config
raiz=Tk()
raiz.title("Filtrar y Buscar")#nombre del programa no oficial
raiz.resizable(0,0) 
raiz.iconbitmap("sources\lupaxd.ico")

#variables
go=StringVar()
focus=-1

#listasxd
lstuti=[]
indice1=[]
indice2=[]
cfolio=[]
cseriedo01=[]
creferen01=[]
inmutserie=[]
#--------dbfshit----------/
for record in table:
    inmutserie.append(record[0])
    cseriedo01.append(record[3])
    cfolio.append(record[4])
    creferen01.append(record[16])

#------------------------------------------------------------frame config
frame=Frame(raiz, bg='white')
frame.pack(fill='both', expand='true')#tambien está anchor para seleccionar donde se esquina, con brujula(n,s,e,w)/
frame.config(relief='ridge', bd='10')#y también tenemos el 'side', muy similar(left,right,top,bottom)////

#------------------------------------------------------------etiquetas y variables
#/////////////////////////////////////////////////////////Showing labels, not really important, just display
Label(frame, text='Folio:', font=("comic sans ms",18), bg='white').grid(row=0, column=0, sticky='e', pady=4, padx=4)#prueba tambien ipady, y ipadx
Label(frame, text='Serie:', font=('comic sans ms',18), bg='white').grid(row=1, column=0, sticky='e', pady=4, padx=4)
Label(frame, text='Referencia:', font=('comic sans ms',16), bg='white').grid(row=3, column=0, sticky='e', pady=4)

#/////////////////////////////////////////////////////////labels de los dos datos necesarios para buscar la referencia(fijos)
folio,serie=Entry(frame, font=('arial',18)),Entry(frame, font=('arial',18,))
folio.config(justify='center')#configuracion de entrys
serie.config(justify='center')#///////////////////////
#///////////////ubicación inicial de los entry's
folio.grid(row=0, column=1, pady=4, padx=7)
serie.grid(row=1, column=1, pady=4, padx=7)


#Función principal (busca y sincroniza los datos que se introducen)
def search (entfolio,entserie):
    table.open(dbf.READ_WRITE)
    nocoincidencias.grid_forget()#este limpia el mensaje de no coincidencias, si es que saltó
    c1=0#variable de control
    c2=0#variable de control
    focus=-1#variable de control
    for i in cfolio:
        if i == entfolio:
            indice1.append(c1)
        c1+=1
    for a in cseriedo01:

        if a.strip() == entserie.upper():
            indice2.append(c2)
        c2+=1
    for e in indice1:
        if e in indice2:
            focus=e
    lstuti.append(focus)
    if focus!=-1:
        go.set(creferen01[focus])#esta variable entrega la referencia encontrada al label--------/
        if go== '':
            go.set('Referencia en blanco')
        foundref.grid(row=3, column=1, pady=4, padx=4)
        indice1.clear()
        indice2.clear()
        c1=0
        c2=0
        btnvolver.grid(row=4, column=0, pady=4, padx=4)
        btnmodify.grid(row=4, column=1, sticky='w', padx=10)
        btnbuscar.grid_forget()
    else:#else que sale en caso de no coincidencia
        nocoincidencias.grid(row=3, column=1, pady=4, padx=4)

#funcion de cancelación de movimiento, modificación, o volver a la búsqueda----/
def cancel():
    foundsel.delete(0,'end')
    folio.delete(0,'end')
    serie.delete(0,'end')
    table.close()
    foundsel.grid_forget()
    foundref.grid_forget()
    btnmodify.grid_forget()
    btncancel.grid_forget()
    btnvolver.grid_forget()
    btnsave.grid_forget()
    btnbuscar.grid(row=4, column=1, padx=10)

#--------------------funcion donde salta la seccion de modificación--------------/
def mas():#------los grid_forget quitan los botones que no se usan aqui----/
    btnvolver.grid_forget()
    btnbuscar.grid_forget()
    foundref.grid_forget()
    btnmodify.grid_forget()
    btncancel.grid(row=4, column=0, padx=4, pady=4)
    foundsel.delete(0,'end')#esto se asegura de que el cuadro de texto este en blanco(en caso de que se haya usado una vez antes)
    foundsel.grid(row=3, column=1, pady=4, padx=4)
    btnsave.grid(row=4, column=1, sticky='w', padx=10)
    table.close()

#------------------------Funcion posterior al guardar modificación(modifica la lista)---------/            
def back(ren):
    focus=lstuti[-1]
    with table:#----------------con esta librearia, la única forma de modificar un campo específico del dbf es con with, o con Process()---/
        wa=table[focus]
        with wa:
            wa['CREFEREN01']=ren
    del creferen01[focus]
    creferen01.insert(focus,ren)
    lstuti.clear()
    table.close()
    btnsave.grid_forget()
    btncancel.grid_forget()
    foundsel.grid_forget()
    serie.delete(0,'end')
    folio.delete(0,'end')
    btnbuscar.grid(row=4, column=1, padx=10)

#-------------------entry de modificación de ref------------------------------------------/
foundsel=Entry(frame, font=('arial',16), justify='center')#elección a modificar por el usuario

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////botones y label(buscar, modificar, volver)
btnbuscar=Button(frame, text='Buscar', font=('comic sans ms',16), command=lambda:search(float(folio.get()), str(serie.get())),)
btnbuscar.grid(row=4, column=1, padx=10)
foundref=Label(frame, text='Referencia: ', textvariable=go, font=('arial',18), bg='white')
btnsave=Button(frame, text='Guardar', font=('arial',16), command=lambda:back(foundsel.get()))

btnmodify=Button(frame, text='Modificar', font=('arial',16), command=lambda:mas())#botón modificar

btncancel=Button(frame, text='Cancelar', font=('arial',16), command=lambda:cancel())#cancelar modificación
btnvolver=Button(frame, text='Volver', font=('arial',16), command=lambda:cancel())#volver a la búsqueda

nocoincidencias=Label(frame, text='No hay coincidencias', font=('arial',18), bg='white')#mensaje en caso de no coincidencias o no existencia

#main loop, dont move
raiz.mainloop()