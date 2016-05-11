#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.gdk
    import gtk.glade
    import hal
    import gladevcp.makepins
    import pango
    import string
    from gladevcp.gladebuilder import GladeBuilder
except:
    sys.exit(1)
    
class HellowWorldGTK:

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("work.glade")
#        halcomp = hal.component("work")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")
#+ Устанавливаем шрифты и все что не смог гладе
        lABELFont = pango.FontDescription("Tahoma 24")
        self.builder.get_object("ProgName").modify_font(lABELFont)
        self.builder.get_object("label4").modify_font(lABELFont)
        self.builder.get_object("label5").modify_font(lABELFont)
        self.builder.get_object("label6").modify_font(lABELFont)
        self.builder.get_object("label7").modify_font(lABELFont)
        self.builder.get_object("label8").modify_font(lABELFont)
        self.builder.get_object("label9").modify_font(lABELFont)
        self.builder.get_object("label15").modify_font(lABELFont)
#- Устанавливаем шрифты и все что не смог гладе       
        self.window.show()
        self.Click_Button_panel(self.builder.get_object('f1'))

        
        
#        panel = gladevcp.makepins.GladePanel( halcomp, "work.glade", self.builder, None)
 #       halcomp.ready()
        
#         
#         self.gladefile = "face1.glade" 
#         self.glade = gtk.Builder()
#         self.glade.add_from_file(self.gladefile)
#         halcomp = hal.component("face1")
#         self.glade.connect_signals(self)
#         self.glade.get_object("MainWindow").show_all()
    def Set_Font_Text_Button(self,widget,text):
        obj=self.builder.get_object(widget)
        obj.set_label(text)
        for widget2 in obj.get_children(): 
            if (isinstance(widget2, gtk.Label)):
                widget2.set_justify(gtk.JUSTIFY_CENTER)

    def Click_Button_panel(self, widget):
        #+ Подкаждую закладку меняем кнопки

        
        NameButton = widget.get_label()
        if (NameButton.translate(None, string.whitespace).find('F1Начатьвыделение')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.Tag = self.textbuffer.create_tag("Selected",background='yellow',size_points=24.0)
#            tttt=gtk.TextView
#            tttt.get_buffer().s
            print self.Tag
            
        
        elif (NameButton.translate(None, string.whitespace).find('F5Редакторпрограмм')==0):
            self.Set_Font_Text_Button('f1','F1 \nНачать\nвыделение')
            self.Set_Font_Text_Button('f2','F2 \nЗакончить\nвыделение')
            self.Set_Font_Text_Button('f3','F3 \nСкопировать\n ')
            self.Set_Font_Text_Button('f4','F4 \nВырезать\n ')
            self.Set_Font_Text_Button('f5','F5 \nВставить\n ')
            self.Set_Font_Text_Button('f6','F6 \n  \n ')
            self.Set_Font_Text_Button('f7','F7 \n  \n ')
            self.Set_Font_Text_Button('f8','F8 \nВернуться\n на \nГлавную')
            self.builder.get_object("notebook1").set_current_page(4)
        else:
            self.Set_Font_Text_Button('f1','F1 \nРучное \nУправление')
            self.Set_Font_Text_Button('f2','F2 \nAUTO\n')
            self.Set_Font_Text_Button('f3','F3 \nНоль Детали\n')
            self.Set_Font_Text_Button('f4','F4 \nКоррекция\nинструмента')
            self.Set_Font_Text_Button('f5','F5 \nРедактор\nпрограмм')
            self.Set_Font_Text_Button('f6','F6 \nГрафика\n')
            self.Set_Font_Text_Button('f7','F7 \nСервис\n')
            self.Set_Font_Text_Button('f8','F8 \nСистема\n')
            self.builder.get_object("notebook1").set_current_page(0)

    
    def on_MainWindow_delete_event(self, widget, event):
        gtk.main_quit()
        
    def gtk_widget_destroy(self, widget, event):
        gtk.main_quit()  
    
    def on_notebook1_select_page(self, notebook, arg1, user_data):
        print(notebook)  
    
    
        
    def master_page(self, widget):
        self.notebook = self.glade.get_object("notebook1")
        self.notebook.set_current_page(0)
#        self.notebook.set_current_page(self.notebook.get_current_page()+1)
    def change_page_down(self, widget):
        self.notebook = self.glade.get_object("notebook1")
        self.notebook.prev_page()
#        self.notebook.set_current_page(self.notebook.get_current_page()-1)   
    
    def helloWorld(self, widget):
        
        gtk.main_quit()
#         print(self)
#         print(widget)
#         self.glade.get_object("label1").set_text('Ебана в рот')
        

if __name__ == "__main__":
    hwg = HellowWorldGTK()
    gtk.main()    
