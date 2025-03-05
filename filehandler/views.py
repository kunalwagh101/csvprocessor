from django.shortcuts import render
from pathlib import Path
import os, pandas as pd, traceback
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CSVUploadForm
from .models import CSVUpload
from .tasks import process_csv_task

def upload_view(request):
    """
    Render the CSV upload form and process file upload.
    """
    context = {}
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            
            upload_instance = CSVUpload.objects.create(file=csv_file)
            file_path = os.path.join(settings.MEDIA_ROOT, upload_instance.file.name)
            
            
            task = process_csv_task.delay(file_path)
            upload_instance.task_id = task.id
            upload_instance.save()

            context['message'] = "File uploaded successfully! Processing started."
            context['task_id'] = task.id
    else:
        form = CSVUploadForm()
    context['form'] = form
    return render(request, 'filehandler/index.html', context)

def get_result(request):
    """
    AJAX view that returns the processed CSV results.
    """

    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'error': 'Missing task_id'}, status=400)
    
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    if result.ready():
        data = result.result
        return JsonResponse({'status': 'SUCCESS', 'data': data})
    else:
        return JsonResponse({'status': 'PENDING'})





def search_data(request):
    """
    correctly mapsto an actual file on to the  server
    """
    try:
        product = request.GET.get('product', '').lower()
        file_path_str = request.GET.get('file_path', '')

    
        if file_path_str.startswith(settings.MEDIA_URL):
            relative_path = file_path_str[len(settings.MEDIA_URL):]
            file_path = Path(settings.MEDIA_ROOT) / relative_path
        else:
            file_path = Path(file_path_str)
      
        if not file_path.exists():
            return JsonResponse({'error': 'Invalid file path.'}, status=400)
        
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            return JsonResponse({'error': f"Error reading CSV: {str(e)}"}, status=400)
        
        # Ensure the CSV has the expected "Product Name" column.
        if 'Product Name' not in df.columns:
            return JsonResponse({'error': 'Column "Product Name" not found in CSV file.'}, status=400)
        
        # Filter the DataFrame by product name if a search term is provided.
        if product:
            df = df[df['Product Name'].str.lower().str.contains(product)]
        
        data = df.to_dict(orient='records')
        return JsonResponse({'data': data})
    except Exception as ex:
        traceback.print_exc()
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)