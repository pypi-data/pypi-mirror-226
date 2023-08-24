#     Copyright (c) 2023, Kevan White (Thyripian)
#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are met:
#       Compliance with MIT License clauses.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Flask, render_template, request
import webbrowser
import threading
import datamason as dm

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main interface page
    return render_template('index.html')

@app.route('/clean', methods=['POST'])
def clean_data():
    # Logic to clean the data based on user input
    # You can receive the user input using request.form
    # Call the appropriate functions from the datamason package
    return "Data cleaned successfully!"

def run_interface():
    # Open the web browser and navigate to the localhost URL
    webbrowser.open("http://127.0.0.1:5000/")
    # Run the Flask app
    app.run()

def launch():
    # Launch the interface in a separate thread, allowing the user to continue using the Python session
    threading.Thread(target=run_interface, daemon=True).start()

# You can then call dm.interface.launch() to launch the interface
