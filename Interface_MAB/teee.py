#!/usr/bin/env python
# -*- coding: utf-8 -* 
import sys
import ConfigParser
try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.gdk
    import gtk.glade
    import gobject
    import hal
    import linuxcnc
    import gladevcp.makepins
    import pango
    import string
    import sys,os
    import math
    import pprint
    from gscreen import mdi
    from gscreen import emc_interface
    from gladevcp.gladebuilder import GladeBuilder
except:
    sys.exit(1)

first_position=0
last_position=0
isSelect=False


    
class HellowWorldGTK:
    def __init__(self):
#  Константы всякие
        self.type_gremlin_view = ("x","y","z","p")
#  Установка emc       
        self.emc = linuxcnc
        self.status = self.emc.stat()
        self.command = linuxcnc.command()
        self.error_channel = linuxcnc.error_channel()
# сразу включаем станок 
        self.command.state(linuxcnc.STATE_ESTOP_RESET)
        self.command.state(linuxcnc.STATE_ON)
        self.jog_distance=0
        self.curr_coordinate='G54' # П54 и прочее
        mdi_labels = mdi_eventboxes = []
        self.mdi_control = mdi.mdi_control(gtk, linuxcnc, mdi_labels, mdi_eventboxes)
#        self.command.home(0)
#        self.command.home(1)
#        self.command.home(2)
        self.emcgscreen=emc_interface.emc_control(linuxcnc)
        self.emcgscreen.home_all(1)
        self.ConfigParser = ConfigParser.SafeConfigParser()

#        inifile = linuxcnc.ini(sys.argv[2])
#        print inifile
#        for (gcod) in self.status.gcodes():
#            print gcod
        self.builder = gtk.Builder()
        BASE = os.path.abspath("/")
        datadir = os.path.join(BASE, "usr", "share", "linuxcnc")
        xmlname = os.path.join(datadir,"work.glade")
        self.builder.add_from_file(xmlname)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")
        self.window.set_default_size(640,400)
#  Установка HAL         
        self.halcomp = hal.component("work")
        self.halcomp.ready()
        self.machine_status = 0
#+ Устанавливаем шрифты и все что не смог гладе
        lABELFont = pango.FontDescription("Tahoma 20")
        self.builder.get_object("ProgName1").modify_font(lABELFont)
        self.builder.get_object("label27").modify_font(lABELFont)

        self.tree_store = gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_FLOAT,gobject.TYPE_FLOAT,gobject.TYPE_FLOAT)
        self.treeview3 = gtk.TreeView(self.tree_store)
        cell = gtk.CellRendererText()
        cell.set_property('xalign', 0.5);
        cell.set_property("font", "Tahoma 20")
        cell2 = gtk.CellRendererText()
        cell2.set_property('xalign', 0.5);
        cell2.set_property("font", "Tahoma 20")
        cell2.set_property("editable", True)
        cell3 = gtk.CellRendererText()
        cell3.set_property('xalign', 0.5);
        cell3.set_property("font", "Tahoma 20")
        cell3.set_property("editable", True)
        cell4 = gtk.CellRendererText()
        cell4.set_property('xalign', 0.5);
        cell4.set_property("font", "Tahoma 20")
        cell4.set_property("editable", True)
        treeviewcolumn = gtk.TreeViewColumn('OFFSET', cell,text=0)
        treeviewcolumn2 = gtk.TreeViewColumn('X',cell2,text=1)
        treeviewcolumn3 = gtk.TreeViewColumn('Y',cell3,text=2)
        treeviewcolumn4 = gtk.TreeViewColumn('Z',cell4,text=3)

        dictCol = {4:"OFFSET", 5: "X" ,6:"Y",7:"Z"}
        dictCol2 = {4:treeviewcolumn, 5: treeviewcolumn2 ,6:treeviewcolumn3,7:treeviewcolumn4}
        i=4
        while i<8:
            labelfff = gtk.Label(dictCol[i]);
            labelfff.modify_font(lABELFont);
            labelfff.show();
            dictCol2[i].set_widget(labelfff);
            dictCol2[i].set_property('alignment', 0.5)
            dictCol2[i].set_property('expand', True)
            self.treeview3.append_column(dictCol2[i])
            i= i+1
        treeviewcolumn2.set_cell_data_func(cell2, self.Thround)
        treeviewcolumn3.set_cell_data_func(cell3, self.Thround)
        treeviewcolumn4.set_cell_data_func(cell4, self.Thround)
        cell2.connect("edited", self.editTable, self.tree_store,1)
        cell3.connect("edited", self.editTable, self.tree_store,2)
        cell4.connect("edited", self.editTable, self.tree_store,3)
        self.treeview3.connect_after("move-cursor",self.move_cursor)
        self.tree_store.append([str('G54'),float(0),float(0),float(0)])
        self.tree_store.append([str('G55'),float(0),float(0),float(0)])
        self.tree_store.append([str('G56'),float(0),float(0),float(0)])
        self.tree_store.append([str('G57'),float(0),float(0),float(0)])
        self.tree_store.append([str('G58'),float(0),float(0),float(0)])
        self.tree_store.append([str('G59'),float(0),float(0),float(0)])        
        self.builder.get_object("scrolledwindow3").add(self.treeview3)
        self.builder.get_object("scrolledwindow3").show_all()

        self.Set_Big_Fat(self.builder.get_object("label20"))
        self.Set_Big_Fat(self.builder.get_object("label30"))
        self.Set_Big_Fat(self.builder.get_object("label31"))
        self.Set_Big_Fat(self.builder.get_object("label31"))
        self.Set_Big_Fat(self.builder.get_object("label31"))
        self.Set_Big_Fat(self.builder.get_object("label35"))
        self.Set_Big_Fat(self.builder.get_object("label36"))
        self.Set_Big_Fat(self.builder.get_object("label37"))

        self.builder.get_object("label32").modify_font(lABELFont)
        self.builder.get_object("label33").modify_font(lABELFont)
        self.builder.get_object("label34").modify_font(lABELFont)        
        self.builder.get_object("hal_dro6").modify_font(lABELFont)
        self.builder.get_object("hal_dro5").modify_font(lABELFont)
        self.builder.get_object("hal_dro4").modify_font(lABELFont)

        self.gremlin = self.builder.get_object("hal_gremlin1")
        self.gremlin.set_property('metric_units',True)
        self.gremlin_x=0
        self.gremlin_y=0
