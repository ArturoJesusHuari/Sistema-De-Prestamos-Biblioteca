from tkinter import *
import sqlite3
from datetime import datetime
from tkcalendar import Calendar

class MainApp():
    def main(self):
        #Ventana
        Inicio = Tk()
        Inicio.title('Sistema de Biblioteca')
        Inicio.geometry('500x300+100+100')
        Inicio.iconbitmap("library.ico")
        Inicio.resizable(0, 0)
        #Botones
        ButtonRealizarPedido = Button(Inicio, command = lambda:[self.InterfazRealizarPedido(Inicio)] , text ="PETICION DE LIBROS", bg="#1DDB2C", fg="#000000", font = "Calibri 10 bold")
        ButtonRealizarPedido.place(x=55, y=200)
        ButtonDevolucionLibros = Button(Inicio, command = lambda:[self.InterfazDevolucion(Inicio)], text ="DEVOLUCION DE LIBROS", bg="#FF2221", fg="white", font = "Calibri 10 bold")
        ButtonDevolucionLibros.place(x=305, y=200)
        #Imagenes
        PNGPeticion = PhotoImage(file="Peticion.png")
        LabelCodigoEstudiante = Label(Inicio, image=PNGPeticion)
        LabelCodigoEstudiante.place(x=45, y=50)
        PNGDevolucion = PhotoImage(file="Devolucion.png")
        LabelDevolucion = Label(Inicio, image=PNGDevolucion)
        LabelDevolucion.place(x=305, y=55)
        Inicio.mainloop()

    def InterfazDevolucion(self, Inicio) :
        Devolucion = Toplevel()
        Devolucion.geometry("500x300+650+100")
        Devolucion.title("Devolucion")
        Devolucion.iconbitmap("library.ico")
        Devolucion.resizable(0, 0)

        Devolucion.mainloop()

    def InterfazRealizarPedido(self, Inicio) :
        RealizarPedido = Toplevel()
        RealizarPedido.geometry("500x300+650+100")
        RealizarPedido.title("Realizar Pedido")
        RealizarPedido.iconbitmap("library.ico")
        RealizarPedido.resizable(0, 0)
        #Labels
        LabelCodigoEstudiante = Label(RealizarPedido, text = "Codigo de estudiante: ", font = "Calibri 10")
        LabelCodigoEstudiante.place(x=10, y=10)
        LabelLibros = Label(RealizarPedido, text = "Libros: ", font = "Calibri 10 bold")
        LabelLibros.place(x=10, y=50)
        LabelID = Label(RealizarPedido, text = "Libros: ", font = "Calibri 10")
        LabelID.place(x=10, y=250)
        LabelListBox = Label(RealizarPedido)
        LabelListBox.place(x=10, y=70)
        LabelFecha = Label(RealizarPedido, text = "Fecha: ", font = "Calibri 10")
        LabelFecha.place(x=320, y=10)
        #ComboBox
        ListBoxLibros = Listbox(LabelListBox, width=35, height=10)
        ListBoxLibros.pack(side = LEFT, fill = BOTH)
        scrollbar = Scrollbar(LabelListBox)
        scrollbar.pack(side = RIGHT, fill = BOTH)
        for values in self.ListDataBaseLibros():
            #print(values)
            ListBoxLibros.insert(END, str(values[0])+' - '+str(values[1])+' / '+str(values[2]))
        ListBoxLibros.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = ListBoxLibros.yview)
        #Entrys
        EntryCodigoEstudiante = Entry(RealizarPedido, font = "Calibri 10")
        EntryCodigoEstudiante.place(x=140, y=10)
        EntryBusqueda = Entry(RealizarPedido, font = "Calibri 10")
        EntryBusqueda.place(x=100, y=50)
        EntryID = Entry(RealizarPedido, font = "Calibri 10")
        EntryID.place(x=50, y=250)
        EntryFechaEntrega = Entry(RealizarPedido, font = "Calibri 10")
        EntryFechaEntrega.place(x=320, y=40)
        #Botones
        PNGBusqueda = PhotoImage(file="Busqueda.png")
        ButtonBuscar = Button(RealizarPedido, image=PNGBusqueda, command = lambda:[self.Buscar(self.ListDataBaseLibros(), EntryBusqueda.get(), ListBoxLibros)] )
        ButtonBuscar.place(x=250, y=49)
        ButtonAgregar = Button(RealizarPedido, text="Agregar", command = lambda:[self.Seleccion(EntryID, ListBoxLibros)] , font = "Calibri 10")
        ButtonAgregar.place(x=190, y=248)
        ButtonFinalizar = Button(RealizarPedido, text="Finalizar" , command=lambda:[self.Finalizar(RealizarPedido, EntryCodigoEstudiante.get(), EntryFechaEntrega.get(), EntryID.get())], font = "Calibri 10")
        ButtonFinalizar.place(x=420, y=248)

        PNGCalendario = PhotoImage(file="Calendario.png")
        ButtonFecha = Button(RealizarPedido, image=PNGCalendario, command = lambda:[self.Calendario(EntryFechaEntrega)])
        ButtonFecha.place(x=360, y=10)


        RealizarPedido.mainloop()

    def Calendario(self, Entry):
        Calendario = Tk()
        Calendario.geometry("300x250+750+140")
        Calendario.title("Seleccionar Fecha")
        Calendario.iconbitmap("Calendario.ico")
        Calendario.resizable(0, 0)
        now = datetime.now()
        cal = Calendar(Calendario, selectmode = 'day',
                    year = int(now.year), month = int(now.month),
                    day = int(now.day))
        cal.pack(pady = 10)
        Button(Calendario, text = "Seleccionar fecha", command = lambda:[self.SeleccionFecha(cal.get_date(), Entry), Calendario.destroy()] ).pack(pady = 10)
        date = Label(Calendario, text = "")
        date.pack(pady = 10)
        Calendario.mainloop()

    def SeleccionFecha(self, date, Entry):
        date = date[0:len(date)-2]+'20'+date[len(date)-2:len(date)]
        Entry.delete(0, END)
        date = self.FechaValida(date)
        date=date[3:5]+'/'+date[0:2]+'/'+date[6:10]
        if(self.ValidarFecha(str(date))):
            Entry.insert(0, date)
        else:
            Error = Toplevel()
            Error.geometry("200x80+790+200")
            Error.title("Error")
            Error.iconbitmap("Error.ico")
            Error.resizable(0, 0)
            LabelError = Label(Error, text = "Fecha no valida")
            LabelError.place(x=35, y=20)
            Error.mainloop()

    def ValidarFecha(self, String):
        format = str('%'+'d/%m/%Y')
        res = True
        try:
            res = bool(datetime.strptime(String, format))
        except ValueError:
            res = False
        return res

    def FechaValida(self, String):
        try:
            dia = int(String[0:2])
        except ValueError:
            String = '0'+str(String)
        try:
            mes = int(String[3:5])
        except ValueError:
            año = String[3:9]
            String = String[0:3]+'0'+str(año)
        return String

    def Seleccion(self, Entry, ListBox):
        itm = ListBox.get(ListBox.curselection())
        if(len(Entry.get())==0):
            Entry.insert(0, itm[0:itm.find("-")-1])
        else:
            Texto = Entry.get()
            Entry.delete(0, END)
            Entry.insert(0, Texto+','+itm[0:itm.find("-")-1])

    def Finalizar(self, RealizarPedido, Codigo, FechaDevolucion, Libros):
        if (self.ValidarCodigo(Codigo)):
            if(self.ValidarFecha(FechaDevolucion)):
                if(self.ValidarLibros(Libros)):
                    FechaDevolucion = self.FechaValida(FechaDevolucion)
                    now = datetime.now()
                    Fecha = str(now.day)+'/'+str(now.month)+"/"+str(now.year)
                    Fecha = self.FechaValida(Fecha)
                    if(self.MayorFecha(Fecha, FechaDevolucion)):
                        Ficha = Toplevel()
                        Ficha.geometry("500x300+650+100")
                        Ficha.title("Ficha")
                        Ficha.iconbitmap("library.ico")
                        Ficha.config(bg="white")
                        Ficha.resizable(0, 0)
                        #Modificacion en base de datos
                        ListaPedidos = Libros.split(',')
                        ListaIndices = []
                        for i in ListaPedidos:
                            ListaIndices.append(int(i))
                        for e in ListaIndices:
                            con = sqlite3.connect('Libros.db')
                            cursor = con.cursor()
                            cursor.execute("SELECT * FROM libros")
                            for j in range(e):
                                Registro = cursor.fetchone()
                            cursor.execute("UPDATE libros set Stock = {} where id = {};".format(str(int(Registro[3])-1),e))
                            con.commit()
                            con.close()

                        con = sqlite3.connect('Prestamos.db')
                        cursor = con.cursor()
                        cursor.execute("INSERT into prestamos (CodigoEstudiante, FechaPedido, FechaDevolucion, Libros) values ('{}','{}','{}','{}');".format(str(Codigo), str(Fecha), str(FechaDevolucion), str(Libros)))
                        con.commit()
                        con.close()

                        RealizarPedido.destroy()
                        #Label
                        PNGUncp = PhotoImage(file="UNCP.png")
                        LabelUncpImage = Label(Ficha, image=PNGUncp, bg="white")
                        LabelUncpImage.place(x=20, y=10)
                        LabelUncpTitulo = Label(Ficha, text = "UNIVERSIDAD NACIONAL DEL CENTRO DEL PERÚ", font = "Times 12 bold", bg="white")
                        LabelUncpTitulo.place(x=90, y=30)
                        LabelFichaDePrestamo = Label(Ficha, text = "Ficha de préstamo", font = "Times 11", bg="white")
                        LabelFichaDePrestamo.place(x=20, y=80)
                        LabelCodigoEstudiante = Label(Ficha, text = "Codigo de estudiante: {}".format(Codigo), font = "Times 10", bg="white")
                        LabelCodigoEstudiante.place(x=20, y=110)
                        LabelFechaPrestamo = Label(Ficha, text = "Fecha de prestamo: {}".format(Fecha), font = "Times 10", bg="white")
                        LabelFechaPrestamo.place(x=20, y=130)
                        LabelFechaDevolucion = Label(Ficha, text = "Fecha de devolucion: {}".format(FechaDevolucion), font = "Times 10", bg="white")
                        LabelFechaDevolucion.place(x=20, y=150)
                        LabelLibros = Label(Ficha, text = "Libros: {}".format(Libros), font = "Times 10", bg="white")
                        LabelLibros.place(x=20, y=170)
                        Ficha.mainloop()
                    else:
                        Error = Toplevel()
                        Error.geometry("200x80+790+200")
                        Error.title("Error")
                        Error.iconbitmap("Error.ico")
                        Error.resizable(0, 0)
                        LabelError = Label(Error, text = "Fecha de devolucion no valida")
                        LabelError.place(x=15, y=20)
                else:
                    Error = Toplevel()
                    Error.geometry("200x80+790+200")
                    Error.title("Error")
                    Error.iconbitmap("Error.ico")
                    Error.resizable(0, 0)
                    LabelError = Label(Error, text = "Error al registrar los libros")
                    LabelError.place(x=20, y=20)
            else:
                Error = Toplevel()
                Error.geometry("200x80+790+200")
                Error.title("Error")
                Error.iconbitmap("Error.ico")
                Error.resizable(0, 0)
                LabelError = Label(Error, text = "Fecha de devolucion no valida")
                LabelError.place(x=15, y=20)
        else:
            Error = Toplevel()
            Error.geometry("200x80+790+200")
            Error.title("Error")
            Error.iconbitmap("Error.ico")
            Error.resizable(0, 0)
            LabelError = Label(Error, text = "Codigo de estudiante no valido")
            LabelError.place(x=15, y=20)

    def ValidarCodigo(self, Codigo):
        if(len(Codigo)==11):
            try:
                ParteNumerica = int(Codigo[0:10])
                try:
                    ParteLetra = int(Codigo[10:11])
                    return False
                except Exception as e:
                    if(Codigo[10:11].isupper()):
                        return True
                    else:
                        return False
            except Exception as e:
                return False
        else:
            return False

    def ListLibros(self, Libros):
        ListaLibros = Libros.split(',')
        return ListaLibros

    def Buscar(self, ListLibros, StringBusqueda, ListBox):
        ListBox.delete(0, END)
        for libros in ListLibros:
            Palabras = (str(libros[0])+' - '+str(libros[1])+' / '+str(libros[2])).split(' ')
            for palabra in Palabras:
                if str(palabra) == StringBusqueda:
                 ListBox.insert(END, str(Palabras[0])+' - '+str(libros[1])+' / '+str(libros[2]))

    def ValidarLibros(self, Libros):
        try:
            ListLibros = Libros.split(',')
            if(ListLibros[0] == ''):
                return False
            else:
                return True
        except Exception as e:
                return False

    def MayorFecha(self, StringFecha1, StringFecha2):
        Fecha1 = datetime(int(StringFecha1[6:10]), int(StringFecha1[3:5]), int(StringFecha1[0:2]))
        Fecha2 = datetime(int(StringFecha2[6:10]), int(StringFecha2[3:5]), int(StringFecha2[0:2]))

        if(Fecha1 <= Fecha2):
            return True
        else:
            return False

    def ListDataBaseLibros(self):
        try:
            con = sqlite3.connect('Libros.db')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM libros")
            Registros = cursor.fetchall()
            ListLibros = []

            for Registro in Registros:
                ListLibros.append(Registro)

            con.commit()
            con.close()
            return ListLibros

        except Exception as e:
            print(e)

    def ListDataBasePrestamos(self):
        try:
            con = sqlite3.connect('Prestamos.db')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM prestamos")
            Registros = cursor.fetchall()
            ListPedidos = []

            for Registro in Registros:
                ListPedidos.append(Registro)

            con.commit()
            con.close()
            return ListPedidos

        except Exception as e:
            print(e)

if __name__ == '__main__':
    App = MainApp()
    App.main()