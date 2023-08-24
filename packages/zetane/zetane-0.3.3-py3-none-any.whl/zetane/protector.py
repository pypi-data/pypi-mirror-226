import os, filetype, time, json, io
from tqdm import tqdm
import requests as req
import numpy as np
import zipfile
from zipfile import ZipFile
from pathlib import Path

def api_url_builder(client, *args):
    url = client.address + 'api'
    for arg in args:
        url = url + "/" + arg
    return url

def req_handle(url, client, method, body=None, json_bool=False):
    headers = {"Authorization": "Token " + client.api_key}
    res = None
    if method == "get":
        res = req.get(url, headers=headers)
    if method == "post":
        if json_bool:
            res = req.post(url, json=body, headers=headers)
        else:
            res = req.post(url, data=body, headers=headers)
    if method == "put":
        if json_bool:
            res = req.put(url, json=body, headers=headers)
        else:
            res = req.put(url, data=body, headers=headers)
    if method == "delete":
        res = req.delete(url, data=body, headers=headers)

    #if res is not None and res.status_code != 200 and res.status_code != 201 and res.status_code != 202:
    #    print('STATUS CODE: ', res.status_code)
    #    raise NetworkError(res)

    return res

def check_org_in_user(self, org):
    user = self.user
    for org_temp in user['organizations']:
        if org_temp['name'] == org:
            return True
    print('Organization name is invalid')
    return False

def check_project_in_org(self, org, project_to_check):
    user = self.user
    org_check = None
    for org_tmp in user['organizations']:
        if org_tmp['name'] == org:
            org_check = org_tmp
    for project in org_check['projects']:
        if project['name'] == project_to_check:
            return True
    print('Project name is invalid')
    return False

def get_default_org(json):
    if len(json['organizations']) > 0:
        return json['organizations'][0]['name']

    raise ValueError("No default organization for this user!")

def file_helper(file_path, metadata, name=None):
    filename = os.path.basename(file_path)
    absolute_file_path = os.path.abspath(file_path)
    file_size = os.path.getsize(absolute_file_path)
    file_type = filetype.guess_mime(absolute_file_path)
    if not name:
        name = filename
    body = {"name": name, "filename": filename, "file_type": file_type, "file_size": file_size, "source": "API", "metadata": json.dumps(metadata)}
    newObj = {
            'upload_status': { 'status': "Pending" },
            'dataset_type': 'classification',
        }

    body = {**body, **newObj}
    return body


class NetworkError(Exception):
    def __init__(self, result, message=""):
        self.result = result
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.result.reason + ' ' + str(self.result.status_code) + ' at ' + self.result.url + ' -> ' + self.result.text

class Connection:
    def __init__(self, api_key, address):
        self.api_key = api_key
        self.address = address if address.endswith('/') else f'{address}/'
        self.user = None
        self.org = None
        self.project = None

    def refresh_user(self):
        try:
            res = req_handle(self.address + "users/me", self, 'get')
            self.user = res.json()
        except:
            raise Exception("API KEY is invalid. You can retrieve your api key from: protector.zetane.com")

    def auth_check(self):
        if not hasattr(self, 'api_key') or not self.api_key:
            raise SystemExit('Failed to authenticate API key')

    def config(self, api_key=None, org=None, project=None):
        self.refresh_user()

        if org and check_org_in_user(self, org.lower()):
            self.org = org.lower()
            print('Organization configuration successful')
        else:
            self.org = get_default_org(self.user)
        if self.org and project and check_project_in_org(self, self.org, project):
            self.project = project
            print('Project configuration successful')

