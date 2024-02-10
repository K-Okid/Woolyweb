import pymysql
from flask import Flask,render_template,url_for,request,redirect,session
import json
from shared import *
from en_de import*
@app.route('/farmer_personal_login',methods=["POST","GET"])
def ren_farmer():
    return render_template("farmers_personal.html")
x_farmers=["name","age","aadhaar","address","city","state","phone","processing","sheep_type","inventory","No. of sheep","gender","password"]
@app.route("/submit_farmer",methods=["POST","GET"])
def submit_farmer():
    if(request.method=="POST"):
        dic={}
        if(request.method=="POST"):
            for i in x_farmers:
                dic[i]=request.form[i]
            return redirect(url_for("complete_farmer",a=encrypt(json.dumps(dic))),code=307)
    elif(request.method=="GET"):
        return redirect('/farmer_personal_login')
#global var
r_farmer=[]
@app.route("/complete_farmer/<a>",methods=["POST","GET"])
def complete_farmer(a):
    if(request.method=="POST"):
        r_farmer.clear()
        obj3=pymysql.connect(host="localhost",user="root",password="abcd",database="woolyweb")
        cur3=obj3.cursor()
        cur4=obj3.cursor()
        obj4=pymysql.connect(host="localhost",user="root",password="abcd",database="aadhar")
        cur5=obj4.cursor()
        cur=obj3.cursor()
        cur4.execute("select * from farmers;")
        cur5.execute("select aadhar_numbers from verified_aadhar")
        a=decrypt(a)
        a=json.loads(a)
        if(str(a['aadhaar']) in [z[0] for z in cur5.fetchall()]):
            cur.execute("Select aadhar_number from farmers;")
            for i in x_farmers:
                r_farmer.append(a[i])
            r_farmer[-2]=r_farmer[-2][0]
            r_farmer[7]=r_farmer[7][0]
            if(not r_farmer[-3].isdigit()):
                return "<h1>SUBMISSION UNSUCCESSFUL..!!<br>ENTER A VALID NO OF SHEEPS</h1>"
            if(r_farmer[7].lower()!="y" and r_farmer[7].lower()!="n"):
                return "<h1>SUBMISSION UNSUCCESSFUL..!!<br>ENTER A VALID PROCESSING REQUIREMENT</h1>"
            r_farmer[9]=r_farmer[9][0]
            if(r_farmer[9].lower()!="y" and r_farmer[9].lower()!="n"):
                return "<h1>SUBMISSION UNSUCCESSFUL..!!<br>ENTER A VALID INVENTORY REQUIREMENT</h1>"
            temp=cur.fetchall()
            print(temp)
            if(r_farmer[2] in [x[0] for x in temp]):
                return "<h1>SUBMISSION UNSUCCESSFUL..!!<br>THIS AADHAR NUMBER IS ALREADY REGISTERED</h1>"
            if(len(r_farmer[6])!=10):
                return "<h1>SUBMISSION UNSUCCESSFUL..!!<br>PLEASE ENTER A VALID PHONE NUMBER</h1>"
            if(cur4.fetchone()==None):
                r_farmer.append(1)        
            else:
                cur4.execute("select * from farmers;")
                r_farmer.append(int(cur4.fetchall()[-1][0])+1)
            cur3.execute("Insert into farmers(fname,age,aadhar_number,address,city,state,phone_number,processing_access,type_of_sheep,inventory_access,no_of_sheeps,gender,password,fid) values"+str(tuple(r_farmer))+";")
            obj3.commit()
            return render_template("bank details.html")
        else:
            return "<h1>YOUR SUBMISSION IS UNSUCCESSFUL<br>PLEASE ENTER A VALID AADHAR</h1>"
    elif(request.method=="GET"):
        return redirect('/farmer_personal_login')

'''if __name__=="__main__":
    app.run(debug=True)'''