#- Устанавливаем акселераторы которые не смог гладе 
        agroup = gtk.AccelGroup()
        self.window.add_accel_group(agroup)
        knn=self.builder.get_object("f9")
        knn.add_accelerator("clicked",agroup,gtk.keysyms.Escape, 0, 0)
#        knn=self.builder.get_object("x+")
#        print knn
#        knn.add_accelerator("clicked",agroup,ord('F9'), 0, 0)
#        knn.add_accelerator("clicked",agroup,gtk.gdk.keyval_from_name('g'), 0, 0)
#+ Читаем конфигурационный файл
        inifile = linuxcnc.ini(sys.argv[2])
        toolfile = inifile.find('EMCIO', 'TOOL_TABLE')
        cycle_time = inifile.find('EMCIO', 'CYCLE_TIME')
        dir_ini=os.path.dirname(sys.argv[2])
        self.color_path=dir_ini+"/Color_config.ini"
        if os.path.exists(dir_ini+"/Color_config.ini")== False :
           self.ConfigParser.add_section('DISPLAY')
           self.ConfigParser.set('DISPLAY', 'COLOR_BUTTON',self.builder.get_object("colorbutton1").get_color().to_string())
           self.ConfigParser.set('DISPLAY', 'COLOR_TEXT',self.builder.get_object("colorbutton2").get_color().to_string())
           with open(self.color_path, 'w') as configfile:
                self.ConfigParser.write(configfile)
        self.ConfigParser.read(self.color_path)
        color_button = self.ConfigParser.get('DISPLAY', 'COLOR_BUTTON')
        color_text = self.ConfigParser.get('DISPLAY', 'COLOR_TEXT')
        
#+ Читаем конфигурационный файл
#- Устанавливаем шрифты и все что не смог гладе       
        
    # + Получаем стиль кнопок из конфига
        if (color_button!="unknown" and color_text!="unknown"):
            print color_text
            print color_button
            Button_color =gtk.gdk.Color(color_button)
            Text_color = gtk.gdk.Color(color_text)
            self.builder.get_object("colorbutton1").set_color(Button_color)
            self.builder.get_object("colorbutton2").set_color(Text_color)
#cfgfile = open(sys.argv[2],'w')
#            self.ConfigParser.write(cfgfile)
#            cfgfile.close()

        style = self.builder.get_object("f1").get_style().copy()
        style.bg[gtk.STATE_NORMAL] = self.builder.get_object("colorbutton1").get_color()
        self.color_button_style=style
        self.color_text_style=self.builder.get_object("colorbutton2").get_color()

    # - Получаем стиль кнопок из конфига


        self.default_style_button = self.builder.get_object("f1").get_style().copy()
        map = self.builder.get_object("f1").get_colormap() 
        color = map.alloc_color("green")
        style = self.builder.get_object("f1").get_style().copy()
        style.bg[gtk.STATE_NORMAL] = color
        self.gren_style_button=style
        i=1
        while i<10:
           self.builder.get_object('f'+str(i)).set_size_request(60,60)
           self.builder.get_object('f'+str(i)).set_style(self.default_style_button)

           i=i+1 
        self.window.show()
        self.builder.get_object('hidenButton').show()
        self.Click_Button_panel(self.builder.get_object('f9'))
