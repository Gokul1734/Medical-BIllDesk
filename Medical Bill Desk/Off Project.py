import mysql.connector as ms
import csv
import smtplib                                                #pip install smtplib
from email.message import EmailMessage      
from datetime import date                              #pip install datetime
from tabulate import tabulate                         #pip install tabulate
import random
import subprocess                                           #pip install subprocess
import os

mydb=ms.connect(host='localhost',user='root',passwd='1734',database='project')

c=mydb.cursor()

tot=0
total=0
k=0
l=[]
flag=False
ref=0
bill=[]
bl=[]
fl=0

def order():

 def Details():
  print("\n*****************************************CUSTOMER DETAILS********************************************\n")
  global l
  global k
  global flag
  a=input('Are you an existing Customer(y/n) : ')
  if a == 'y' or a == 'Y':
      u = int(input('Enter your ref no : '))
      c.execute('SELECT * FROM customers')
      for i in c.fetchall():
          if u == i[5] :
              k=float(i[4])*(10/100)
              l=[i[0],i[1],i[2],i[3],i[5]]
              global tot
              tot=i[4]
              flag = True
              break
      if flag == False:
          print('Sorry ref no not available !!\n\n')
          

  if l != []:
      print('\n Name : ' ,l[0] ,'\n','Phone number : ' ,l[1],'\n','Mail ID : ',l[3],'\n','Ref no : ',l[4],'\n\n')
  else:
      name=input('Enter Name : ')
      ph=int(input('Enter Phone no : '))
      age=int(input('Enter Age : '))
      mail=input('Enter Mail ID : ')
      while len(str(ph)) != 10:
          print('Phone Number not valid !!')
          ph=int(input('Enter Phone no : '))
          
          l=[name,ph,age,mail]
          
      l=[name,ph,age,mail]
  return l



 def reorder():
  global bill
  global bl
  global total
  try:
      with open(r'D:\Gokul\Studies\Subjects\Computer Science\Python Files\Project Final out\Bills\Bill - {0}.csv'.format(ref),'r') as f:
          r=csv.reader(f)
          for i in r:
              i[1] = int(i[1])
              bill = [i[0] , i[1]]
              total += int(i[1])
              bl.append(bill)
              
          print(tabulate(bl,headers=['Medicine','Rate'],tablefmt="fancy_grid"))
  except FileNotFoundError:
      print('We are not able to find your old cart !!')



 def medicines():
  global bl
  if flag == True:
      a=input('PRESS "Y" TO REORDER\nPRESS "X" TO PLACE NEW ORDER\n :  ')
      if a.upper() == 'Y':
          reorder()
          k=input('PRESS "Y" TO ORDER\nPRESS "X" TO EXIT\n :  ')
          if k.upper() == 'Y':
              return tabulate(bl,headers=['Medicine','Rate'],tablefmt="fancy_grid")
  global bill
  global total
  total = 0     
  l2=[]
  bl=[]
  c.execute('SELECT * FROM medicines;')
  for i in c.fetchall():
      l2.append(list(i))
  f=1
  print("*****************************************MEDICINES********************************************")
  ans=''
  
  while ans != '-':
      med=input('Enter medicine name or Tagno : ')
      q=int(input('Enter quantity : '))
      for k in l2:
          if med.lower() == k[1].lower() or med.lower() == str(k[0]):
            bill=[k[1],q*int(k[3])]                                     #[clein500,300]
            total += (bill[1])  
            f=0
      if f == 0:
         print(bill)
      else:
         print('Medicine not found !!')

      ans =input('------------------------------------------------------------')
      if f == 0:
       bl.append(bill)                                #[[celin500,300],[]]
          
  
  print(tabulate(bl,headers=['Medicine','Rate'],tablefmt="fancy_grid"))
  return tabulate(bl,headers=['Medicine','Rate'],tablefmt="fancy_grid") 


 def refgen():
  if flag == False:
      global ref
      lk=[]
      ref = 0
      c.execute('use project')
      c.execute('SELECT * FROM customers')
      for i in c:
          lk.append(i[5])
      while ref not in lk :
          ref = random.randint(100000 , 999999)
          break
      return ref
  else:
      ref = l[4]
      return ref


 def mse(m,ref):
  global y
  global bl
  global total
  y=0
  today = date.today()
  d1 = today.strftime("%d/%m/%Y")
  
  msg = EmailMessage()
  
  medic=medicines()
  
  if k >= total:
      y=50
  else:
      y=total-k
      
  msg.set_content('''\n Name : {0} \n Phone Number : {1} \n Ref No : {2} \n Date : {3} \n\n {4} \n Total : {5}/-
                                  \nThank you for shopping on E-Pharmacy !!\n\n'''.format(l[0],l[1],ref,d1,medic,y))

  if flag == True:
      print('\nYour Subtotal = ',total, '\nYour previous Order has been taken into consideration for a discount of 10%\nYour Total = ' ,y)
  else:
      print('Your Subtotal = ' , total)

  h=int(input('\nPRESS 1 TO CONFIRM CART\nPRESS 2 TO EXIT\n : '))

  if h == 1:
      msg['Subject'] = 'Hi {0} ,you have successfully booked the medicines in our store ,here is your bill receipt !!'.format(l[0])
      msg['From'] = "epharmacy6920@gmail.com"
      msg['To'] = m
          
      # Send the message via our own SMTP server.
      
      print('Processing your Order.........')

      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.login("epharmacy6920@gmail.com", "cscproject6920")
      server.send_message(msg)
      server.quit()

      print('Your Order has been placed Successfully !!')


      f=open(r'D:\Gokul\Studies\Subjects\Computer Science\Python Files\Project Final out\Bills\Bill - {0}.csv'.format(ref),'w',newline='')
      w=csv.writer(f)
      w.writerows(bl)
      f.flush()
      f.close()

      if flag == True:
          c.execute('DELETE FROM customers WHERE Refno = {0}'.format(ref))

      c.execute('INSERT INTO customers VALUES("{0}","{1}",{2},"{3}",{4},{5})'.format(l[0],l[1],l[2],l[3],float(tot)+float(y),ref))
      mydb.commit()
 
  bl = []
  total = 0
                     
 mse(Details()[3],refgen())




