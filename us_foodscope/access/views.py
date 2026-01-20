from django.shortcuts import render
from .services import predict_access, classify_access, cluster_access
from .forms import AccessPredictionForm, AccessClusteringForm
from .models import AccessPredictionHistory
from users.decorators import prediction_access_required
from django.shortcuts import redirect

@prediction_access_required('access')
def access_clustering_clear(request):
    return redirect("access:clustering")



def access_home(request):
    return render(request, "access/access_home.html")


# ✅ MUST match model training order (10 prediction features)
PREDICTION_COLS = [
    "PCT_LACCESS_POP10",
    "LACCESS_LOWI15",
    "LACCESS_HISP15",
    "LACCESS_NHASIAN15",
    "LACCESS_BLACK15",
    "Median_Income",
    "Poverty_Rate",
    "Food_Tax_Rate_14",
    "PCT_65OLDER10",
    "PCT_18YOUNGER10",
]


@prediction_access_required('access')
def access_prediction(request):
    form = AccessPredictionForm()
    prediction_result = None
    classification_result = None
    cluster_result = None
    error_message = None

    # ✅ LOAD HISTORY
    prediction_history = []
    if request.user.is_authenticated:
        prediction_history = AccessPredictionHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")[:5]

    # ✅ REUSE HISTORY
    load_id = request.GET.get("load_id")
    if load_id and request.user.is_authenticated and request.method == "GET":
        try:
            hist_item = AccessPredictionHistory.objects.get(id=load_id, user=request.user)
            form = AccessPredictionForm(initial=hist_item.input_data)
        except AccessPredictionHistory.DoesNotExist:
            pass

    # ✅ POST PREDICTION
    if request.method == "POST":
        form = AccessPredictionForm(request.POST)

        if form.is_valid():
            try:
                cleaned = form.cleaned_data

                # ✅ prediction features (10)
                prediction_features = [cleaned[col] for col in PREDICTION_COLS]

                prediction_result = float(predict_access(prediction_features))
                classification_result = str(classify_access(prediction_features))

                # ✅ clustering features (9) with POPLOSS10 auto-filled = 0
                clustering_features = [
                    cleaned["Poverty_Rate"],
                    cleaned["Median_Income"],
                    cleaned["PCT_65OLDER10"],
                    cleaned["PCT_18YOUNGER10"],
                    0,  # ✅ POPLOSS10 auto-filled (not in form)
                    cleaned["LACCESS_HISP15"],
                    cleaned["LACCESS_NHASIAN15"],
                    cleaned["LACCESS_BLACK15"],
                    cleaned["PCT_LACCESS_POP10"],
                ]

                cluster_result = int(cluster_access(clustering_features))

                # ✅ SAVE HISTORY
                if request.user.is_authenticated:
                    AccessPredictionHistory.objects.create(
                        user=request.user,
                        input_data=cleaned,
                        prediction_value=prediction_result
                    )

                # ✅ reload history
                prediction_history = AccessPredictionHistory.objects.filter(
                    user=request.user
                ).order_by("-created_at")[:5]

            except Exception as e:
                error_message = f"Prediction Error: {str(e)}"

    context = {
        "form": form,
        "prediction_result": prediction_result,
        "classification_result": classification_result,
        "cluster_result": cluster_result,
        "error_message": error_message,
        "prediction_history": prediction_history,
    }

    return render(request, "access/access_home.html", context)


@prediction_access_required('access')
def access_clustering(request):
    cluster = None
    cluster_label = None
    error_message = None

    # ✅ Human-readable labels for your 3 clusters
    CLUSTER_LABELS = {
        0: "Moderate Access Risk",
        1: "High Minority + High Access Risk",
        2: "High Poverty + High Low Access",
    }

    form = AccessClusteringForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            cleaned = form.cleaned_data

            # ✅ Must match scaler/PCA training order (9 features)
            features = [
                cleaned["Poverty_Rate"],
                cleaned["Median_Income"],
                cleaned["PCT_65OLDER10"],
                cleaned["PCT_18YOUNGER10"],
                cleaned["POPLOSS10"],
                cleaned["LACCESS_HISP15"],
                cleaned["LACCESS_NHASIAN15"],
                cleaned["LACCESS_BLACK15"],
                cleaned["PCT_LACCESS_POP10"],
            ]

            cluster = int(cluster_access(features))
            cluster_label = CLUSTER_LABELS.get(cluster, "Unknown Cluster")

        except Exception as e:
            error_message = f"Clustering Error: {str(e)}"

    return render(request, "access/access_clustering.html", {
        "form": form,
        "cluster": cluster,
        "cluster_label": cluster_label,
        "error_message": error_message,
    })