# Зеленые кнопочги
# Установка цветных кнопок
#+ Тэг на выделение
        self.Tag = self.builder.get_object("textview3").get_buffer().create_tag("Selected",background='yellow',size_points=24.0)
#- Тэг на выделение 
        self.timelock()      


        dir_ini=os.path.dirname(sys.argv[2])
        self.tool_file = dir_ini+"/"+toolfile
# редактор инструмента загрузим из файла и занесем в табличку
        self.liststore = self.builder.get_object('liststore1')
        self.treeview1=self.builder.get_object('treeview1')
        self.builder.get_object("cellrenderertext2").connect("edited", self.editToolTable, self.liststore,1)
        self.builder.get_object("cellrenderertext3").connect("edited", self.editToolTable, self.liststore,2)

        self.builder.get_object("treeviewcolumn2").set_cell_data_func(self.builder.get_object("cellrenderertext2"), self.Thround)
        self.builder.get_object("treeviewcolumn3").set_cell_data_func(self.builder.get_object("cellrenderertext3"), self.Thround)
  
# редактор точек G5x
#        self.liststore2 = self.builder.get_object('liststore2')
#        self.treeview2=self.builder.get_object('treeview2')

        with open(self.tool_file,'r') as fin:
            linesfile = fin.read().split("\n")
            linesfile = filter(lambda x:len(x.strip(' '))>0,linesfile )
            for x in linesfile:
                ToolLine=x.split(' ')
                ToolLine=filter(lambda x:len(x.strip(' '))>0,ToolLine)
                Tnumber =filter(lambda x:x.find('T')==0,ToolLine)
                Znumber =filter(lambda x:x.find('Z')==0,ToolLine)
                Dnumber =filter(lambda x:x.find('D')==0,ToolLine)
                self.liststore.append([int(Tnumber[0].replace('T','')), float(Znumber[0].replace('Z','')), float(Dnumber[0].replace('D',''))])
    def Thround(self,column, cell, model, iter):
        origstr = cell.get_property('text')
        sizestr = round(float(origstr),3)
        cell.set_property('text', sizestr) 
        return  sizestr       
           

# Ввод координат окончание
    def end_coordinate(self,widget,new_text):
        if (widget.get_editable()==False):
            return
        X_coor=float(self.builder.get_object("label17").get_text())
        Y_coor=float(self.builder.get_object("label18").get_text())
        Z_coor=float(self.builder.get_object("label39").get_text())
        Cur_coord=0
        axis_number=0
        if (widget==self.builder.get_object("entry2")):
            Cur_coord=X_coor
            axis_number=0
        elif (widget==self.builder.get_object("entry3")):
            Cur_coord=Y_coor
            axis_number=1   
        elif (widget==self.builder.get_object("entry4")):
            Cur_coord=Z_coor
            axis_number=2
        widget.set_text(str(Cur_coord+float(widget.get_text())))
    
        self.SetAxis(axis_number,float(widget.get_text()))
#        print(gtk.Buildable.get_name(widget))


# Редактор инструмента
    def save_reload_tool_table(self):
        with open(self.tool_file,'w') as output:
            for el in self.liststore:
                Tool_STR = 'T'+str(el[0])+" P"+str(el[0])+" Z"+str(el[1])+" D"+str(el[2])+'\n' 
                output.write(Tool_STR)
        self.command.load_tool_table()        

    def editTable(self, widget, row, new_text, model, column):
          iter = model.get_iter(row)
          model.set_value(iter, column, float(new_text))

    def editToolTable(self, widget, row, new_text, model, column):
          iter = self.liststore.get_iter(row)
          self.liststore.set_value(iter, column, float(new_text))
          if len(self.liststore)>0:
            self.save_reload_tool_table()

    def timelock(self):
        gobject.timeout_add(100, self.periodic) 

    def godeTosrting(self,tuplecode,litera,dop):
        gcodestext=''
        i=0
        for (gcod) in tuplecode:
            if(gcod*dop>0):
                if (i==5):
                    gcodestext=gcodestext+'\n' 
                    i=0
                codd=math.modf(gcod*dop)
                if (codd[0]>0):
                    gcodestext=gcodestext+litera+'%.1f'%(gcod*dop)+', '
                else:
                    gcodestext=gcodestext+litera+'%d'%int(gcod*dop)+', ' 
                i=i+1
        if (litera=='M' and tuplecode.index(0)>=0): 
            gcodestext=gcodestext+litera+'0'+', '       

        return  gcodestext       


    def move_cursor(self,treeview, step, count):
        path, column1 = treeview.get_cursor()        
        treeview.set_cursor(path, column1, start_editing = True)
        # self.treeview.grab_focus() # Если не убрать, то не работает
        return True # Чтобы не обрабатывался дальше Tab


