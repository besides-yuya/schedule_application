# -*- coding:utf-8 -*-

import Tkinter as tk
import os
from subprocess import Popen
import ttk

# カレンダーを作成するフレームクラス
class mycalendar(tk.Frame):
    def __init__(self,master=None,cnf={},**kw):
        "初期化メソッド"
        import datetime
        tk.Frame.__init__(self,master,cnf,**kw)
        
        # 現在の日付を取得
        self.now = datetime.datetime.now()
        # 現在の年と月を属性に追加
        self.year = self.now.year
        self.month = self.now.month

        self.filename = None
        self.files = None
        self.folderpath = None
        self.pressedbutton = None

        # プレビューを開く部分の作成
        self.frame_preview = tk.Frame(self)
        self.frame_preview.pack(side = tk.RIGHT)
        self.preview_label = tk.Label(self.frame_preview, text = "Preview", font = ("",14))
        self.preview_label.pack()
        self.preview_widget = tk.Text(self.frame_preview)
        self.preview_widget.pack(padx = 10)

        # frame_top部分の作成
        frame_top = tk.Frame(self)
        frame_top.pack()
        self.previous_month = tk.Label(frame_top, text = "<", font = ("",14))
        self.previous_month.bind("<1>",self.change_month)
        self.previous_month.pack(side = "left", padx = 10)
        self.current_year = tk.Label(frame_top, text = self.year, font = ("",18))
        self.current_year.pack(side = "left")
        self.current_month = tk.Label(frame_top, text = self.month, font = ("",18))
        self.current_month.pack(side = "left")
        self.next_month = tk.Label(frame_top, text = ">", font = ("",14))
        self.next_month.bind("<1>",self.change_month)
        self.next_month.pack(side = "left", padx = 10)

        # frame_week部分の作成
        frame_week = tk.Frame(self)
        frame_week.pack()
        button_mon = d_button(frame_week, text = "Mon")
        button_mon.grid(column=0,row=0)
        button_tue = d_button(frame_week, text = "Tue")
        button_tue.grid(column=1,row=0)
        button_wed = d_button(frame_week, text = "Wed")
        button_wed.grid(column=2,row=0)
        button_thu = d_button(frame_week, text = "Thu")
        button_thu.grid(column=3,row=0)
        button_fri = d_button(frame_week, text = "Fri")
        button_fri.grid(column=4,row=0)
        button_sta = d_button(frame_week, text = "Sat", fg = "blue")
        button_sta.grid(column=5,row=0)
        button_san = d_button(frame_week, text = "San", fg = "red")
        button_san.grid(column=6,row=0)

        # frame_calendar部分の作成
        self.frame_calendar = tk.Frame(self)
        self.frame_calendar.pack()

        # 押された日にちのフォルダにあるファイルをリストとして表示する部分の作成
        self.frame_list = tk.Frame(self)
        self.frame_list.pack(padx = 10)
        self.list_widget = tk.Listbox(self.frame_list, width = 60)
        self.list_widget.bind("<Button-3>",self.preview_file)
        self.list_widget.bind("<Double-Button-1>",self.open_file)
        self.list_widget.pack(pady=10)

        # 押された日にちのフォルダを開く部分の作成
        self.frame_open = tk.Frame(self)
        self.frame_open.pack()
        self.button_open = tk.Button(self.frame_open, text = "open folder",command=self.open_folder)
        #self.button_open.grid(column=1,row=0)
        self.button_open.grid(column=2, row=0, padx=10, pady=5)

        # 日付部分を作成するメソッドの呼び出し
        self.create_calendar(self.year,self.month)


    def create_calendar(self,year,month):
        "指定した年(year),月(month)のカレンダーウィジェットを作成する"

        # ボタンがある場合には削除する（初期化）
        try:
            for key,item in self.day.items():
                item.destroy()
        except:
            pass
            
        # calendarモジュールのインスタンスを作成
        import calendar
        cal = calendar.Calendar()
        # 指定した年月のカレンダーをリストで返す
        days = cal.monthdayscalendar(year,month)

        # 日付ボタンを格納する変数をdict型で作成
        self.day = {}
        self.date_label = {}
        # for文を用いて、日付ボタンを生成
        for i in range(0,42):
            c = i - (7 * int(i/7))
            r = int(i/7)
            try:
                # 日付が0でなかったら、ボタン作成
                if days[r][c] != 0:
