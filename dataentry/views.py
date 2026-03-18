from django.shortcuts import render,redirect
from .utils import get_all_custom_models,check_csv_errors
from uploads.models import Upload
from django.conf import settings
from .tasks import import_data_task
from django.contrib import messages

# Create your views here.
def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")
        
        # store the file in the upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # construct the file path
        relative_path = str(upload.file.url) # This is the relative path to the uploaded file
        base_url = str(settings.BASE_DIR)  # This is the base directory of your project
        
        file_path = base_url + relative_path  # Construct the full file path
        
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request,str(e))
            return redirect('import_data')
        # trigger the importdata cammend

        import_data_task.delay(file_path,model_name)

        messages.success(request,'your data is being imported,you wil be notified once it is done')
        


        return redirect("import_data")
    else:
        custom_models = get_all_custom_models()
        context = {
            "custom_models": custom_models
        }
    return render(request, "dataentry/importdata.html",context)