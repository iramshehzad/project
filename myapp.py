from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def main():
    if request.method=="POST":
       return redirect(url_for("second", prompt=request.form["todo"]))
    else:
        return render_template("first-page.html")
    

@app.route("/<prompt>",methods=["POST","GET"])
def second(prompt):
        return render_template("second-page.html",content=prompt)
    

if __name__=="__main__":
  app.run()