from flask import request

from App import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False,host='192.168.70.12')
