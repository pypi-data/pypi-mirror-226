import os
import pathlib
import shutil

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render


def mirrors(request, path):
    cur = settings.MIRRORS_DIR.joinpath(path)
    if path == '': path = '/'
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            if name is None:
                for file in request.FILES.getlist('files'):
                    file_path = cur.joinpath(file.name)
                    if not file_path.parent.exists(): os.makedirs(file_path.parent)
                    with open(file_path, 'wb+') as f:
                        for chunk in file.chunks(): f.write(chunk)
            else:
                folder = cur.joinpath(name)
                if not folder.exists(): os.makedirs(folder)
        elif request.method == 'DELETE':
            if cur.exists():
                if cur.is_dir(): shutil.rmtree(cur)
                else: os.remove(cur)
    if cur.is_file(): return FileResponse(open(cur, 'rb'))
    return render(request, 'mirrors.html', {
        "path": pathlib.Path('/').joinpath(path).as_posix(),
        "full_path": request.get_full_path(),
        "parent": '/'.join(request.get_full_path().split('/')[:-1]),
        "files": [{
            "name": file.name,
            "url": pathlib.Path(request.get_full_path()).joinpath(file.name).as_posix(),
        } for file in cur.iterdir()] if cur.exists() else []
    })
