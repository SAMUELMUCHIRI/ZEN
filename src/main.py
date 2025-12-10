import os
import shutil


def main():
    public_path = f"{os.getcwd()}/public"
    static_path = f"{os.getcwd()}/static"
    print(public_path)
    print(static_path)
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


main()
