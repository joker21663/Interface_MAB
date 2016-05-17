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
    import linuxcnc
    import gladevcp.makepins
    import pango
    import string
    import sys,os
    from gladevcp.gladebuilder import GladeBuilder
except:
    sys.exit(1)

first_position=0
last_position=0
isSelect=False


    
class HellowWorldGTK:


    def __init__(self):
#  Константы всякие
        self.type_gremlin_view = ("X","Y","Z","P")

#  Установка emc       
        self.emc = linuxcnc
        self.status = self.emc.stat()
        
        self.builder = gtk.Builder()
        BASE = os.path.abspath("/")
        datadir = os.path.join(BASE, "usr", "share", "linuxcnc")
        xmlname = os.path.join(datadir,"work.glade")
        self.builder.add_from_file(xmlname)
#        halcomp = hal.component("work")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")
#  Установка HAL         
        self.halcomp = hal.component("work")
        self.machine_status = 0
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
#        self.builder.get_object("label20").modify_font(lABELFont)
        self.builder.get_object("ProgName1").modify_font(lABELFont)
        self.builder.get_object("label27").modify_font(lABELFont)
        self.builder.get_object("label28").modify_font(lABELFont)
        self.builder.get_object("label29").modify_font(lABELFont)
        self.builder.get_object("label24").modify_font(lABELFont)
        self.builder.get_object("label25").modify_font(lABELFont)
        self.builder.get_object("label26").modify_font(lABELFont)
#- Устанавливаем акселераторы которые не смог гладе 
        agroup = gtk.AccelGroup()
        self.window.add_accel_group(agroup)
        knn=self.builder.get_object("f9")
        knn.add_accelerator("clicked",agroup,gtk.keysyms.Escape, 0, 0)
#- Устанавливаем шрифты и все что не смог гладе       
        self.window.show()
        self.Click_Button_panel(self.builder.get_object('f9'))
#+ Тэг на выделение
        self.Tag = self.builder.get_object("textview3").get_buffer().create_tag("Selected",background='yellow',size_points=24.0)
#- Тэг на выделение 
        
        
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


    def on_textview3_move_cursor(self, widget,MovementStepU,intparam,boolparam):
        global last_position
        if isSelect:
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.remove_tag_by_name("Selected",self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(last_position))
            self.textbuffer.apply_tag_by_name("Selected",self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position))
            last_position = self.textbuffer.props.cursor_position
#       print (self.textbuffer.props.cursor_position)

        
    def Click_Button_panel(self, widget):
        #+ Подкаждую закладку меняем кнопки
        global first_position
        global isSelect
        NameButton = widget.get_label()
        if (NameButton.translate(None, string.whitespace).find('F3Начатьвыделение')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            first_position=self.textbuffer.props.cursor_position
            
            self.textbuffer.remove_all_tags(self.textbuffer.get_iter_at_offset(0),self.textbuffer.get_iter_at_offset(self.textbuffer.get_char_count()))
            self.textbuffer.apply_tag(self.Tag,self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position),self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position))
            self.textbuffer.select_range(self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position), self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position))
            isSelect=True
#            tttt=gtk.TextView
#            tttt.get_buffer().a
#            print self.textbuffer.props.cursor_position
        elif (NameButton.translate(None, string.whitespace).find('F2Поиск')==0): 
            self.findwindow = self.builder.get_object("findwindow")
            self.Set_Font_Text_Button('find','F1 \nПоиск\n')
            self.Set_Font_Text_Button('cancel','F2 \nОтмена\n')
            self.findwindow.show()
        elif (NameButton.translate(None, string.whitespace).find('F1Поиск')==0): 
            findtext=self.builder.get_object("entry1").get_text()
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            textToFind=self.textbuffer.get_text(self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position), self.textbuffer.get_iter_at_offset(self.textbuffer.get_char_count()), True)
            index=textToFind.find(findtext)
            if (index>-1):
                self.textbuffer.remove_all_tags(self.textbuffer.get_iter_at_offset(0),self.textbuffer.get_iter_at_offset(self.textbuffer.get_char_count()))
                self.textbuffer.apply_tag(self.Tag,self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index),self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index+len(findtext)))
                self.textbuffer.select_range(self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index), self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index))
            else:
                parent = None
                md = gtk.MessageDialog(parent, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, "Ничего не найдено")
                md.run()
                md.destroy()
            self.findwindow.hide()
        elif (NameButton.translate(None, string.whitespace).find('F2Отмена')==0): 
            self.findwindow.hide()
        elif (NameButton.translate(None, string.whitespace).find('F4Закончитьвыделение')==0): 
            isSelect=False
        elif (NameButton.translate(None, string.whitespace).find('F5Скопировать')==0): 
            isSelect=False
            self.textbuffer = self.builder.get_object("textview3").get_buffer() 
            self.textbuffer.select_range(self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(last_position))   
            self.textbuffer.copy_clipboard(gtk.clipboard_get("CLIPBOARD"))
#            self.textbuffer.delete_selection(True,True)
        elif (NameButton.translate(None, string.whitespace).find('F6Вырезать')==0): 
            isSelect=False
            self.textbuffer = self.builder.get_object("textview3").get_buffer() 
            self.textbuffer.select_range(self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(last_position))   
            self.textbuffer.cut_clipboard(gtk.clipboard_get("CLIPBOARD"),True)