class Protector(Connection):
    def __init__(self, api_key, address="https://protector-api-1.zetane.com"):
        super().__init__(api_key, address)
        print('Successfully authenticated: ')
        self.get_orgs_and_projects()
        self.model_filename = None
        self.dataset_filename = None

    def get_orgs_and_projects(self):
        self.auth_check()
        res = req_handle(self.address + 'users/me', self, 'get')
        user = res.json()
        for org in user['organizations']:
            print("Organization: ", org['name'])
            for project in org['projects']:
                print('\t' + "Project: ",  project['name'])

    def create_project(self, name):
        self.auth_check()
        print("Creating project")
        body = {"name": name}
        res = req_handle(self.address + "/api/" + self.org + "/project", self, "post", body)
        if (res.status_code != 201):
            raise RuntimeError("Project was not created : ", res.json())
        return res

    def delete_project(self, name):
        self.auth_check()
        return req_handle(self.address + "/api/" + self.org + "/" + name + "/delete", self, "delete")

    def upload_dataset(self, file_path='', name=None, org=None, project=None):
        # POST /org/project/dataset
        self.auth_check()
        print('Starting dataset upload..')
        self.config(project=project, org=org)
        # metadata = construct_metadata_obj(file_path)
        # if not metadata:
        #     print('Please select a zipped file to upload')
        #     return
        # return
        body = file_helper(file_path, {}, name)
        post_url = api_url_builder(self, self.org, self.project, "dataset")
        res = req_handle(post_url, self, "post", body, True)
        if res.status_code == 201:
            dataset_id = res.json()["id"]
            dataset_filename = res.json()['filename']
            res = upload(self, "datasets", dataset_id, file_path)
            res = confirm_upload(self, "datasets", dataset_id)
            self.dataset_filename = dataset_filename
            print("Completed")
        else:
            raise RuntimeError(f"Dataset did not successfully upload. Error: {res.json()}")
        return res

    def upload_model(self, file_path, name=None, org=None, project=None):
        self.auth_check()
        print('Starting model upload...')
        self.config(project=project, org=org)
        # metadata = construct_metadata_obj(file_path)
        # if not metadata:
        #     print('Please select a zipped file to upload')
        #     return
        body = file_helper(file_path, {}, name)
        post_url = api_url_builder(self, self.org, self.project, "model")
        res = req_handle(post_url, self, "post", body, json_bool=True)
        if res.status_code == 201:
            model_id = res.json()["id"]
            model_filename = res.json()['filename']
            res = upload(self, "models", model_id, file_path)

            res = confirm_upload(self, "models", model_id)
            self.model_filename = model_filename
            print("Completed")
        else:
            raise RuntimeError(f"Model did not successfully upload. Error: {res.json()}")
        return res

    def get_entries(self, datatype, org=None, project=None):
        # GET /org/project/datatype
        self.auth_check()
        print("Getting entries..")
        if datatype != 'models' and datatype != 'datasets':
            return print('Only available datatypes are "models" or "datasets"')
        self.config(project=project, org=org)
        if not self.project:
            return print('Please select a project')
        url = api_url_builder(self, self.org, self.project, datatype)
        res = req_handle(url, self, "get")

        if res.status_code == 200:
            for x in res.json():
                if not x['name']:
                    continue
                print(f'ID: {str(x["id"])} NAME: {x["name"]}')
        return res

    def get_report_status(self, name, org=None, project=None):
        # GET /org/project/report_name
        self.auth_check()
        self.config(project=project, org=org)
        url = api_url_builder(self, self.org, self.project, f"/{name}/status")
        res = req_handle(url, self, "get")
        if res:
            curr_status = res.json()["status"]
            print('Report Name: ' + name)
            print('Report Status: ' + curr_status)
        return res

    def report(self, test_profile_path=None, test_json=dict(), input_shape=list(), model_type=None, organization=None, project=None, model=None, dataset=None, autoRun=False):
        # POST /org/project/run
        self.auth_check()
        self.config(organization=organization, project=project)
        model_filename = model if model else self.model_filename
        dataset_filename = dataset if dataset else self.dataset_filename

        validation_errors = list()
        if not input_shape:
           validation_errors.append('Please specify a model input_shape as a list in the format [B H W C]')
        if not model_type and model_type not in ['object_detection', 'image_classification']:
            validation_errors.append('Please specify a model input type: either "object_detection" or "image_classification"')
        if not model and not hasattr(self, 'model'):
            validation_errors.append('Please specify which model you wish to use')
        if not dataset and not hasattr(self, 'dataset'):
            validation_errors.append('Please specify which dataset you wish to use')
        if not project and not hasattr(self, 'project'):
            validation_errors.append('Please specify which project you wish to use')
        if not test_json and validate_file_type(test_profile_path):
            validation_errors.append('Please provide a json test spec or a path to a file containing a json test spec')

        if len(validation_errors) > 0:
            for error in validation_errors:
                print(error)
            return

        #get model ID
        try:
            url = api_url_builder(self, organization, project, 'models')
            res = req_handle(url, self, "get")
            if not res.status_code == 200:
                print('Report creation failed - invalid model selection')
                print(res.json())
                return
            else:
                models_json = res.json()
                models_match = [v['id'] for v in models_json if v['filename'] == model_filename]
                model_id = max(models_match)
        except:
            print('Invalid model selection - please select from the following or upload a new model:')
            return self.get_entries('models')

        #get dataset ID
        try:
            url = api_url_builder(self, organization, project, 'datasets')
            res = req_handle(url, self, "get")
            if not res.status_code == 200:
                print('Report creation failed - invalid dataset selection')
                print(res.json())
            else:
                dataset_json = res.json()
                datasets_match = [v['id'] for v in dataset_json if v['filename'] == dataset_filename]
                dataset_id = max(datasets_match)
        except:
            print("Invalid dataset selection - please select from the following or upload a new dataset:")
            return self.get_entries('datasets')

        test_series_name = "Test Report"
        if test_profile_path is not None:
            test_series_name = test_profile_path.split('/')[-1]
            with open(test_profile_path) as f:
                test_json = json.load(f)

        crafted_test_profile = validate_test_json(test_json, model_filename, model_id,input_shape, model_type, dataset_filename, dataset_id, test_series_name)

        url = api_url_builder(self, self.org, self.project, "run")
        body = {"save": False, "data": crafted_test_profile, "supValues": { "numPrimaryTests": '', "numComposedTests": '', "totalTestRuns": '', "totalXaiApplied": '' }}
        res = req_handle(url, self, "post", body, json_bool=True)
        name = None
        name = res.json()["name"]

        if res.status_code == 201:
            print("Starting report: " + name)
            print('When completed, your report can be found at the following url:')
            link_url = f"https://protector.zetane.com/{self.org}/{self.project}/runs/{name}"
            print(link_url)
            if (autoRun):
                i = 0
                sleep_time = 10
                status_url = f"{self.address}api/{self.org}/{self.project}/{name}/status"
                while True:
                    time.sleep(sleep_time)
                    i += 1
                    res = req_handle(status_url, self, "get")
                    if res.status_code == 200:
                        print("Running... " + str(sleep_time * i) + " seconds")
                        status = res.json()["status"]
                        if status == "Ready":
                            print(f"Report completed! View the results {link_url}")
                            return True
                        elif status == "Error":
                            print(f"Error running report! View the error logs: {res.json()['error']}")
                            return False
        else:
            raise NetworkError(res, "Failed to schedule report")

        return res