##                    self.date_label[i] = str(year)+str(month)+str(days[r][c])
                    self.date_label[i] = '{0}'.format(year)+'{0:02d}'.format(month)+'{0:02d}'.format(days[r][c])
#                    self.day[i] = d_button(self.frame_calendar,text = days[r][c],command=self.display_contents(self.date_label[i]))
                    self.day[i] = ttk.Button(self.frame_calendar,width=6, text = days[r][c],command=self.display_contents(i,self.date_label[i]))
                    #self.day[i].bind("<Button-1>", self.change_state(i))
                    #self.day[i] = d_button(self.frame_calendar,text = days[r][c])
                    self.day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break

    def change_state(self,i):
        if not self.pressedbutton == None:
            self.pressedbutton.state(['!pressed'])
        self.day[i].state(['pressed'])
        self.pressedbutton = self.day[i]
##        for ii in self.day:
##            self.day[ii].state(['!pressed'])
        
    
    def change_month(self,event):
        #押されたボタンのリセット
        self.pressedbutton = None
        # 押されたラベルを判定し、月の計算
        if event.widget["text"] == "<":
            self.month -= 1
        else:
            self.month += 1
        # 月が0、13になったときの処理
        if self.month == 0:
            self.year -= 1
            self.month = 12
        elif self.month == 13:
            self.year +=1
            self.month =1
        # frame_topにある年と月のラベルを変更する
        self.current_year["text"] = self.year
        self.current_month["text"] = self.month
        # 日付部分を作成するメソッドの呼び出し
        self.create_calendar(self.year,self.month)

    def display_contents(self,i,label):
        def x():
            self.change_state(i)

##            self.filename = 'スケジュール/'+label+'.txt'
            self.folderpath = 'schedules\\'+label+'\\'
            if not os.path.isdir(self.folderpath):
                os.mkdir(self.folderpath)
            self.files = os.listdir(self.folderpath)
            self.files.sort()
            self.list_widget.delete(0,tk.END)
#            self.text_widget.delete('1.0','end')
            for file in self.files:
                self.list_widget.insert(tk.END,file.decode('shift_jis'))
##                self.list_widget.insert(tk.END,file.decode('shift_jis')+'\r\n')
        return x

    def open_folder(self):
        if self.folderpath == None:
            return
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = abs_path+'\\'+self.folderpath
        proc = Popen(['explorer',path.encode('shift_jis')],shell=True)
        proc.wait()

    def open_file(self,event):
        self.filename = self.list_widget.get(tk.ACTIVE)
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = abs_path+'\\'+self.folderpath+'\\'+self.filename
        proc = Popen(['start',path.encode('shift_jis')],shell=True)
        proc.wait()

    def preview_file(self,event):
        self.filename = self.list_widget.get(tk.ACTIVE)
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = abs_path+'\\'+self.folderpath+'\\'+self.filename
        self.preview_widget.delete('1.0','end')
        f = open(path.encode('shift_jis'),'r')
        for i in f:
##            self.preview_widget.insert('1.0',i.decode('shift_jis')+'\r\n')
            try:
                self.preview_widget.insert(tk.END,i.decode('shift_jis'))
            except:
                self.preview_widget.insert(tk.END,i)

        
# デフォルトのボタンクラス
class d_button(tk.Button):
    def __init__(self,master=None,cnf={},**kw):
        tk.Button.__init__(self,master,cnf,**kw)
        self.configure(font=("",14),height=2, width=4, relief="flat")

if __name__=='__main__':
    # ルートフレームの定義      
    root = tk.Tk()
    root.title("Calendar App")
    mycal = mycalendar(root)
    mycal.pack()
    root.mainloop()
