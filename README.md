# Lexicon Generation Solution

## Description

This solution is designed to take a JSON input file containing a corpus of sentences where each sentence has been tokenised, and each token has been lemmatised and annotated with additional information including part-of-speech tags and morphological features. Then, the solution models the information using data classes and generates a Lexicon in JSON format that includes the following elements:

- An entry per lemma for all lemmas in the input file.
- The part of speech label and all inflection information per lemma.
- A total frequency count for each lemma.
- A total frequency count for each wordform per lemma.

Output Entry Example:

```json
    {"биіктік": {
        "lemma_frequency": 1,
        "pos": [
            "NOUN"
        ],
        "morph_features": [
            "Case=Nom|Number[psor]=Plur,Sing|Person[psor]=3"
        ],
        "word_forms": {
            "Биіктігі": {
                "frequency": 1
            }
        }}
    }
```


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)

## Prerequisites

Before running the app, ensure you have the following prerequisites:

- Python 3.x installed on your development and production environments.
- An Cloud services account if you plan to deploy the app to a Cloud Service (optional but recommended).
- The necessary cloud services and resources (e.g., Blob Storage, Azure Functions) set up if deploying to Azure.


## Installation

1. Clone the repository to your local development environment:

   ```bash
   git clone https://github.com/febaut/LE_OUP.git
   ```

2. Navigate to the app's directory:

   ```bash
   cd your_project_copy_location
   ```

3. See and install the required Python packages:
    ```bash
   pip install -r requirements.txt 
   ```
   
## Usage

To process the JSON files, follow these steps:

1. Place or connect to the JSON input file(s) that you want to process. This can be an Azure Blob Storage container if you are using Azure. The default place is the subfolder 'Data' if you are running the app locally.

2. Configuration: Update input and output paths in the main.py file to specify new locations if needed. Default: 
   
    ```python
    input_json = './Data/sample_parsed_sentences.json'
    output_json = './Data/sample_lexicon.json'
    ```

3. Run the App: Execute the ```main.py``` script using Python:
    ```bash
    python app.py
    ```

On successful excecution, the ```Data``` folder will now contain a new file named ```sample_lexicon.json``` or as renamed in [step 2](#usage).

*Note: The project folder contains an alternative Python Notebook ```LE_notebook.ipynb``` for a more controlled execution of the code.*

## Deployment

If it is required to deploy the app in a production environment, Serverless Azure services can be a good option in terms of reliability and scalability. Additionally as the function would be used ocasionally, a pay-per-use model would be the most efficient one to save costs. Depending on input source and output destination, it can be complemented with Azure Blob Storage. Overview:

- Set up Azure Blob Storage for input and output files if required.
- Deploy the Python app to Azure Functions, triggered by Blob Storage events.
- Configure Azure Function bindings and access settings.
- Update configurations such as input source/location and output destination according to Azure-specific details.

For local deployment, you can run the app on your production server following the same steps as for local development, updating the configuration file for your production environment.


