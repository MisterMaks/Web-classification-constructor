from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import Form1
from .forms import FillingGapsMethodInsertMeanMode, FillingGapsMethodHardRemoval, FillingGapsMethodLinearImputer
from .forms import DeletingAnomaliesMethodThreeSigma, DeletingAnomaliesMethodGrubbs, \
    DeletingAnomaliesMethodInterquartile, DeletingAnomaliesMethodIsolationForest, DeletingAnomaliesMethodElliptic, \
    DeletingAnomaliesMethodSVM, DeletingAnomaliesMethodApproximate, DeletingAnomaliesMethodLocalFactor
from .forms import FeatureSelectionMethodVarianceThreshold, FeatureSelectionMethodSelectKBest, \
    FeatureSelectionMethodSelectPercentile, FeatureSelectionMethodSelectFpr, FeatureSelectionMethodSelectFdr, \
    FeatureSelectionMethodSelectFwe, FeatureSelectionMethodGenericUnivariateSelect, FeatureSelectionMethodRFE, \
    FeatureSelectionMethodSelectFromModel
from .forms import CompositionMethodVoting, CompositionMethodAdaboost, CompositionMethodStacking
from .forms import NeuralNetwork, DecisionTree, LogisticRegression
from .forms import UploadFileForm
from Web_classification_constructor_backend.settings import MEDIA_ROOT
from packages.check_df import check_df
from Classification_constructor_code.code.main import main_function
from urllib.parse import urlencode
import json
import os
from zipfile import ZipFile


