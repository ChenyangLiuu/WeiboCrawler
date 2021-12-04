from tkinter import *
from Crawler import get_page
from Crawler import parse_page
from Crawler import params
from mongo import save_to_mongo
from mongo import connect_to_mongo


max_page= params().max_page
base_url= params().base_url
headers=params().headers
collection=connect_to_mongo()

#ui
window = Tk()
window.title("Hello World")
window.geometry('350x200')
lbl = Label(window, text="Hello! My name is ")
lbl.grid(column=0, row=0)
txt = Entry(window, width=10)
txt.grid(column=1, row=0)


def clicked1():
    global keyword
    keyword = txt.get()
    window.destroy()


btn1 = Button(window, text="submit", command=clicked1)
btn1.grid(column=2, row=0)
window.mainloop()


if __name__ == '__main__':
    for page in range(1, max_page + 1):
        json = get_page(page,base_url,headers)
        results = parse_page(keyword, *json)
        for result in results:
            print(result)
            save_to_mongo(collection,result)


