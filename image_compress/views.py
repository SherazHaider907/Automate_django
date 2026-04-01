from django.shortcuts import render
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse
from django.core.files.base import ContentFile


def compress(request):
    user = request.user

    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)

        if form.is_valid():
            original_image = form.cleaned_data['original_image']
            quality = form.cleaned_data['quality']

            compress_image = form.save(commit=False)
            compress_image.user = user

            # Open image
            img = Image.open(original_image)

            # Convert if needed
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            # Compress
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)

            # New filename
            filename = original_image.name.split('.')[0] + "_compressed.jpg"

            # Save to model
            compress_image.compressed_image.save(
                filename,
                ContentFile(buffer.getvalue()),
                save=False
            )

            compress_image.save()

            # 🔥 FORCE DOWNLOAD
            response = HttpResponse(buffer.getvalue(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

    else:
        form = CompressImageForm()

    return render(request, "image_compress/compress.html", {'form': form})