#            self.textbuffer.delete_selection(True,True)    
        elif (NameButton.translate(None, string.whitespace).find('F7Вставить')==0): 
            isSelect=False
            self.textbuffer = self.builder.get_object("textview3").get_buffer() 
            self.textbuffer.paste_clipboard(gtk.clipboard_get("CLIPBOARD"),None,True)
        elif (NameButton.translate(None, string.whitespace).find('F1Выборфайлапрограммы')==0): 
            self.Fileprogramm = self.builder.get_object("vcp_filechooserbutton1")
            dialog = gtk.FileChooserDialog("Выбор файла программы..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
   
#            filter = gtk.FileFilter()
#            filter.set_name("All files")
#            filter.add_pattern("*")
#            dialog.add_filter(filter)
            filter = gtk.FileFilter()
            filter.set_name("Images")
            filter.add_mime_type("image/png")
            filter.add_mime_type("image/jpeg")
            filter.add_mime_type("image/gif")
            filter.add_pattern("*.png")
            filter.add_pattern("*.jpg")
            filter.add_pattern("*.gif")
            filter.add_pattern("*.tif")
            filter.add_pattern("*.xpm")
            filter.add_pattern("*.ngc")
            filter.add_pattern("*.nc")
            dialog.add_filter(filter)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                self.Fileprogramm.set_filename(dialog.get_filename())
                my_file = open(dialog.get_filename())
                self.textbuffer = self.builder.get_object("textview3").get_buffer() 
                self.textbuffer.set_text(my_file.read())
                self.builder.get_object("ProgName").set_text(dialog.get_filename())
#                my_string = my_file.read()
#                print("Было прочитано:")
#                print(my_string)
                my_file.close()
#                print dialog.get_filename(), 'selected'
#            elif response == gtk.RESPONSE_CANCEL:
#                print 'Closed, no files selected'
            dialog.destroy()
        elif (NameButton.translate(None, string.whitespace).find('F8Выход')==0):
            gtk.main_quit()
        elif (NameButton.translate(None, string.whitespace).find('F7Test')==0):
            self.status.poll()
            print self.machine_status
        elif (NameButton.translate(None, string.whitespace).find('F1СменитьВид')==0):
            gremlin=self.builder.get_object("hal_gremlin1")
            gremlin.set_property('view',"X")
            print self.type_gremlin_view.index("P")    
        elif (NameButton.translate(None, string.whitespace).find('F5Редакторпрограмм')==0):
            self.Set_Font_Text_Button('f1','F1 \nВыбор файла\nпрограммы')
            self.Set_Font_Text_Button('f2','F2 \nПоиск')
            self.Set_Font_Text_Button('f3','F3 \nНачать\nвыделение')
            self.Set_Font_Text_Button('f4','F4 \nЗакончить\nвыделение')
            self.Set_Font_Text_Button('f5','F5 \nСкопировать\n')
            self.Set_Font_Text_Button('f6','F6 \nВырезать\n ')
            self.Set_Font_Text_Button('f7','F7 \nВставить\n')
            self.Set_Font_Text_Button('f8','F8 \n\nГрафика\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(5)
        elif (NameButton.translate(None, string.whitespace).find('F7Сервис')==0):
            self.Set_Font_Text_Button('f1','F1 \n\n')
            self.Set_Font_Text_Button('f2','F2 \n\n')
            self.Set_Font_Text_Button('f3','F3 \n\n ')
            self.Set_Font_Text_Button('f4','F4 \n\n ')
            self.Set_Font_Text_Button('f5','F5 \n\n ')
            self.Set_Font_Text_Button('f6','F6 \n\n ')
            self.Set_Font_Text_Button('f7','F7 \n Test\n')
            self.Set_Font_Text_Button('f8','F8 \nВыход\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(7)    
        elif (NameButton.translate(None, string.whitespace).find('F6Графика')==0 or NameButton.translate(None, string.whitespace).find('F8Графика')==0):
            self.Set_Font_Text_Button('f1','F1 \nСменить\nВид')
            self.Set_Font_Text_Button('f2','F2 \n\n')
            self.Set_Font_Text_Button('f3','F3 \n\n ')
            self.Set_Font_Text_Button('f4','F4 \n\n ')
            self.Set_Font_Text_Button('f5','F5 \n\n ')
            self.Set_Font_Text_Button('f6','F6 \n\n ')
            self.Set_Font_Text_Button('f7','F7 \n\n ')
            self.Set_Font_Text_Button('f8','F8 \n\n\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(6)   
        elif (NameButton.translate(None, string.whitespace).find('F1РучноеУправление')==0):
            self.Set_Font_Text_Button('f1','F1 \nMDI\nРучной набор')
            self.Set_Font_Text_Button('f2','F2 \nМаховичок\n')
            self.Set_Font_Text_Button('f3','F3 \n0.001\n ')
            self.Set_Font_Text_Button('f4','F4 \n0.01\n ')
            self.Set_Font_Text_Button('f5','F5 \n0.1\n')
            self.Set_Font_Text_Button('f6','F6 \nВращение шпинделя\nвправо')
            self.Set_Font_Text_Button('f7','F7 \nСтоп\nшпиндель')
            self.Set_Font_Text_Button('f8','F8 \nВращение шпинделя\nвлево')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(0)        
        else:
            self.Set_Font_Text_Button('f1','F1 \nРучное \nУправление')
            self.Set_Font_Text_Button('f2','F2 \nAUTO\n')
            self.Set_Font_Text_Button('f3','F3 \nНоль Детали\n')
            self.Set_Font_Text_Button('f4','F4 \nКоррекция\nинструмента')
            self.Set_Font_Text_Button('f5','F5 \nРедактор\nпрограмм')
            self.Set_Font_Text_Button('f6','F6 \nГрафика\n')
            self.Set_Font_Text_Button('f7','F7 \nСервис\n')
            self.Set_Font_Text_Button('f8','F8 \nСистема\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
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
