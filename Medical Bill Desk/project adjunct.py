def project():
        import mysql.connector as ms
        import csv
        

        mydb=ms.connect(host='localhost',user='root',passwd='1734')

        c=mydb.cursor()

        c.execute('CREATE DATABASE if not exists project')
        c.execute('USE project')
        c.execute('''CREATE TABLE if not exists medicines
                  (Tagno int PRIMARY KEY NOT NULL, Medicinename varchar(300) NOT NULL , Quantity int NOT NULL , Rate decimal NOT NULL)''')
        c.execute('''CREATE TABLE if not exists customers
                  (Cno int PRIMARY KEY NOT NULL, Name varchar(300) NOT NULL
                  , Phone int NOT NULL , Age int NOT NULL , MailID varchar(500) NOT NULL , Totalrate decimal NOT NULL , Refno int NOT NULL)''')


        f=open('Medicines.csv','r',newline='')
        a=csv.reader(f)
        c.execute('DELETE FROM medicines')
        for i in a:
                c.execute('INSERT INTO medicines VALUES({0},"{1}",{2},{3})'.format(i[0],i[1],i[2],i[3]))
        mydb.commit()
    

project()

