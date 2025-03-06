import api
if __name__ == "__main__":
    app = api.app 
    app.run(host='0.0.0.0', port=8000, debug=True)