#        path, column = treeview.get_cursor()
#        treeview.set_cursor(path, column, start_editing = True)
#        print path
#        print column
#        print step
#        print count
#        area = treeview.row_activated(path,column) 
#        print area
#        if (column != None): 
#            treeview.set_cursor(path, column, start_editing = True)
#        treeview.set_cursor_on_cell(path, column, ,True)


    def periodic(self): # обновляем значения интерфейса
# обновляем параметры на форме
        self.status.poll()
        GcodeView=self.builder.get_object("textview4").get_buffer()
        GcodeView.set_text(self.godeTosrting(self.status.gcodes,'G',0.1))
        McodeView=self.builder.get_object("textview5").get_buffer()
        McodeView.set_text(self.godeTosrting(self.status.mcodes,'M',1))
        self.builder.get_object("label24").set_label('T'+str(self.status.tool_in_spindle))
        self.builder.get_object("label25").set_label('S'+str(int(self.status.spindle_speed)))
        self.builder.get_object("label26").set_label('F'+str(int(self.status.feedrate)))
        tgg=os.path.split(self.status.file)
        self.builder.get_object("ProgName1").set_label(tgg[1])
        pos=self.status.actual_position
        posOff = self.status.g5x_offset
        self.builder.get_object("label35").set_text('%.3f'%(posOff[0]+pos[0]))
        self.builder.get_object("label36").set_text('%.3f'%(posOff[1]+pos[1]))
        self.builder.get_object("label37").set_text('%.3f'%(posOff[2]+pos[2]))
        
#        self.builder.get_object("label17").set_text('%.3f'%(pos[0]))
#        self.builder.get_object("label18").set_text('%.3f'%(pos[1]))
#        self.builder.get_object("label39").set_text('%.3f'%(pos[2]))

   #     self.Set_Big_Fat(self.builder.get_object("label17"))
   #     self.Set_Big_Fat(self.builder.get_object("label18"))
   #     self.Set_Big_Fat(self.builder.get_object("label39"))

        self.Set_Big_Fat(self.builder.get_object("label35"))
        self.Set_Big_Fat(self.builder.get_object("label36"))
        self.Set_Big_Fat(self.builder.get_object("label37"))
# канал ошибок
        error = self.error_channel.poll()
        if error:
           kind, text = error
           if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
            typus = "error"
            parent = None
            md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, text)
            md.run()
            md.destroy()
            print typus, text 
           else:
            typus = "info"
            print text 
        gobject.timeout_add(100, self.periodic)
    
    def Set_Big_Fat(self,widget):
        widget.set_use_markup(gtk.TRUE)
        widget.set_markup('<span font="40" font_weight="heavy">'+widget.get_text()+'</span>')
    
    def set_color_connect(self,widget):
        style = self.builder.get_object("f1").get_style().copy()
        style.bg[gtk.STATE_NORMAL] = self.builder.get_object("colorbutton1").get_color()
        self.color_button_style=style
        self.color_text_style=self.builder.get_object("colorbutton2").get_color()
        self.ConfigParser.read(self.color_path)
        self.ConfigParser.set('DISPLAY', 'COLOR_BUTTON',self.builder.get_object("colorbutton1").get_color().to_string())
        self.ConfigParser.set('DISPLAY', 'COLOR_TEXT',self.builder.get_object("colorbutton2").get_color().to_string())
        with open(self.color_path, 'w') as configfile:
            self.ConfigParser.write(configfile)


    def Set_Font_Text_Button(self,widget,text):
        obj=self.builder.get_object(widget)
        obj.set_label(text)
        for widget2 in obj.get_children(): 
            if (isinstance(widget2, gtk.Label)):
                widget2.set_justify(gtk.JUSTIFY_CENTER)
#+ установим цвет кнопочек
        obj.set_style(self.color_button_style)
        obj.get_children()[0].modify_fg(gtk.STATE_NORMAL, self.color_text_style)                


    def on_textview3_move_cursor(self, widget,MovementStepU,intparam,boolparam):
        global last_position
        if isSelect:
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.remove_tag_by_name("Selected",self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(last_position))
            self.textbuffer.apply_tag_by_name("Selected",self.textbuffer.get_iter_at_offset(first_position),self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position))
            last_position = self.textbuffer.props.cursor_position
