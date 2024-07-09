import requests
from flask import Flask,render_template,url_for
from flask import request as req
from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("API_TOKEN")


app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Output",methods=["GET","POST"])
def Output():
    if req.method== "POST": 
        result1=Summarize()
        result2=Grammer()
        if req.form['submit'] == 'summarize':    
            return render_template("index.html",result=result1)
        elif req.form['submit'] == 'grammer':
            return render_template("index.html",result=result2)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")
    



def Summarize():
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {SECRET_KEY}"}

    data=req.form["data"]

    maxL=int(req.form["maxL"])
    minL=maxL//4
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    outputs = query({
        "inputs":data,
        "parameters":{"min_length":minL,"max_length":maxL},
    })[0]

    return outputs
    #return outputs['summary_text']
 

    
def Grammer():
    API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"
    headers = {"Authorization": f"Bearer {SECRET_KEY}"}

    data=req.form["data"]

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs":data,
    })

    return output
    #return output['summary_text']




if __name__ == "__main__":
    app.run(debug=True)
