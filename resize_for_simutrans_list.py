import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os


class resize_for_simutrans():
    def __init__(self, input_file, output_file, beforesize, aftersize, how=0):
        self.input=input_file
        self.output=output_file
        self.before=int(beforesize)
        self.after=int(aftersize)
        self.how=how
    def flag(self):
        if os.path.isfile(self.input)==False:
            return 0
        else:
            imge = Image.open(self.input)
            print(imge.mode)
            im = np.array(imge)
            print(im.shape)
            imX = im.shape[0]
            imY = im.shape[1]
            if imge.mode == "RGBA":
                #f=open("img.txt","w")
                #for i in range(self.before):
                #    f.write("[")
                #    for j in range(self.before):
                #        f.write(str(im[i,j])+",")
                #    f.write("]\n")
                #f.close()
                #return 2
                modemode=2
            elif imge.mode=="RGB":
                modemode=0
            if imge.mode=="P":
                modemode=1
            print(im[0,0])
            if imX % self.before == 0 and imY % self.before == 0 and self.before>0 and self.after>0:
                output=Image.fromarray(resize_program(im,self.before,self.after,self.how,modemode))
                output.save(self.output)
                return 1
            else: 
                return 2

def resize_program(inimg,beforesize,aftersize,how,mode):
    def merge(inimg,inX,inY,inrangeX,inrangeY):
        color = np.array([0.0,0.0,0.0])
        count = 0.0
        if special_color(inimg[int(inX),int(inY)])=="Special_color":
            return inimg[int(inX),int(inY)]
        for k in range(int(-inrangeX/2.0+inX),int(inrangeX/2.0+inX+0.99)):
            for l in range(int(-inrangeY/2.0+inY-0.99),int(inrangeY/2.0+inY+0.99)):
                #print(inimg[k,l])
                if 0<= k< inimg.shape[0] and 0<= l< inimg.shape[1]:
                    if reduce_color(inimg[k,l])!="False" and special_color(inimg[k,l])!="Special_color":
                        thiscount=np.abs((-max(k,inX-inrangeX/2.0)+min(k+1,inX+inrangeX/2.0))*(-max(l,inY-inrangeY/2.0)+min(l+1,inY+inrangeY/2.0)))
                        color=color+inimg[k,l]*thiscount
                        #print(inimg[k,l],color,k,l)
                        count = count+thiscount
        if count==0.0:
            return inimg[int(inX),int(inY)]
        else:
            result = color/count
            return result
    def merge_mode2(inimg,inX,inY,inrangeX,inrangeY):
        color = np.array([0.0,0.0,0.0,0.0])
        count = 0.0
        for k in range(int(-inrangeX/2.0+inX),int(inrangeX/2.0+inX+0.99)):
            for l in range(int(-inrangeY/2.0+inY-0.99),int(inrangeY/2.0+inY+0.99)):
                #print(inimg[k,l])
                if 0<= k< inimg.shape[0] and 0<= l< inimg.shape[1]:
                    if reduce_color_2(inimg[k,l])!="False":
                        thiscount=np.abs((-max(k,inX-inrangeX/2.0)+min(k+1,inX+inrangeX/2.0))*(-max(l,inY-inrangeY/2.0)+min(l+1,inY+inrangeY/2.0)))
                        color=color+inimg[k,l]*thiscount
                        #print(inimg[k,l],color,k,l)
                        count = count+thiscount
        if count==0.0:
            return inimg[int(inX),int(inY)]
        else:
            result = color/count
            return result
    def merge_mode1(inimg,inX,inY,inrangeX,inrangeY):
        color = 0.0
        count = 0.0
        for k in range(int(-inrangeX/2.0+inX),int(inrangeX/2.0+inX+0.99)):
            for l in range(int(-inrangeY/2.0+inY-0.99),int(inrangeY/2.0+inY+0.99)):
                #print(inimg[k,l])
                if 0<= k< inimg.shape[0] and 0<= l< inimg.shape[1]:
                    if inimg[k,l]!=234:
                        thiscount=(-max(k,inX-inrangeX/2.0)+min(k+1,inX+inrangeX/2.0))*(-max(l,inY-inrangeY/2.0)+min(l+1,inY+inrangeY/2.0))
                        color=color+inimg[k,l]*thiscount
                        #print(inimg[k,l],color,k,l)
                        count = count+thiscount
        if count==0.0:
            return inimg[int(inX),int(inY)]
        else:
            result = color/count
            result = result.astype(np.uint8)
            if special_color(result)=="Special_color":
                result[0]=result[0]-(result[0]-123.5)/np.abs(result[0]-123.5)
                result=result.astype(np.unit8)
            return result
    def reduce_color(input):
        if (input==np.array([231,255,255])).all()==True:
            return "False"
        else:
            return "True"
    def special_color(input):
        special_color_list=np.array([[107,107,107],[155,155,155],[179,179,179],[201,201,201],[223,223,223],[127,155,241],[255,255,83],[255,33,29],[1,221,1],[227,227,255],[193,177,209],[77,77,77],[255,1,127],[1,1,255],[36,75,103],[57,94,124],[76,113,145],[96,132,167],[116,151,189],[136,171,211],[156,190,233],[176,210,255],[123,88,3],[142,111,4],[161,134,5],[180,157,7],[198,180,8],[217,203,10],[236,226,11],[255,249,13]])
        for i in range(len(special_color_list)):
            if np.array_equal(input,special_color_list[i]):
                return "Special_color"
                break
        return "usual_color"
    def reduce_color_2(input):
        if (input==np.array([231,255,255,255])).all()==True:
            return "False"
        else:
            return "True"
    def resize(beforesize,aftersize,how):
        if beforesize>aftersize and how==0:
            rinX=beforesize/aftersize
            rinY=beforesize/aftersize
        elif how == 0:#Sharpness
            rinX=1
            rinY=1
        elif how == 1 and beforesize<=aftersize:#Brightness
            rinX=4
            rinY=4
        elif how == 1 and beforesize>aftersize:
            rinX=1.5*beforesize/aftersize
            rinY=1.5*beforesize/aftersize
        return rinX,rinY
    outX=inimg.shape[0]*aftersize//beforesize
    outY=inimg.shape[1]*aftersize//beforesize
    inrangeX,inrangeY=resize(beforesize,aftersize,how)
    if mode==0:
        outimg=np.zeros((outX,outY,inimg.shape[2]))
        for i in range(outX):
            for j in range(outY):
                inX = (i+0.5)*beforesize/aftersize
                inY = (j+0.5)*beforesize/aftersize
                outimg[i,j]=merge(inimg,inX,inY,inrangeX,inrangeY)
    elif mode==2:
        outimg=np.zeros((outX,outY,inimg.shape[2]))
        for i in range(outX):
            for j in range(outY):
                inX = (i+0.5)*beforesize/aftersize
                inY = (j+0.5)*beforesize/aftersize
                outimg[i,j]=merge_mode2(inimg,inX,inY,inrangeX,inrangeY)
    elif mode==1:
        outimg=np.zeros((outX,outY))
        for i in range(outX):
            for j in range(outY):
                inX = (i+0.5)*beforesize/aftersize
                inY = (j+0.5)*beforesize/aftersize
                outimg[i,j]=merge_mode1(inimg,inX,inY,inrangeX,inrangeY)        
    outimg=outimg.astype(np.uint8)
    print(outimg)
    print(outimg.shape)
    return outimg




