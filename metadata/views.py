from django.http import FileResponse, HttpRequest
from django.shortcuts import get_object_or_404

from metadata.models import StepExecution


# Create your views here.

def download_parquet_file(request: HttpRequest, pk: int) -> FileResponse:
    obj: StepExecution = get_object_or_404(StepExecution, pk=pk)
    response: FileResponse = FileResponse(open(obj.file_path, 'rb'), as_attachment=True)
    return response