############################## END OF CLASS ######################################
# def handleErr(errCode, jobType, res):
#     if jobType == 'report' and (errCode != 200 or errCode != 201):
#         raise NetworkError(res, "Failed Report")

#     return

def confirm_upload(client, datatype, id):
    # PUT /org/project/datatype/id
    body = {"upload_status": {"status": "Ready"}}
    url = api_url_builder(client, client.org, client.project, datatype, f"{str(id)}")
    return req_handle(url, client, "put", body, json_bool=True)


def upload(client, datatype, id, file):
    FILE_CHUNK_SIZE = 10000000  # 10MB
    if isinstance(file, str):
        absolute_file_path = os.path.abspath(file)
        file_size = os.path.getsize(absolute_file_path)
        file_path = Path(absolute_file_path)
        file_type = file_path.suffix
        file_obj = open(absolute_file_path, "rb")
    else:
        file_size = file.getbuffer().nbytes
        file_type = "application/zip"
        file_obj = file

    NUM_CHUNKS = (file_size - 1) // FILE_CHUNK_SIZE + 1

    base_url = api_url_builder(client, client.org, client.project, datatype, f"{str(id)}")

    res = req_handle(base_url + '/upload', client, "post", {"fileType": file_type})

    # Initialize multi-part
    upload_id = res.json()["uploadId"]

    # Upload multi-part
    parts = []
    for index in tqdm(range(NUM_CHUNKS)):
        offset = index * FILE_CHUNK_SIZE
        file_obj.seek(offset, 0)

        res = req_handle(base_url + "/upload_part",
                        client,
                        "post",
                       {"part": index + 1, "uploadId": upload_id})
        presigned_url = res.json()["presignedUrl"]
        res = req.put(presigned_url, data=file_obj.read(FILE_CHUNK_SIZE), headers={"Content-Type": file_type})
        parts.append({"ETag": res.headers["etag"][1:-1], "PartNumber": index + 1})

    if isinstance(file, str):
        file_obj.close()
    # Finalize multi-part
    res = req_handle(base_url + "/upload_complete", client, "post", {"parts": parts, "uploadId": upload_id}, json_bool=True)
    return res


