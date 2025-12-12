import os
import shutil
import sys

from functions import generate_pages_recursive


def main():
    basepath = "/"
    try:
        sys.argv[1]
        basepath = sys.argv[1]
        print(f"base path is '{basepath}'")
    except IndexError:
        print("Default base path is '/'")

    cwd = os.getcwd()
    public_path = f"{cwd}/docs"
    static_path = f"{cwd}/static"
    if os.path.exists(public_path):
        shutil.rmtree(path=public_path, ignore_errors=False)
    os.mkdir(public_path)
    shutil.copytree(
        src=static_path,
        dst=public_path,
        symlinks=False,
        ignore=None,
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=False,
        dirs_exist_ok=True,
    )

    from_path = f"{cwd}/content"
    template_path = f"{cwd}/template.html"
    dest_path = f"{cwd}/docs"

    generate_pages_recursive(from_path, template_path, dest_path, basepath)


main()