# Create your views here.


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def post_form_1(request):
    form_1 = Form1(request.POST)
    data = {}
    if form_1.is_valid():
        for field in form_1.cleaned_data.keys():
            data[field.replace('_', ' ') if field != 'test_ratio' else field] = form_1.cleaned_data[field]
        response = {"form_1": form_1,
                    "data": data}
        print(response["data"])
        return response
    response = {"form_1": form_1,
                "data": data}
    print(response)
    return response


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def button_click_tracking(request):
    if "button exit" in request.POST.keys():
        return redirect("/logout")
    if "button send" in request.POST.keys():
        response = post_form_1(request)
        data = {}
        if response["data"]:
            for key, value in response["data"].items():
                data[key.replace(' ', '_') if key != 'test_ratio' else key] = value
            url_get_data = urlencode(data)
            return redirect(f'/2/?{url_get_data}')
        return render(request, "form_1.html", response)
    else:
        form_1 = Form1(request.POST)
        response = {"form_1": form_1,
                    "data": None}
        return render(request, "form_1.html", response)


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def post_form_2(request, common_params):
    # print(common_params)

    # name_of_model_with_time_of_create = f"{common_params['name of model']}" \
    #     f"({datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')})"

    # filling_gaps_method = FillingGapsMethodInsertMeanMode(request.POST, prefix="filling_gaps_method")
    if common_params['filling gaps method'] == 'InsertMeanMode':
        filling_gaps_method = FillingGapsMethodInsertMeanMode(request.POST, prefix="filling_gaps_method")
    if common_params['filling gaps method'] == 'HardRemoval':
        filling_gaps_method = FillingGapsMethodHardRemoval(request.POST, prefix="filling_gaps_method")
    if common_params['filling gaps method'] == 'LinearImputer':
        filling_gaps_method = FillingGapsMethodLinearImputer(request.POST, prefix="filling_gaps_method")

    # deleting_anomalies_method = DeletingAnomaliesMethodThreeSigma(request.POST)
    if common_params['deleting anomalies method'] == 'ThreeSigma':
        deleting_anomalies_method = DeletingAnomaliesMethodThreeSigma(request.POST, prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'Grubbs':
        deleting_anomalies_method = DeletingAnomaliesMethodGrubbs(request.POST, prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'Interquartile':
        deleting_anomalies_method = DeletingAnomaliesMethodInterquartile(request.POST,
                                                                         prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'IsolationForest':
        deleting_anomalies_method = DeletingAnomaliesMethodIsolationForest(request.POST,
                                                                           prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'Elliptic':
        deleting_anomalies_method = DeletingAnomaliesMethodElliptic(request.POST, prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'SVM':
        deleting_anomalies_method = DeletingAnomaliesMethodSVM(request.POST, prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'Approximate':
        deleting_anomalies_method = DeletingAnomaliesMethodApproximate(request.POST, prefix="deleting_anomalies_method")
    if common_params['deleting anomalies method'] == 'LocalFactor':
        deleting_anomalies_method = DeletingAnomaliesMethodLocalFactor(request.POST, prefix="deleting_anomalies_method")

    # feature_selection_method = FeatureSelectionMethodVarianceThreshold(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'VarianceThreshold':
        feature_selection_method = FeatureSelectionMethodVarianceThreshold(request.POST,
                                                                           prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectKBest':
        feature_selection_method = FeatureSelectionMethodSelectKBest(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectPercentile':
        feature_selection_method = FeatureSelectionMethodSelectPercentile(request.POST,
                                                                          prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectFpr':
        feature_selection_method = FeatureSelectionMethodSelectFpr(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectFdr':
        feature_selection_method = FeatureSelectionMethodSelectFdr(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectFwe':
        feature_selection_method = FeatureSelectionMethodSelectFwe(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'GenericUnivariateSelect':
        feature_selection_method = FeatureSelectionMethodGenericUnivariateSelect(request.POST,
                                                                                 prefix="feature_selection_method")
    if common_params['feature selection method'] == 'RFE':
        feature_selection_method = FeatureSelectionMethodRFE(request.POST, prefix="feature_selection_method")
    if common_params['feature selection method'] == 'SelectFromModel':
        feature_selection_method = FeatureSelectionMethodSelectFromModel(request.POST,
                                                                         prefix="feature_selection_method")

    # composition_method = CompositionMethodVoting(request.POST, prefix="composition_method")
    if common_params['composition method'] == 'voting':
        composition_method = CompositionMethodVoting(request.POST, prefix="composition_method")
    if common_params['composition method'] == 'adaboost':
        composition_method = CompositionMethodAdaboost(request.POST, prefix="composition_method")
    if common_params['composition method'] == 'stacking':
        composition_method = CompositionMethodStacking(request.POST, prefix="composition_method")

    base_algorithms = {}
    if common_params['neural network number'] not in [0, None]:
        for i in range(common_params['neural network number']):
            neural_network = NeuralNetwork(request.POST, prefix=f'neural_network_{i + 1}')
            base_algorithms[f'neural network #{i + 1}'] = neural_network
    if common_params['decision tree number'] not in [0, None]:
        for i in range(common_params['decision tree number']):
            decision_tree = DecisionTree(request.POST, prefix=f'decision_tree_{i + 1}')
            base_algorithms[f'decision tree #{i + 1}'] = decision_tree
    if common_params['logistic regression number'] not in [0, None]:
        for i in range(common_params['logistic regression number']):
            logistic_regression = LogisticRegression(request.POST, prefix=f'logistic_regression_{i + 1}')
            base_algorithms[f'logistic regression #{i + 1}'] = logistic_regression

    all_params = {
        # "name of model with time of create": name_of_model_with_time_of_create
    }

    if deleting_anomalies_method.is_valid():
        if common_params["deleting anomalies method"] not in ["ThreeSigma"]:
            all_params["deleting anomalies method"] = {common_params["deleting anomalies method"]: {}}
            for field in deleting_anomalies_method.cleaned_data.keys():
                all_params["deleting anomalies method"][common_params["deleting anomalies method"]][field] = \
                    deleting_anomalies_method.cleaned_data[field]
        else:
            deleting_anomalies_method = None
            all_params["deleting anomalies method"] = common_params["deleting anomalies method"]

    if feature_selection_method.is_valid():
        all_params["feature selection method"] = {common_params["feature selection method"]: {}}
        for field in feature_selection_method.cleaned_data.keys():
            all_params["feature selection method"][common_params["feature selection method"]][field] = \
                feature_selection_method.cleaned_data[field]

    all_params["base algorithms"] = {}
    for key in base_algorithms:
        if base_algorithms[key].is_valid():
            all_params["base algorithms"][key] = {}
            for field in base_algorithms[key].cleaned_data.keys():
                all_params["base algorithms"][key][field] = base_algorithms[key].cleaned_data[field]

    # all_params["name of model"] = common_params["name of model"]

    if filling_gaps_method.is_valid():
        if common_params["filling gaps method"] not in ["HardRemoval", "LinearImputer"]:
            all_params["filling gaps method"] = {common_params["filling gaps method"]: {}}
            for field in filling_gaps_method.cleaned_data.keys():
                all_params["filling gaps method"][common_params["filling gaps method"]][field] = \
                    filling_gaps_method.cleaned_data[field]
        else:
            filling_gaps_method = None
            all_params["filling gaps method"] = common_params["filling gaps method"]

    if composition_method.is_valid():
        if common_params["composition method"] not in ["voting"]:
            all_params["composition method"] = {common_params["composition method"]: {}}
            for field in composition_method.cleaned_data.keys():
                all_params["composition method"][common_params["composition method"]][field] = \
                    composition_method.cleaned_data[field]
        else:
            composition_method = None
            all_params["composition method"] = common_params["composition method"]

    all_params["test_ratio"] = common_params["test_ratio"]
    all_params["common params"] = common_params

    print(all_params)

    response = {
        "filling_gaps_method": filling_gaps_method,
        "deleting_anomalies_method": deleting_anomalies_method,
        "feature_selection_method": feature_selection_method,
        "composition_method": composition_method,
        "base_algorithms": base_algorithms,
        "data": all_params,
        "logistic_regression_number": common_params['logistic regression number']
    }

    return response


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def button_click_tracking_2(request):
    data = dict(request.GET)
    common_params = {}
    for key, value in data.items():
        if key in ['neural_network_number', 'decision_tree_number', 'logistic_regression_number']:
            if value[0] != 'None':
                value[0] = int(value[0])
            else:
                value[0] = 0
        if key == 'test_ratio':
            if value[0] != 'None':
                value[0] = float(value[0])
            else:
                value[0] = None
        common_params[key.replace('_', ' ') if key != 'test_ratio' else key] = value[0]

    # print(common_params)

    if "button exit" in request.POST.keys():
        return redirect("/logout")
    if "button send 2" in request.POST.keys():
        response = post_form_2(request, common_params)
        with open(f"{MEDIA_ROOT}/user_all_params.json", 'w') as all_params_file:
            json.dump(response["data"], all_params_file)
        return redirect(f'/3')
        # return render(request, "form_2.html", response)
    else:
        response = post_form_2(request, common_params)
        return render(request, "form_2.html", response)


def handle_uploaded_file(file, filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'Classification_constructor_code', 'Input', filename)

    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def create_archive():
    current = os.path.dirname(__file__)
    z = ZipFile(os.path.join(current, '..', 'user_files', 'results.zip'), 'w')
    path = os.path.join(current, '..', 'Classification_constructor_code', 'App', 'images')
    for image in os.listdir(path):
        z.write(os.path.join(path, image), arcname=f'Images/{image}')
        os.remove(os.path.join(path, image))
    path = os.path.join(current, '..', 'Classification_constructor_code', 'App', 'models')
    for model in os.listdir(path):
        z.write(os.path.join(path, model), arcname=f'Models/{model}')
        os.remove(os.path.join(path, model))
    path = os.path.join(current, '..', 'Classification_constructor_code', 'Output')
    for file in os.listdir(path):
        z.write(os.path.join(path, file), arcname=f'Files/{file}')
        os.remove(os.path.join(path, file))
    z.close()


def remove_tmp():
    os.remove(os.path.join(os.path.dirname(__file__), '..', 'Classification_constructor_code', 'Input', 'train.csv'))
    os.remove(os.path.join(os.path.dirname(__file__), '..', 'Classification_constructor_code', 'Input', 'test.csv'))
    os.remove(os.path.join(os.path.dirname(__file__), '..', 'user_files', 'user_all_params.json'))


@csrf_exempt
# @login_required
@require_http_methods(["GET", "POST"])
def button_click_tracking_3(request):
    if "button exit" in request.POST.keys():
        return redirect("/logout")
    if "button send 3" in request.POST.keys():
        if 'file_train' in request.FILES and 'file_test' in request.FILES:
            upload_file_form = UploadFileForm(request.POST, request.FILES)
            if upload_file_form.is_valid():
                check_train = check_df(request.FILES['file_train'], is_train=True)
                check_test = check_df(request.FILES['file_test'], is_train=False)
                if not check_train[0]:
                    response = {"data": check_train[1]}
                elif not check_test[0]:
                    response = {"data": check_test[1]}
                else:
                    handle_uploaded_file(request.FILES['file_train'], 'train.csv')
                    handle_uploaded_file(request.FILES['file_test'], 'test.csv')
                    response = {"data": "Файлы загружены", "begin_work": True}
                response["upload_file_form"] = upload_file_form
                return render(request, "form_3.html", response)
        else:
            return render(request, "form_3.html", {'upload_file_form': UploadFileForm()})
    if "button send 4" in request.POST.keys():

        main_function()
        create_archive()
        stages_dict = {
            'Считывание файлов': 'Завершено',
            'Заполнение пропусков': 'Завершено',
            'Удаление выбросов': 'Завершено',
            'Нормализация': 'Завершено',
            'Отбор признаков': 'Завершено',
            'Обучение': 'Завершено',
            'Предсказание': 'Завершено',
            'Создание архива с результатами': 'Завершено'
        }
        with open(f"{MEDIA_ROOT}/stages.json", 'w') as stages_json:
            json.dump(stages_dict, stages_json, ensure_ascii=False)
        remove_tmp()

        response = {
            "data": "Work is completed!!!",
            "upload_file_form": UploadFileForm()
        }
        return render(request, "form_3.html", response)
    else:
        upload_file_form = UploadFileForm()
    return render(request, 'form_3.html', {'upload_file_form': upload_file_form})
