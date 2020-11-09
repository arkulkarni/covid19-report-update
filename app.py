import json
import papermill as pm
import nbformat
import gc

from nbconvert import HTMLExporter
from nbconvert.writers import FilesWriter

import os

from flask import Flask

SCRATCH_DIR = '.'

app = Flask(__name__)


@app.route('/')
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
    # html_exporter.template_file = 'nbhtml'

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

    # print('START: uploading html file to S3')

    # s3_client = boto3.client('s3')
    # s3_client.upload_file('/tmp/index.html', 'covid19report', 'index.html', ExtraArgs={'ContentType': "text/html"})

    # print('SUCCESS: uploading html file to S3')

    gc.collect()
    return 'Done processing and updating the report'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