#       print (self.textbuffer.props.cursor_position)
    def set_color_button(self):
        self.builder.get_object("f3").set_style(self.default_style_button)
        self.builder.get_object("f4").set_style(self.default_style_button)
        self.builder.get_object("f5").set_style(self.default_style_button)
        self.builder.get_object('hidenButton').hide()
        if (self.jog_distance==0.001):
            self.builder.get_object("f3").set_style(self.gren_style_button) 
            self.builder.get_object('hidenButton').show()
        if (self.jog_distance==0.01):
            self.builder.get_object("f4").set_style(self.gren_style_button) 
            self.builder.get_object('hidenButton').show()
        if (self.jog_distance==0.1):
            self.builder.get_object("f5").set_style(self.gren_style_button)
            self.builder.get_object('hidenButton').show()
    def set_color_button_G_5x(self,widget):
            self.builder.get_object("f1").set_style(self.default_style_button)
            self.builder.get_object("f2").set_style(self.default_style_button)
            self.builder.get_object("f3").set_style(self.default_style_button)
            self.builder.get_object("f4").set_style(self.default_style_button)
            self.builder.get_object("f5").set_style(self.default_style_button)
            self.builder.get_object("f6").set_style(self.default_style_button)
            print self.builder.get_object("notebook1").get_current_page()
            if (self.builder.get_object("notebook1").get_current_page()==3):
                widget.set_style(self.gren_style_button)
    def Jog_Operation(self, widget):
        NameButton = widget.get_label()
        NameButton =NameButton.translate(None, string.whitespace)
        if (NameButton=="x+"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 0, 5, self.jog_distance)
        if (NameButton=="x-"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 0, 5, -self.jog_distance)
        if (NameButton=="y+"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 1, 5, self.jog_distance) 
        if (NameButton=="y-"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 1, 5, -self.jog_distance) 
        if (NameButton=="z+"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 2, 5, self.jog_distance) 
        if (NameButton=="z-"):
            self.command.jog(linuxcnc.JOG_INCREMENT, 2, 5, -self.jog_distance) 
    
    def MDI_Click_button(self, widget):
        NameButton = widget.get_label()
        if (NameButton.translate(None, string.whitespace).find('F1Выполнить')==0):   
           self.command.mode(linuxcnc.MODE_MDI)           
           buff=self.builder.get_object("textview6").get_buffer()
           self.command.mdi(buff.get_text(buff.get_start_iter(),buff.get_end_iter()))
           self.command.mode(linuxcnc.MODE_MANUAL) 
           self.builder.get_object("textview6").grab_focus();
           self.MDIWindows.hide()
        elif (NameButton.translate(None, string.whitespace).find('F2Отмена')==0): 
            self.MDIWindows.hide()
        elif (NameButton.translate(None, string.whitespace).find('F3Удалитьсимвол')==0):
            buff=self.builder.get_object("textview6").get_buffer()
            txtB=buff.get_text(buff.get_start_iter(),buff.get_end_iter())
            buff.set_text(txtB[0:len(txtB)-1])
    def SetAxis(self,axis,value):
            d = {0: 'x', 1: 'y', 2:'z'}
            m = "G10 L20 P0 %s%f"%(d[axis],value)
            self.command.mode(linuxcnc.MODE_MDI)
            self.command.mdi(m)

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
            self.builder.get_object("entry1").grab_focus(); 
            findtext=self.builder.get_object("entry1").get_text()
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            textToFind=self.textbuffer.get_text(self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position), self.textbuffer.get_iter_at_offset(self.textbuffer.get_char_count()), True)
            index=textToFind.find(findtext)
            if (index>-1):
                self.textbuffer.remove_all_tags(self.textbuffer.get_iter_at_offset(0),self.textbuffer.get_iter_at_offset(self.textbuffer.get_char_count()))
                self.textbuffer.apply_tag(self.Tag,self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index),self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index+len(findtext)))
                self.textbuffer.select_range(self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index), self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index))
                self.findwindow.hide()
                self.builder.get_object("textview3").scroll_to_iter (self.textbuffer.get_iter_at_offset(self.textbuffer.props.cursor_position+index), 0.0, False, 0, 0);
            else:
                self.findwindow.hide()
                parent = None
                md = gtk.MessageDialog(parent, 
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                gtk.BUTTONS_CLOSE, "Ничего не найдено")
                md.run()
                md.destroy()
            self.builder.get_object("textview3").grab_focus();    
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
                self.command.program_open(dialog.get_filename())
#                print dialog.get_filename(), 'selected'
#            elif response == gtk.RESPONSE_CANCEL:
#                print 'Closed, no files selected'
            dialog.destroy()
        elif (NameButton.translate(None, string.whitespace).find('F8Выход')==0):
            gtk.main_quit()
        elif (NameButton.translate(None, string.whitespace).find('F7Test')==0):