def build_image(client, model_id):
    # POST /org/project/id/image
    url = api_url_builder(client, client.org, client.project, f"{str(model_id)}", "image")
    res = req_handle(url, client, "post", json.dumps({id: id}))
    if res.status_code == 201:
        name = res.json()["name"]
        i = 0
        while True:
            time.sleep(10)
            i += 1
            url = api_url_builder(client) + f"{name}/image/status"
            res = req_handle(url, client, "get")
            if res.status_code == 200:
                print("Building... " + str(10 * i) + " seconds")
                status = res.json()["status"]["status"]
                if status != "Running" and status != "Pending":
                    break
            else:
                print('Not building image...')
                break
    return res

def recurz(arrOfPaths, dict):
    if len(arrOfPaths) > 1:
        if arrOfPaths[0] not in dict:
            dict[arrOfPaths[0]] = {'type': '', 'size': ''}
        recurz(arrOfPaths[1:], dict[arrOfPaths[0]])
    else:
        dict[arrOfPaths[0]]= {'type': arrOfPaths[0].split('.')[-1] if '.' in arrOfPaths[0] else '', 'size': ''}
    return

def construct_metadata_obj(file_path):
    absolute_file_path = os.path.abspath(file_path)
    if not absolute_file_path.endswith('.zip'):
        return False
    metadata = {}
    with ZipFile(absolute_file_path, 'r') as zipObj:
        listOfilesFirst = zipObj.namelist()
        listOfFiles = [x for x in listOfilesFirst if 'macosx' not in x.lower()]
        for fileName in listOfFiles:
            arrOfPaths = fileName.split('/')
            recurz(arrOfPaths, metadata)

        return metadata


def validate_file_type(file_path):
    absolute_file_path = os.path.abspath(file_path)

    file_size = os.path.getsize(absolute_file_path)
    file_type = Path(absolute_file_path).suffix
    # print(file_type, file_size, absolute_file_path)
    if file_type != 'application/json' and not '.json' in file_path:
        return False
    return True

def check_if_valid_test(test, max, min, intervals):
    test = test.replace(' ', '_')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)

    absolute_file_path = os.path.abspath(dname+'/user_transformation_table.json')

    with open(absolute_file_path, 'r', encoding='utf-8') as reference_file:

        reference_obj = json.loads(reference_file.read())
        if not max or not min or not intervals:
            return False

        if test not in reference_obj:
            return False
        max_lim = reference_obj[test]['range_max']
        min_lim = reference_obj[test]['range_min']

        if max_lim < max or max_lim < min:
            return False
        if min_lim > min or min_lim > max:
            return False

    return True

