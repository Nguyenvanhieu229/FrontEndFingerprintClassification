from flask import Flask, request, jsonify, render_template, session
from flask_caching import Cache
import os
import json
import requests
import copy

from Manager import Manager
from Model import Model
from FingerprintImage import FingerprintImage
from EmployeeLabel import EmployeeLabel
from ModelStatistics import ModelStatistics
from TrainingStatusStatistics import TrainingStatusStatistics

session = {}


class ClientController:
     def __init__(self):
         self.app = Flask(__name__)
         self.app.secret_key = 'HieuNV'
         self.app.add_url_rule('/start', 'StartPage', self.start, methods=['GET'])
         self.app.add_url_rule('/login', 'managerLogin', self.login, methods = ['POST'])
         self.app.add_url_rule('/home-model', 'viewHomeModelManager', self.homeModel, methods=['GET'])
         self.app.add_url_rule('/choose-image', 'Choose image to train', self.chooseImage, methods = ['GET'])
         self.app.add_url_rule('/train-new-model', 'view', self.trainNewModel, methods = ['POST'])
         self.app.add_url_rule('/model-statistics', 'view Model Statistics', self.modelStatistics, methods = ['GET'])
         self.app.add_url_rule('/training-statistics', 'view training statistics', self.trainingStatistics, methods = ['GET'])
         self.app.add_url_rule('/delete', 'delete model', self.deleteModel, methods = ['GET'])
         self.app.add_url_rule('/active', 'active model', self.active, methods = ['GET'])
         self.app.add_url_rule('/inactive', 'inactive model', self.inactive, methods=['GET'])
         self.app.add_url_rule('/view-details', 'view details model', self.viewDetails, methods = ['GET'])

     def run(self):
         port = int(os.environ.get('PORT', 2002))
         self.app.run(host='0.0.0.0', debug=True, port=port)

     def start(self):
        return render_template('login.html')

     def login(self):
         try:
             username = request.form['username']
             password = request.form['password']
             manager = Manager(id = None, username = username, password = password)

             server_url = 'http://localhost:2209/login'
             response = requests.post(server_url, json=manager.__dict__)

             if response.status_code == 200:
                 data = response.json()
                 manager = Manager(**data)
                 return render_template('home.html', manager = manager) if manager.id != None else render_template('login.html', message = "Login failed!")

             else:
                 return jsonify("An error has occured!")
         except Exception as e:
             print(e)



     def homeModel(self):
         try:
             server_url = 'http://localhost:2209/get-all-model'
             responce = requests.get(server_url)

             if responce.status_code == 200:
                 datas = responce.json()
                 models = []
                 for data in datas:
                     model = Model(**data)
                     model.creationManager = Manager(**model.creationManager)
                     models.append(model)

                 session['models'] = models
                 print(models)
                 return render_template('homeModel.html', models = models)
         except Exception as e:
             print(e)
             return jsonify("An error has occured!")


     def chooseImage(self):
         server_url = 'http://localhost:2209/get-all-fingerprint-image'

         if session.get('dataset') != None:
             return render_template('chooseImage.html', images = session['dataset'])
         respone = requests.get(server_url)

         if respone.status_code == 200:
             datas = respone.json()
             images = [FingerprintImage(**data) for data in datas]
             for image in images:
                 image.employeeLabel = EmployeeLabel(**image.employeeLabel)

             session['dataset'] = images[:]
             return render_template('chooseImage.html', images = images)
         else:
             return jsonify("An error has occured!")



     def trainNewModel(self):
         try:
             image_ids = [int(i) for i in request.form.getlist('image_ids')]
             tmp_data = copy.deepcopy(session['dataset'])
             data_to_send = []
             for x in tmp_data:
                 if x.id in image_ids:
                     data_to_send.append(x)

             for data in data_to_send:
                 data.employeeLabel = data.employeeLabel.__dict__
             data_to_send = [x.__dict__ for x in data_to_send]
             server_url = "http://localhost:2209/train-new-model"

             responce = requests.post(server_url, json = data_to_send)
             if responce.status_code == 200:
                 data = responce.json()
                 print(data)
                 model = Model(**data)
                 model.creationManager = Manager(**model.creationManager)
                 session['models'].append(model)
                 return render_template('model_info.html', model = model)
             else:
                 return jsonify("An error has occured")
         except Exception as e:
             print(e)
             return jsonify("An error has occured")

     def modelStatistics(self):
         serverurl = "http://localhost:2209/model-statistics"

         responce = requests.get(serverurl)

         if responce.status_code == 200:
             data = responce.json()
             print(data)
             modelStatistics = ModelStatistics(**data)
             return render_template('model_statistics.html', statistics = modelStatistics)
         else:
             return jsonify("An error has occured!")

     def trainingStatistics(self):

         serverurl = "http://localhost:2209/training-status"
         responce = requests.get(serverurl)

         if responce.status_code == 200:
             data = responce.json()
             modelStatistics = []
             for row in data:
                 model = Model(**row[0])
                 statistics = TrainingStatusStatistics(**row[1])
                 modelStatistics.append([model, statistics])
             print(modelStatistics)
             return render_template('training_status_statistics.html',modelStatistics=modelStatistics)
         else:
             return jsonify("An error has occured!")

     def deleteModel(self):
         id = int(request.args.get('id'))
         server_url = 'http://localhost:2209/delete?id=' + str(id)

         responce = requests.post(server_url)

         if responce.status_code == 200:
             data = responce.json()
             if data == True:
                 session['models'] = [model for model in session['models'] if model.id != id]
                 return render_template('homeModel.html', models = session['models'])
             else:
                 return render_template('homeModel.html', models = session['models'])

     def viewDetails(self):
         try:
             id = int(request.args.get('id'))
             model = None
             print(session['models'])
             for i in session['models']:
                 if i.id == id:
                     model = copy.copy(i)
             return render_template('model_info.html', model = model)
         except Exception as e:
             print(e)
             return jsonify("An error has occured!")

     def active(self):
         id = int(request.args.get('id'))
         model = None
         for i in session['models']:
             if i.id == id:
                 model = copy.copy(i)

         model.creationManager = model.creationManager.__dict__

         server_url = "http://localhost:2209/active"

         responce = requests.post(server_url, json = model.__dict__)

         if responce.status_code == 200:
             model_data = responce.json()
             model = Model(**model_data)
             model.creationManager = Manager(**model.creationManager)

             for i in session['models']:
                 if i.id == id:
                     i = model
             return render_template('model_info.html', model = model)
         else:
             return jsonify("An error has occured!")

     def inactive(self):
         id = int(request.args.get('id'))
         model = None
         for i in session['models']:
             if i.id == id:
                 model = copy.copy(i)

         model.creationManager = model.creationManager.__dict__

         server_url = "http://localhost:2209/inactive"

         responce = requests.post(server_url, json = model.__dict__)

         if responce.status_code == 200:
             model_data = responce.json()
             model = Model(**model_data)
             model.creationManager = Manager(**model.creationManager)

             for i in session['models']:
                 if i.id == id:
                     i = model
             return render_template('model_info.html', model = model)
         else:
             return jsonify("An error has occured!")




app = ClientController()
app.run()
