#!/usr/bin/env python3

import json
import requests
import collections
import matplotlib.pyplot as plt
from tkinter import *
from time import sleep

class Position:
    def __init__(self, ticker, shares):
        self.ticker = ticker
        self.shares = shares
        self.init_price = 1

class Profile:
    def __init__(self, name):
        self.name = name
        self.positions = []
    def add(self, ticker, shares):
        self.positions.append(Position(ticker, shares))
    def rem(self, ticker, shares):
        for pos in self.positions:
            if (pos.shares == shares and pos.ticker == ticker):
                self.positions.remove(pos)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.list_prices = []
        self.pf_var = StringVar()
        self.ps_var = StringVar()
        self.ch_choice = "se"
        self.profiles = []
        self.cur_profile = Profile("--unset")
        self.initialize()
        self.list_profiles()
        self.list_pos()
        self.create_widgets()

    def initialize(self):
        pro_file = open("profile_file", "r")
        for line in pro_file:
            if (line[-1] == '\n'):
                line = line[:-1]
            if (line[:3] == "pro"):
                self.profiles.append(Profile(line[3:]))
            elif (line[:3] == "pos"):
                self.profiles[len(self.profiles)-1].add(line[3:11],(int)(line[11:]))
                tmp = self.profiles[len(self.profiles)-1].positions[len(self.profiles[len(self.profiles)-1].positions)-1].ticker
                self.profiles[len(self.profiles)-1].positions[len(self.profiles[len(self.profiles)-1].positions)-1].ticker = tmp[:tmp.find('-')]
        pro_file.close()

    def my_chart(self, time_per):
        if (time_per == "day"):
            self.list_prices = [0.0] * 28
            for pos in self.cur_profile.positions:
                self.add_day_prices(pos.ticker, pos.shares)
            x = range(28)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "week"):
            self.list_prices = [0.0] * 35
            for pos in self.cur_profile.positions:
                self.add_week_prices(pos.ticker, pos.shares)
            x = range(35)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "month"):
            self.list_prices = [0.0] * 30
            for pos in self.cur_profile.positions:
                self.add_month_prices(pos.ticker, pos.shares)
            x = range(30)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "year"):
            self.list_prices = [0.0] * 52
            for pos in self.cur_profile.positions:
                self.add_year_prices(pos.ticker, pos.shares)
            x = range(52)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "5year"):
            self.list_prices = [0.0] * 60
            for pos in self.cur_profile.positions:
                self.add_5year_prices(pos.ticker, pos.shares)
            x = range(60)
            plt.plot(x, self.list_prices)
            plt.show()
        else:
            print("Invalid time period. (day, week, month, year, 5year)")

    def chart(self, ticker, time_per):
        if (time_per == "day"):
            self.list_prices = [0.0] * 28
            self.add_day_prices(ticker, 1)
            x = range(28)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "week"):
            self.list_prices = [0.0] * 35
            self.add_week_prices(ticker, 1)
            x = range(35)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "month"):
            self.list_prices = [0.0] * 30
            self.add_month_prices(ticker, 1)
            x = range(30)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "year"):
            self.list_prices = [0.0] * 52
            self.add_year_prices(ticker, 1)
            x = range(52)
            plt.plot(x, self.list_prices)
            plt.show()
        elif (time_per == "5year"):
            self.list_prices = [0.0] * 60
            self.add_5year_prices(ticker, 1)
            x = range(60)
            plt.plot(x, self.list_prices)
            plt.show()
        else:
            print("Invalid time period. (day, week, month, year, 5year)")

    def add_day_prices(self, ticker, shares):
        rep = 28
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
        +"&interval=15min&apikey=6CITKGABXG4P8ZUH&outputsize=compact&symbol=" + ticker)
        j = 0
        prices = []
        a = r.text
        for i in range(len(a)):
            if (a[i] != 'c'):
                continue
            if (a[i:i+5] == "close"):
                if (a[i+5] == ')'):
                    continue
                deci = a[i+9:i+15].find('.')
                prices.append((float)(a[i+9:i+deci+13]))
                j += 1
                if (j == rep):
                    break
        prices.reverse()
        for i in range(rep):
            self.list_prices[i] += (prices[i] * shares)

    def add_week_prices(self, ticker, shares):
        rep = 35
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
        +"&interval=60min&apikey=6CITKGABXG4P8ZUH&outputsize=compact&symbol=" + ticker)
        j = 0
        prices = []
        a = r.text
        for i in range(len(a)):
            if (a[i] != 'c'):
                continue
            if (a[i:i+5] == "close"):
                if (a[i+5] == ')'):
                    continue
                deci = a[i+9:i+15].find('.')
                prices.append((float)(a[i+9:i+deci+13]))
                j += 1
                if (j == rep):
                    break
        prices.reverse()
        for i in range(rep):
            self.list_prices[i] += (prices[i] * shares)

    def add_month_prices(self, ticker, shares):
        rep = 30
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY"
        +"&apikey=6CITKGABXG4P8ZUH&outputsize=compact&symbol=" + ticker)
        j = 0
        prices = []
        a = r.text
        for i in range(len(a)):
            if (a[i] != 'c'):
                continue
            if (a[i:i+5] == "close"):
                if (a[i+5] == ')'):
                    continue
                deci = a[i+9:i+15].find('.')
                prices.append((float)(a[i+9:i+deci+13]))
                j += 1
                if (j == rep):
                    break
        prices.reverse()
        for i in range(rep):
            self.list_prices[i] += (prices[i] * shares)

    def add_year_prices(self, ticker, shares):
        rep = 52
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY"
        +"&apikey=6CITKGABXG4P8ZUH&outputsize=compact&symbol=" + ticker)
        j = 0
        prices = []
        a = r.text
        for i in range(len(a)):
            if (a[i] != 'c'):
                continue
            if (a[i:i+5] == "close"):
                if (a[i+5] == ')'):
                    continue
                deci = a[i+9:i+15].find('.')
                prices.append((float)(a[i+9:i+deci+13]))
                j += 1
                if (j == rep):
                    break
        prices.reverse()
        for i in range(rep):
            self.list_prices[i] += (prices[i] * shares)

    def add_5year_prices(self, ticker, shares):
        rep = 60
        r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY"
        +"&apikey=6CITKGABXG4P8ZUH&outputsize=compact&symbol=" + ticker)
        j = 0
        prices = []
        a = r.text
        for i in range(len(a)):
            if (a[i] != 'c'):
                continue
            if (a[i:i+5] == "close"):
                if (a[i+5] == ')'):
                    continue
                deci = a[i+9:i+15].find('.')
                prices.append((float)(a[i+9:i+deci+13]))
                j += 1
                if (j == rep):
                    break
        prices.reverse()
        for i in range(rep):
            self.list_prices[i] += (prices[i] * shares)

    def button_exit(self):
        pro_file = open("profile_file", "w")
        for pf in self.profiles:
            pro_file.write("pro"+pf.name+'\n')
            for pos in pf.positions:
                pro_file.write("pos"+pos.ticker)
                for i in range(8-len(pos.ticker)):
                    pro_file.write('-')
                pro_file.write(str(pos.shares)+'\n')
        exit()

    def list_pos(self):
        a = ""
        if (self.cur_profile.name == "--unset"):
            a = "No profile selected"
        else:
            for pos in self.cur_profile.positions:
                a += (pos.ticker + " " + str(pos.shares) + " shares\n\n")
        self.ps_var.set(a)

    def retrieve_input_ad(self):
        input = self.pf_text.get("1.0",END)
        found = False
        if (input[-1] == '\n'):
            input = input[:-1]
        for pf in self.profiles:
            if (pf.name == input):
                self.cur_profile = pf
                found = True
                break
        if (not found):
            self.profiles.append(Profile(input))
            self.cur_profile = self.profiles[len(self.profiles)-1]
        self.list_profiles()
        self.list_pos()

    def retrieve_input_rm(self):
        input = self.pf_text.get("1.0",END)
        if (input[-1] == '\n'):
            input = input[:-1]
        for pf in self.profiles:
            if (pf.name == input):
                self.profiles.remove(pf)
                break
        self.cur_profile = Profile("--unset")
        self.list_profiles()
        self.list_pos()
    
    def retrieve_input_adb(self):
        input = self.ps_text.get("1.0",END)
        first_space = input.find(' ')
        second_space = input[first_space+1:].find(' ')+first_space+1
        self.cur_profile.add(input[:first_space], (int)(input[first_space+1:second_space]))
        self.list_pos()

    def retrieve_input_rmb(self):
        input = self.ps_text.get("1.0",END)
        if (input[-1] == '\n'):
            input = input[:-1]
        for pos in self.cur_profile.positions:
            if (pos.ticker+" "+str(pos.shares)+" shares" == input):
                self.cur_profile.positions.remove(pos)
                break
        self.list_pos()

    def retrieve_input_ch(self):
        input = self.ch_text.get("1.0",END)
        if (input[-1] == '\n'):
            input = input[:-1]
        self.chart(input, "day")
        self.ch_choice = "se"
        
    def retrieve_input_mc(self):
        self.my_chart("day")
        self.ch_choice = "mc"

    def retrieve_input_pt_day(self):
        if (self.ch_choice == "mc"):
            if (self.cur_profile.name == "--unset"):
                pass
            else:
                self.my_chart("day")
        else:
            input = self.ch_text.get("1.0",END)
            if (input[-1] == '\n'):
                input = input[:-1]
            self.chart(input, "day")

    def retrieve_input_pt_week(self):
        if (self.ch_choice == "mc"):
            if (self.cur_profile.name == "--unset"):
                pass
            else:
                self.my_chart("week")
        else:
            input = self.ch_text.get("1.0",END)
            if (input[-1] == '\n'):
                input = input[:-1]
            self.chart(input, "week")

    def retrieve_input_pt_month(self):
        if (self.ch_choice == "mc"):
            if (self.cur_profile.name == "--unset"):
                pass
            else:
                self.my_chart("month")
        else:
            input = self.ch_text.get("1.0",END)
            if (input[-1] == '\n'):
                input = input[:-1]
            self.chart(input, "month")

    def retrieve_input_pt_year(self):
        if (self.ch_choice == "mc"):
            if (self.cur_profile.name == "--unset"):
                pass
            else:
                self.my_chart("year")
        else:
            input = self.ch_text.get("1.0",END)
            if (input[-1] == '\n'):
                input = input[:-1]
            self.chart(input, "year")

    def retrieve_input_pt_5year(self):
        if (self.ch_choice == "mc"):
            if (self.cur_profile.name == "--unset"):
                pass
            else:
                self.my_chart("5year")
        else:
            input = self.ch_text.get("1.0",END)
            if (input[-1] == '\n'):
                input = input[:-1]
            self.chart(input, "5year")

    def list_profiles(self):
        a = ""
        if (len(self.profiles) == 0):
            a = "There are no profiles (make a new one using a custom name)"
        else:
            if (self.cur_profile.name == "--unset"):
                a = "No profile selected\n\n\n"
            else: 
                a = "Selected: " + self.cur_profile.name + "\n\n\n"
            for pf in self.profiles:
                a += pf.name + "\n\n"
        self.pf_var.set(a)

    def create_widgets(self):
        self.lframe0 = Frame(self)
        self.lframe0.pack(side="left")
        self.llabel0 = Label(self.lframe0, width=5)
        self.llabel0.pack()

        self.pf_frame = Frame(self)
        self.pf_frame.pack(side="left")

        self.lframe1 = Frame(self)
        self.lframe1.pack(side="left")
        self.llabel1 = Label(self.lframe1, width=5)
        self.llabel1.pack()

        self.ps_frame = Frame(self)
        self.ps_frame.pack(side="left")

        self.lframe2 = Frame(self)
        self.lframe2.pack(side="left")
        self.llabel2 = Label(self.lframe2, width=5)
        self.llabel2.pack()

        self.ch_frame = Frame(self)
        self.ch_frame.pack(side="left")

        self.lframe3 = Frame(self)
        self.lframe3.pack(side="left")
        self.llabel3 = Label(self.lframe3, width=5)
        self.llabel3.pack()

        self.tp_frame = Frame(self)
        self.tp_frame.pack(side="left")

        self.lframe4 = Frame(self)
        self.lframe4.pack(side="left")
        self.llabel4 = Label(self.lframe4, width=5)
        self.llabel4.pack()

        self.pf_label = Label(self.pf_frame, text="Profiles", font=("Ariel", 18), padx=5, pady=5)
        self.pf_label.pack(side="top")
        self.pf_show = Label(self.pf_frame, bg="white", height=20, width=15, textvariable=self.pf_var, font=("Ariel", 14), borderwidth=2, relief="groove", padx=10, pady=5)
        self.pf_show.pack(side="top")
        self.llabel9 = Label(self.pf_frame, height=1)
        self.llabel9.pack(side="top")
        self.pf_text = Text(self.pf_frame, font=("Ariel", 14), height=1, width=14, padx=10, pady=5)
        self.pf_text.pack(side="top")
        self.llabel10 = Label(self.pf_frame, height=1)
        self.llabel10.pack(side="top")
        self.pf_button_add = Button(self.pf_frame, height=3, width=10, text="Add/Select", font=("Ariel", 14), command=self.retrieve_input_ad, padx=10, pady=5)
        self.pf_button_add.pack(side="top")
        self.llabel13 = Label(self.pf_frame, height=1)
        self.llabel13.pack(side="top")
        self.pf_button_rem = Button(self.pf_frame, height=3, width=10, text="Remove", font=("Ariel", 14), command=self.retrieve_input_rm, padx=10, pady=5)
        self.pf_button_rem.pack(side="top")
        self.llabel5 = Label(self.pf_frame, height=3)
        self.llabel5.pack(side="top")
        
        self.ps_label = Label(self.ps_frame, text="Positions", font=("Ariel", 18), padx=5, pady=5)
        self.ps_label.pack(side="top")
        self.ps_show = Label(self.ps_frame, bg="white", height=20, width=15, textvariable=self.ps_var, font=("Ariel", 14), borderwidth=2, relief="groove", padx=10, pady=3)
        self.ps_show.pack(side="top")
        self.llabel11 = Label(self.ps_frame, height=1)
        self.llabel11.pack(side="top")
        self.ps_text = Text(self.ps_frame, font=("Ariel", 14), height=1, width=14, padx=10, pady=5)
        self.ps_text.pack(side="top")
        self.llabel12 = Label(self.ps_frame, height=1)
        self.llabel12.pack(side="top")
        self.ps_button_add = Button(self.ps_frame, height=3, width=10, text="Add/Select", font=("Ariel", 14), command=self.retrieve_input_adb, padx=10, pady=5)
        self.ps_button_add.pack(side="top")
        self.llabel14 = Label(self.ps_frame, height=1)
        self.llabel14.pack(side="top")
        self.ps_button_rem = Button(self.ps_frame, height=3, width=10, text="Remove", font=("Ariel", 14), command=self.retrieve_input_rmb, padx=10, pady=5)
        self.ps_button_rem.pack(side="top")
        self.llabel6 = Label(self.ps_frame, height=3)
        self.llabel6.pack(side="top")

        self.ch_label = Label(self.ch_frame, text="Chart", font=("Ariel", 18), padx=5, pady=5)
        self.ch_label.pack(side="top")
        self.ch_show = Label(self.ch_frame, bg="white", height=20, width=50, font=("Ariel", 14), borderwidth=2, relief="groove", padx=10, pady=3)
        self.ch_show.pack(side="top")
        self.llabel12 = Label(self.ch_frame, height=1)
        self.llabel12.pack(side="top")
        self.ch_text = Text(self.ch_frame, font=("Ariel", 18), height=1, width=20, padx=10, pady=5)
        self.ch_text.pack(side="top")
        self.llabel12 = Label(self.ch_frame, height=1)
        self.llabel12.pack(side="top")
        self.ch_button_se = Button(self.ch_frame, height=3, width=10, text="Search", font=("Ariel", 14), command=self.retrieve_input_ch, padx=10, pady=5)
        self.ch_button_se.pack(side="top")
        self.llabel15 = Label(self.ch_frame, height=1)
        self.llabel15.pack(side="top")
        self.ch_button_mc = Button(self.ch_frame, height=3, width=10, text="My Chart", font=("Ariel", 14), command=self.retrieve_input_mc, padx=10, pady=5)
        self.ch_button_mc.pack(side="top")
        self.llabel7 = Label(self.ch_frame, height=3)
        self.llabel7.pack(side="top")

        self.tp_button_day = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Day", command=self.retrieve_input_pt_day)
        self.tp_button_day.pack(side="top")
        self.tp_button_week = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Week", command=self.retrieve_input_pt_week)
        self.tp_button_week.pack(side="top")
        self.tp_button_month = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Month", command=self.retrieve_input_pt_month)
        self.tp_button_month.pack(side="top")
        self.tp_button_year = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Year", command=self.retrieve_input_pt_year)
        self.tp_button_year.pack(side="top")
        self.tp_button_5year = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Five Year", command=self.retrieve_input_pt_5year)
        self.tp_button_5year.pack(side="top")
        self.llabel8 = Label(self.tp_frame, height=14)
        self.llabel8.pack(side="top")
        self.tp_button_exit = Button(self.tp_frame, height=3, width=10, font=("Ariel", 14), text="Save & Exit", command=self.button_exit)
        self.tp_button_exit.pack(side="top")

root = Tk()
app = Application(master=root)
app.mainloop()
