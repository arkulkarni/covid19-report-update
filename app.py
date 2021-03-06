import json
import papermill as pm
import nbformat
import gc
from nbconvert import HTMLExporter
from nbconvert.writers import FilesWriter
import os
from flask import Flask
from google.cloud import storage


SCRATCH_DIR = '.'
BUCKET_NAME = 'covid19report'

def main_report_generation_function():
    print('START: downloading and executing notebook from github')
    pm.execute_notebook(
       'https://raw.githubusercontent.com/arkulkarni/COVID-19-Analysis/master/COVID-19-Analysis.ipynb',
       SCRATCH_DIR + '/output.ipynb'
    )

    print('SUCCESS: downloading and executing notebook from github')


    print('START: convert to html')
    #jupyter nbconvert output.ipynb --no-input
    nb = nbformat.read(SCRATCH_DIR + '/output.ipynb', as_version=4)

    # Instantiate the exporter. 
    html_exporter = HTMLExporter()
    html_exporter.template_file = 'nbhtml'

    (body, resources) = html_exporter.from_notebook_node(nb)

    print('SUCCESS: convert to html')

    print('START: save html file')

    write_file = FilesWriter()
    write_file.write(
        output=body,
        resources=resources,
        notebook_name=SCRATCH_DIR + '/index'
        )

    print('SUCCESS: save html file')

    print('START: uploading html file to Cloud Storage')

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    # upload the index.html file
    blob = bucket.blob('index.html')
    blob.upload_from_filename(SCRATCH_DIR + '/index.html')
    print('File index.html uploaded')

    # upload the custom.css file
    blob = bucket.blob('custom.css')
    blob.upload_from_filename('./custom.css')
    print('File custom.css uploaded')

    print('SUCCESS: uploading html and css file to Cloud Storage')

    gc.collect()
    return 'Done processing and updating the report'


#Flask scaffolding for Cloud Run
app = Flask(__name__)

@app.route('/')
def handle_route_function():
    return main_report_generation_function()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