#            self.command.home(0)
#            self.command.wait_complete(5)
#            self.command.home(1)
#            self.command.wait_complete(5)
#            self.command.home(2)
#            self.command.wait_complete(5)
            print self.machine_status
        elif (NameButton.translate(None, string.whitespace).find('F1СменитьВид')==0):
            index = self.type_gremlin_view.index(self.gremlin.get_property('view'))+1
            if (index>3):
                index=0
            self.gremlin.set_property('view',self.type_gremlin_view[index])
        elif (NameButton.translate(None, string.whitespace).find('F2ВключитьВыключитьDRO')==0):
            if (self.gremlin.get_property('enable_dro')==0):
                self.gremlin.set_property('use_commanded',(1))
                self.gremlin.set_property('use_relative',(1))
                self.gremlin.set_property('show_dtg',(1))
                self.gremlin.set_property('enable_dro',(1))
            else:
                self.gremlin.set_property('show_dtg',(0))
                self.gremlin.set_property('use_commanded',(0))
                self.gremlin.set_property('use_relative',(0))
                self.gremlin.set_property('enable_dro',(0))
        elif (NameButton.translate(None, string.whitespace).find('F3Приблизить')==0):
            self.gremlin.zoom_in()
        elif (NameButton.translate(None, string.whitespace).find('F4Удалить')==0):
            self.gremlin.zoom_out()
        elif (NameButton.translate(None, string.whitespace).find('F5Вправо')==0):
            self.gremlin_x=self.gremlin_x+5
            self.gremlin_y=self.gremlin_y
            self.gremlin.pan(self.gremlin_x,self.gremlin_y)
        elif (NameButton.translate(None, string.whitespace).find('F6Лево')==0):
            self.gremlin_x=self.gremlin_x-5
            self.gremlin_y=self.gremlin_y
            self.gremlin.pan(self.gremlin_x,self.gremlin_y)
        elif (NameButton.translate(None, string.whitespace).find('F7Вверх')==0):
            self.gremlin_x=self.gremlin_x
            self.gremlin_y=self.gremlin_y+5
            self.gremlin.pan(self.gremlin_x,self.gremlin_y)
        elif (NameButton.translate(None, string.whitespace).find('F8Вниз')==0):
            self.gremlin_x=self.gremlin_x
            self.gremlin_y=self.gremlin_y-5
            self.gremlin.pan(self.gremlin_x,self.gremlin_y)
        elif (NameButton.translate(None, string.whitespace).find('F3Вставить(')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.insert_at_cursor('(')
        elif (NameButton.translate(None, string.whitespace).find('F4Вставить)')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.insert_at_cursor(')')        
        elif (NameButton.translate(None, string.whitespace).find('F5Вставить.')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.insert_at_cursor('.')        
        elif (NameButton.translate(None, string.whitespace).find('F6Вставить,')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.insert_at_cursor(',')        
        elif (NameButton.translate(None, string.whitespace).find('F7Вставить+')==0):
            self.textbuffer = self.builder.get_object("textview3").get_buffer()
            self.textbuffer.insert_at_cursor('+')
        elif (NameButton.translate(None, string.whitespace).find('F7Вставить')==0): 
            isSelect=False
            self.textbuffer = self.builder.get_object("textview3").get_buffer() 
            self.textbuffer.paste_clipboard(gtk.clipboard_get("CLIPBOARD"),None,True)
        elif (NameButton.translate(None, string.whitespace).find('F30.001')==0): 
            if(self.jog_distance==0.001):
                self.jog_distance=0
            else:    
                self.jog_distance=0.001
            self.set_color_button()
        elif (NameButton.translate(None, string.whitespace).find('F40.01')==0): 
            if(self.jog_distance==0.01):
                self.jog_distance=0
            else:    
                self.jog_distance=0.01
            self.set_color_button()
        elif (NameButton.translate(None, string.whitespace).find('F50.1')==0): 
            if(self.jog_distance==0.1):
                self.jog_distance=0
            else:    
                self.jog_distance=0.1
            self.set_color_button()
        elif (NameButton.translate(None, string.whitespace).find('F6Вращениешпинделявправо')==0):
            self.command.spindle(linuxcnc.SPINDLE_FORWARD)

        elif (NameButton.translate(None, string.whitespace).find('F7Стопшпиндель')==0):
            self.command.spindle(linuxcnc.SPINDLE_OFF)

        elif (NameButton.translate(None, string.whitespace).find('F8Вращениешпинделявлево')==0):
            self.command.spindle(linuxcnc.SPINDLE_REVERSE)
        
        elif (NameButton.translate(None, string.whitespace).find('F1MDIРучнойнабор')==0):
            self.MDIWindows = self.builder.get_object("MDI")
            self.MDIWindows.set_default_size(300,300)
            self.builder.get_object("vbox23").modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse("#000000"))


            self.Set_Font_Text_Button('button1','F1 \nВыполнить\n')
            self.Set_Font_Text_Button('button2','F2 \nОтмена\n')
            self.Set_Font_Text_Button('button3','F3 \nУдалить символ\n')            
            self.MDIWindows.show()
            self.builder.get_object("textview6").grab_focus();
        elif (NameButton.translate(None, string.whitespace).find('F1Активироватьтекущею')==0):
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            self.command.mode(linuxcnc.MODE_MDI)
            self.command.mdi(model.get_value(model.get_iter(path),0))
        elif (NameButton.translate(None, string.whitespace).find('F2Проставитьтекущие')==0):
            self.status.poll()
            pos=self.status.actual_position
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            model.set_value(model.get_iter(path),1,pos[0])
            model.set_value(model.get_iter(path),2,pos[1])
            model.set_value(model.get_iter(path),3,pos[2])
        elif (NameButton.translate(None, string.whitespace).find('F3Прибавитьктекущим')==0):
            self.status.poll()
            pos=self.status.actual_position
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            model.set_value(model.get_iter(path),1,model.get_value(model.get_iter(path),1)+pos[0])
            model.set_value(model.get_iter(path),2,model.get_value(model.get_iter(path),2)+pos[1])
            model.set_value(model.get_iter(path),3,model.get_value(model.get_iter(path),3)+pos[2])    
        elif (NameButton.translate(None, string.whitespace).find('F4Вычестьизтекущих')==0):
            self.status.poll()
            pos=self.status.actual_position
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            model.set_value(model.get_iter(path),1,model.get_value(model.get_iter(path),1)-pos[0])
            model.set_value(model.get_iter(path),2,model.get_value(model.get_iter(path),2)-pos[1])
            model.set_value(model.get_iter(path),3,model.get_value(model.get_iter(path),3)-pos[2]) 
        elif (NameButton.translate(None, string.whitespace).find('F5Записатьтекущеюстроку')==0):
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            self.command.mdi(model.get_value(model.get_iter(path),0))
            self.SetAxis(0,model.get_value(model.get_iter(path),1))
            self.SetAxis(1,model.get_value(model.get_iter(path),2))
            self.SetAxis(2,model.get_value(model.get_iter(path),3))
        elif (NameButton.translate(None, string.whitespace).find('F6Записатьтаблицу')==0):
            path, column1 = self.treeview3.get_cursor()        
            model =self.treeview3.get_model()
            self.command.mode(linuxcnc.MODE_MDI)
            for row in model:
                self.command.mdi(row[0])
                self.SetAxis(0,row[1])
                self.SetAxis(1,row[2])
                self.SetAxis(2,row[3])

        elif (NameButton.translate(None, string.whitespace).find('F4Допклавиши')==0): 
            self.Set_Font_Text_Button('f1','F1\nВыбор файла\nпрограммы')
            self.Set_Font_Text_Button('f2','F2\nПоиск')
            self.Set_Font_Text_Button('f3','F3\nВставить\n (')
            self.Set_Font_Text_Button('f4','F4\nВставить\n )')
            self.Set_Font_Text_Button('f5','F5\nВставить\n .')
            self.Set_Font_Text_Button('f6','F6\nВставить\n ,')
            self.Set_Font_Text_Button('f7','F7\nВставить\n +')
            self.Set_Font_Text_Button('f8','F8\nНазад\nв редактор')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(5)
            self.builder.get_object("textview3").grab_focus();
        elif (NameButton.translate(None, string.whitespace).find('F3ФункцииРедактора')==0): 
            self.Set_Font_Text_Button('f1','F1\nВыбор файла\nпрограммы')
            self.Set_Font_Text_Button('f2','F2\nПоиск')
            self.Set_Font_Text_Button('f3','F3\nНачать\nвыделение')
            self.Set_Font_Text_Button('f4','F4\nЗакончить\nвыделение')
            self.Set_Font_Text_Button('f5','F5\nСкопировать\n')
            self.Set_Font_Text_Button('f6','F6\nВырезать\n ')
            self.Set_Font_Text_Button('f7','F7\nВставить\n')
            self.Set_Font_Text_Button('f8','F8\nНазад\nв редактор')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(5)
            self.builder.get_object("textview3").grab_focus(); 
        elif (NameButton.translate(None, string.whitespace).find('F5Редакторпрограмм')==0 or NameButton.translate(None, string.whitespace).find('F8Назадвредактор')==0):
            self.Set_Font_Text_Button('f1','F1\nВыбор файла\nпрограммы')
            self.Set_Font_Text_Button('f2','F2\nПоиск')
            self.Set_Font_Text_Button('f3','F3\nФункции\nРедактора')
            self.Set_Font_Text_Button('f4','F4\nДоп\nклавиши')
            self.Set_Font_Text_Button('f5','F5\nСохранить\nпрограмму')
            self.Set_Font_Text_Button('f6','F6\n\n ')
            self.Set_Font_Text_Button('f7','F7\n\n')
            self.Set_Font_Text_Button('f8','F8\nГрафика\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(5)
            self.builder.get_object("textview3").grab_focus(); 
        elif (NameButton.translate(None, string.whitespace).find('F7Сервис')==0):
            self.Set_Font_Text_Button('f1','F1\n\n')
            self.Set_Font_Text_Button('f2','F2\n\n')
            self.Set_Font_Text_Button('f3','F3\n\n')
            self.Set_Font_Text_Button('f4','F4\n\n')
            self.Set_Font_Text_Button('f5','F5\n\n')
            self.Set_Font_Text_Button('f6','F6\n\n')
            self.Set_Font_Text_Button('f7','F7\n Test\n')
            self.Set_Font_Text_Button('f8','F8\nВыход\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(7)    
        elif (NameButton.translate(None, string.whitespace).find('F6Графика')==0 or NameButton.translate(None, string.whitespace).find('F8Графика')==0):
            self.Set_Font_Text_Button('f1','F1\nСменить\nВид')
            self.Set_Font_Text_Button('f2','F2\nВключить\nВыключить DRO')
            self.Set_Font_Text_Button('f3','F3\nПриблизить\n ')
            self.Set_Font_Text_Button('f4','F4\nУдалить\n ')
            self.Set_Font_Text_Button('f5','F5\nВправо\n ')
            self.Set_Font_Text_Button('f6','F6\nЛево\n ')
            self.Set_Font_Text_Button('f7','F7\nВверх\n ')
            self.Set_Font_Text_Button('f8','F8\nВниз\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(6)   
        elif (NameButton.translate(None, string.whitespace).find('F1РучноеУправление')==0):
            self.Set_Font_Text_Button('f1','F1\nMDI\nРучной набор')
            self.Set_Font_Text_Button('f2','F2\nМаховичок\n')
            self.Set_Font_Text_Button('f3','F3\n0.001\n ')
            self.Set_Font_Text_Button('f4','F4\n0.01\n ')
            self.Set_Font_Text_Button('f5','F5\n0.1\n')
            self.Set_Font_Text_Button('f6','F6\nВращение\nшпинделя\nвправо')
            self.Set_Font_Text_Button('f7','F7\nСтоп\nшпиндель')
            self.Set_Font_Text_Button('f8','F8\nВращение\nшпинделя\nвлево')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(0)        
        elif (NameButton.translate(None, string.whitespace).find('F4Коррекцияинструмента')==0):
            self.Set_Font_Text_Button('f1','F1\n\n')
            self.Set_Font_Text_Button('f2','F2\n\n')
            self.Set_Font_Text_Button('f3','F3\n\n ')
            self.Set_Font_Text_Button('f4','F4\n\n ')
            self.Set_Font_Text_Button('f5','F5\n\n')
            self.Set_Font_Text_Button('f6','F6\n\n')
            self.Set_Font_Text_Button('f7','F7\n\n')
            self.Set_Font_Text_Button('f8','F8\n\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(4)   
        elif (NameButton.translate(None, string.whitespace).find('F3НольДетали')==0):
            self.Set_Font_Text_Button('f1','F1\nАктивировать\nтекущею')
            self.Set_Font_Text_Button('f2','F2\nПроставить\nтекущие')
            self.Set_Font_Text_Button('f3','F3\nПрибавить к\nтекущим')
            self.Set_Font_Text_Button('f4','F4\nВычесть из\nтекущих')
            self.Set_Font_Text_Button('f5','F5\nЗаписать\nтекущею строку')
            self.Set_Font_Text_Button('f6','F6\nЗаписать\nтаблицу')
            self.Set_Font_Text_Button('f7','F7\n\n')
            self.Set_Font_Text_Button('f8','F8\n\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(3)
#            self.builder.get_object("f1").set_style(self.gren_style_button)  
#            self.curr_coordinate='G54'
        elif (NameButton.translate(None, string.whitespace).find('F8Система')==0):
            self.Set_Font_Text_Button('f1','F1\n\n')
            self.Set_Font_Text_Button('f2','F2\n\n')
            self.Set_Font_Text_Button('f3','F3\n\n')
            self.Set_Font_Text_Button('f4','F4\n\n')
            self.Set_Font_Text_Button('f5','F5\n\n')
            self.Set_Font_Text_Button('f6','F6\n\n')
            self.Set_Font_Text_Button('f7','F7\n\n')
            self.Set_Font_Text_Button('f8','F8\n\n')
            self.Set_Font_Text_Button('f9','\nГлавное\nменю')
            self.builder.get_object("notebook1").set_current_page(8)
        else:
            self.jog_distance=0
            self.set_color_button()
            self.Set_Font_Text_Button('f1','F1\nРучное\nУправление')
            self.Set_Font_Text_Button('f2','F2\nAUTO\n')
            self.Set_Font_Text_Button('f3','F3\nНоль\nДетали')
            self.Set_Font_Text_Button('f4','F4\nКоррекция\nинструмента')
            self.Set_Font_Text_Button('f5','F5\nРедактор\nпрограмм')
            self.Set_Font_Text_Button('f6','F6\nГрафика\n')
            self.Set_Font_Text_Button('f7','F7\nСервис\n')
            self.Set_Font_Text_Button('f8','F8\nСистема\n')
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
    
#    def helloWorld(self, widget):
#       gtk.main_quit()
#         print(self)
#         print(widget)
#         self.glade.get_object("label1").set_text('Ебана в рот')
        

if __name__ == "__main__":
    hwg = HellowWorldGTK()
    gtk.main()    
