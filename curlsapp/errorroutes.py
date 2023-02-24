from flask import Flask,render_template,abort
from curlsapp import app

#Error Pages
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('errors/error404.html',error=error),404

@app.errorhandler(500)
def internalserver(error):
    return render_template('errors/error500.html',error=error),500