def validate_test_json(tests, model_filename, model_id, input_shape, model_type, dataset_filename, dataset_id, test_series='dev'):
    testArr = [] #array of test objects
    xaiObj = {}
    for test in tests:
        #first check if the test is a real test & if the ranges and intervals are within acceptable limits
        if not check_if_valid_test(test, tests[test]['max'], tests[test]['min'], tests[test]['intervals']):
            print(f'{test} was invalid and was not included.')
            continue
        #if both of above are good, then construct object
        if 'xai' in tests[test]:
            #add to xai obj
            xaiObj = xaiObj.get(test, []) + tests[test]['xai']

        test_obj = {
            "name": test,
            "number_of_tests": tests[test]['intervals'],
            "sequence": {
                "function": test,
                "min_range": tests[test]['min'],
                "max_range": tests[test]['max']
            }
        }
        testArr.append(test_obj)

    test = {
        "info": {
            "specs_version": 0.1,
            "source": 'api',
            "report_id": 'dev_test1'
        },
        "model": {
            "model_id": model_id,
            "mlflow_model_folder_path": '',
            "filename": model_filename,
            "input_shape": input_shape,
        },
        "dataset": {
            "dataset_id": dataset_id,
            "dataset_folder_path": '',
            "labels_file_path": '',
            "class_list": '',
            "class_list_path": '',
            "filename": dataset_filename
        },
        "ground_truth": {
            "annotations_path": '',
        },
        "model_type": model_type,
        "sample_size": {
            "number": 0,
            "percentage": 100
        },
        "framework": 'image_classification',
        "xai": xaiObj,
        "robustness": {
            "test_series": test_series,
            "tests": testArr
        }
    }
    return test

class Monitor(Connection):
    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.memory = None
        self.compression = zipfile.ZIP_DEFLATED
        self._reset()

    def __enter__(self):
        return self

    def close(self):
        self.memory.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _reset(self):
        self.names = set()
        self.header = {"inputs": [], "outputs": []}
        if self.memory is not None:
            self.memory.close()
        self.memory = io.BytesIO(b'')

    def _add_array(self, is_input, name, numpy_array, named_array):
        if not isinstance(numpy_array, np.ndarray):
            raise Exception("Expected a numpy array. Got: " + type(numpy_array))

        instance = {"name": name,
                    "shape": numpy_array.shape,
                    "type": numpy_array.dtype.str,
                    "named": False}

        if named_array is not None:
            if not isinstance(named_array, np.ndarray):
                raise Exception("Expected a numpy array. Got: " + type(named_array))
            if named_array.dtype.str[1] != "U":
                raise Exception("Expected np._object. Got: " + named_array.dtype)
            if len(numpy_array.shape) != named_array.size:
                if len(numpy_array.shape) != len(named_array.shape):
                    raise Exception("Invalid named array")
                for i in range(len(numpy_array.shape)):
                    if numpy_array.shape[i] % named_array.shape[i] != 0:
                        raise Exception("Invalid named array")
            instance["named"] = True

        if name not in self.names:
            if is_input:
                self.header["inputs"].append(instance)
            else:
                self.header["outputs"].append(instance)
            self.names.add(name)
        else:
            raise Exception("The array \'" + name + "\' already exists")


        with ZipFile(self.memory, 'a', self.compression) as file:
            file.writestr(name, numpy_array.tobytes())
            if named_array is not None:
                file.writestr(name + "_named", named_array.tobytes())

    def add_input(self, name, numpy_array, named_array=None):
        self.auth_check()
        self._add_array(True, name, numpy_array, named_array)

    def add_output(self, name, numpy_array, named_array=None):
        self.auth_check()
        self._add_array(False, name, numpy_array, named_array)

    def send(self, name, org=None, project=None):
        self.auth_check()
        with ZipFile(self.memory, 'a', self.compression) as file:
            file.writestr("header.json", json.dumps(self.header))

        self.config(project=project, org=org)

        if name[-4:] != ".zip":
            zip_name = name + ".zip"
        else:
            zip_name = name

        body = {"filename": zip_name, "file_size": self.memory.getbuffer().nbytes, "metadata": json.dumps("")}
        newObj = {
            'upload_status': {'status': "Pending"},
            'dataset_type': 'classification',
        }

        body = {**body, **newObj}
        post_url = api_url_builder(self, "tensor")
        res = req_handle(post_url, self, "post", body)

        dataset_id = res.json()["id"]
        res = upload(self, "tensors", dataset_id, self.memory)
        res = confirm_upload(self, "tensors", dataset_id)

        print("Completed")
        return res