def make_window():
    def ask_files():
        path=filedialog.askopenfilenames(filetypes=[("PNG Image Files","*.png")],defaultextension=".png")
        print(path)
        path_str=",".join(path)
        file_path.set(path_str)
    def how():
        howhow=how_comb.get()
        if howhow=="くっきり":
            return 0
        elif howhow=="ぼんやり":
            return 1

    def app():
        beforesize=(input_pak_box.get())
        aftersize=(output_pak_box.get())
        hows=how()
        input_files_str = file_path.get()
        input_files=input_files_str.split(",")
        print(input_files)
        print_txt=""
        for i in range(len(input_files)):
            input_file=str(input_files[i])
            output_file = str(input_files[i]).strip(".png")+"_"+str(beforesize)+"_"+str(aftersize)+".png"
            print(output_file)
            if not input_file or not output_file or not beforesize or not aftersize:
                return
            afterfile = resize_for_simutrans(input_file,output_file,beforesize,aftersize,hows)
            if afterfile.flag() !=1:
                print_txt+=output_file+","
        if len(print_txt)==0:
            messagebox.showinfo("完了","完了しました。")
        else:
            messagebox.showinfo("エラー","次のファイルでエラーがあります:"+print_txt)
    main_win = tk.Tk()
    main_win.title("resize_for_simutrans")
    main_win.geometry("500x200")
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)
    file_path=tk.StringVar()
    folder_label = ttk.Label(main_frm, text="ファイルを選択")
    folder_box = ttk.Entry(main_frm,textvariable=file_path)
    folder_btn = ttk.Button(main_frm, text="選択",command=ask_files)
    input_pak_label = ttk.Label(main_frm, text="元画像のpakサイズ")
    input_pak_box = ttk.Entry(main_frm)
    output_pak_label = ttk.Label(main_frm, text="生成するpakサイズ")
    output_pak_box = ttk.Entry(main_frm)
    how_label=ttk.Label(main_frm, text="変換処理方法")
    how_comb = ttk.Combobox(main_frm, values=["くっきり","ぼんやり"], width=15)
    how_comb.current(0)
    app_btn=ttk.Button(main_frm, text="変換を実行",command=app)
    folder_label.grid(column=0,row=0,pady=10)
    folder_box.grid(column=1,row=0,sticky=tk.EW, padx=5)
    folder_btn.grid(column=2,row=0)
    input_pak_box.grid(column=1,row=1,sticky=tk.EW, padx=5)
    input_pak_label.grid(column=0,row=1)
    output_pak_box.grid(column=1,row=2,sticky=tk.EW, padx=5)
    output_pak_label.grid(column=0,row=2)
    how_label.grid(column=0,row=3)
    how_comb.grid(column=1,row=3,sticky=tk.W,padx=5)
    app_btn.grid(column=1,row=4)
    #main_win.columnconfigure(0, wieght=1)
    #main_win.rowconfigure(0, wieght=1)
    #main_frm.columnconfigure(1, wieght=1)
    main_win.mainloop()
    



make_window()