def check():
    c.execute('SELECT * FROM medicines;')
    for i in c.fetchall():
        print(i[0] , ' - ' , i[1])


def export():
 try:
   path=os.path.abspath(r'D:\Gokul\Studies\Subjects\Computer Science\Python Files\Project Final out\Bills\Bill - {0}.csv'.format(ref))
   subprocess.Popen('explorer %s' % path)
 except FileNotFoundError:
   print('Sorry file not found !!')
def suggest():
   ans = 0
   while ans != '-':
      medo=input('\nEnter medicine name : ')
      with open('suggestions.txt','a') as f1:
         f1.writelines([medo,'\n'])
      ans = input('---------------------------------------')

   return '\nThank you ! Your suggestion has been recorded'

        
def Menu():
    p=[]
    while True:
        p=[['PRESS 1 TO VIEW THE AVAILABLE MEDICINES'],
            ['PRESS 2 TO ORDER MEDICINES'],
               ['PRESS 3 TO GENRATE BILL'],
               ['\t\t  PRESS 4 TO SUGGEST MEDICINES TO BE ADDED'],
               ['\t\t  PRESS 5 TO EXIT']]

        print(tabulate(p,headers=['\t\t\tMENU'],tablefmt='fancy_grid'))
    
        ch=input('\nENTER YOUR CHOICE : ')
        if ch == '1':
            check()
        elif ch == '2':
            order()
            fl = 1
        elif ch == '3':
           if fl == 1:
              export()
              print('Opening Bill.....')
              break
           else:
              print('File not Found !!')
        elif ch == '4':
            print(suggest())
        elif ch == '5':
            print('THANK YOU !!')
            break  
        else:
            print('Wrong Choice !!')
             
    
    
Menu()












