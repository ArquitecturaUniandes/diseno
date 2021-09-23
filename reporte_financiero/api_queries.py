from flask import render_template
from joblib import load
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd 
import numpy as np 
import plotly.express as px 
import plotly.graph_objects as go
from plotly.offline import iplot
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from base import app, q



@app.route('/api-queries/reporte-financiero', methods=['GET'])
def hello_world():
    return render_template('output.html', href = '/static/default_output_image_results.svg')


def make_picture(*args):
    
    data = pd.read_csv("ABCdataset.csv")
    data = data.rename_axis("client").reset_index()
    data["client"] = data["client"] + 1
    data = data[["client", "balance", "purchases", "default"]]
    data = data[~data.isnull().any(axis=1)]
    data["default"] =  data["default"].astype("category")
    x_train = data[["balance","purchases"]]
    y_train = data[["default"]]
    
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(x_train, y_train)   
    
    fig = px.scatter(data, x = "balance", y="purchases",  title = "balance (in thousands COP) vs purchases (in thousands of COP) in clinica ABC",color ="default") 
    new_point = {'balance': [args[0]], 'purchases': [args[1]], 'default': [ knn.predict([[args[0],args[1]]])[0] ]}
    new_point = pd.DataFrame.from_dict(new_point)
    new_point["default"] =  new_point["default"].astype("category")
    name = 'default: {}'.format(new_point["default"][0])
    if new_point["default"][0] == 1:
        fig.add_scatter(x = [args[0]], y = [args[1]], name =name, marker = dict(size=[40], color='rgba(237, 84, 57, 1)'))  
    else: 
        fig.add_scatter(x = [args[0]], y = [args[1]], name =name, marker = dict(size=[40], color='rgba(72, 93, 217, 1)'))  
        
    fig.write_image('output_image_results.svg', width=1500)
    

    fig.show()


@app.route('/estado-de-salud', methods=['GET'])
def verificar_salud():
    return '{"estado": "ok"}', 200


# entrypoint
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
