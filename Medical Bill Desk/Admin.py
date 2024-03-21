from tabulate import tabulate  
import mysql.connector as ms
import csv
from project_adjunct import project

mydb=ms.connect(host='localhost',user='root',passwd='1734',database='project')

c=mydb.cursor()

def admin():
 ps=int(input('Enter Password :'))
 if ps == 1734:
  row=[]
  def add():
   co=int(input('PRESS 1 TO SHOW SUGGESTED MEDICINES\nPRESS 2 TO CONTINUE\n: '))
   if co == 1:
    with open('suggestions.txt','r') as f:
     print([f.readlines()])
   
   med= input('Enter Medicine Name : ')
   pow1=int(input('Enter Power in mg : '))
   rate=int(input('Enter Rate : '))
   
   c.execute('SELECT Tagno FROM medicines ORDER BY Tagno DESC')

   row = [int(c.fetchone()[0])+1,med,pow1,rate]
   with open('Medicines.csv','a',newline='') as f:
       w=csv.writer(f)
       w.writerow(row)
   
   print(row)
   project()
   
  while True:
   print(tabulate([['PRESS 1 TO ADD MEDICINES'],
   ['PRESS 2 TO SHOW CUSTOMER DETAILS'],
   ['PRESS 3 TO EXIT']],tablefmt="fancy_grid"))

   ch=int(input('Enter your Choice : '))
   if ch == 1:
    add()
   elif ch == 2:
    print('sc')
   elif ch == 3:
    print('Thank You !!')
    break
   else:
    print('Wrong Choice !!')


admin()
