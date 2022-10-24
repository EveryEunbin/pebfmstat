from flask import Flask, render_template, send_file
from deta import Deta 
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db = deta.Base("count-eunbin")

drive = deta.Drive("images")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

th_data = {
    "zone": ["A1","A2","B1","B2","C1","C2","D1","D2"],
    "total": [406,406,240,240,240,240,180,180]
}
ph_data = {
    "zone": ["PL","PC","PR","GL","GC","GR","SL","SC","SR","BL","BC","BR"],
    "total": [216,388,216,217,330,217,70,75,69,166,195,166]
}

sg_data = {
    "zone": ["VIP", "CAT A", "CAT B"],
    "total": [466, 384, 65]
}

# def customSort(k):
#     return k['date']

app = Flask(__name__)

CORS(app)

@app.route('/', methods=["GET"])
def index():
    th = db.fetch({"country": "th"})
    th = sorted(th.items, key=lambda item: item.get("date"))
    th_date_last = th[-1]['date']
    th_last = zip(th_data['zone'],th[-1]['reserved'],th[-1]['available'],th_data['total'])
    th_last = list(th_last)

    ph = db.fetch({"country": "ph"})
    ph = sorted(ph.items, key=lambda item: item.get("date"))
    ph_date_last = ph[-1]['date']
    ph_last = zip(ph_data['zone'],ph[-1]['reserved'],ph[-1]['available'],ph_data['total'])
    ph_last = list(ph_last)

    sg = db.fetch({"country": "sg"})
    sg = sorted(sg.items, key=lambda item: item.get("date"))
    sg_date_last = sg[-1]['date']
    sg_last = zip(sg_data['zone'],sg[-1]['reserved'],sg[-1]['available'],sg_data['total'])
    sg_last = list(sg_last)

    return render_template('index.html', th=th, th_data=th_data,th_last=th_last, th_date_last=th_date_last, ph=ph, ph_data=ph_data,ph_last=ph_last, ph_date_last=ph_date_last, sg=sg, sg_data=sg_data,sg_last=sg_last, sg_date_last=sg_date_last)

@app.route('/file/<id>', methods=['GET'])
def getFile(id):
    res = drive.get(id)
    return send_file(res, download_name=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)