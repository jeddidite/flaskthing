from website import create_app

app = create_app() #Pulls /website/__init__.py

if __name__ == '__main__': #Runs the app from /website/__init__.py
    app.run(debug=True)


