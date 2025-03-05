from flask import Flask,render_template,request,url_for
import joblib
import mysql.connector as con 

app=Flask(__name__)

model=joblib.load("Credit-Limit-Prediction-Model.lb")

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/user_data",methods=["GET","POST"])
def user_data():
    if request.method=="POST":
        g=request.form["g"]
        i=request.form["i"]
        r=request.form["r"]
        c=request.form["c"]
        b=request.form["b"]
        
    data=[[int(g),int(i),int(r),int(c),int(b)]]
    
    #prediction work 
    pred=model.predict(data)
    pred=pred.ravel()
    pred=str(int(pred[0]))
    msg="your Predicted Credit Limit is "+ pred
    
    
    main_data=[int(g),int(i),int(r),int(c),int(b),int(pred)]
    
    #database work
    #mysql connection work 
    conn=con.connect(
        host="localhost",
        user="root",
        password="",
        database="credit"
    )
    #create the cursor object 
    cursor = conn.cursor()
    
    Qurey="insert into prediction(g,i,r,c,b,p) values(%s,%s,%s,%s,%s,%s)"
    cursor.execute(Qurey,main_data)
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return pred
    
if(__name__=="__main__"):
    app.run(debug=True)