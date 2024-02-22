import os

from zipfile import ZipFile


def support_gbk(zip_file: ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        try:
            real_name = name.encode('cp437').decode('gbk')
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        except:
            pass
    return zip_file


def unzip_file(zip_filepath, dest_path):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with support_gbk(ZipFile(zip_filepath)) as zfp:
        zfp.extractall(dest_path)


unzip_file(r'C:\Users\Admin\Downloads\卡拉彼丘MMD\香奈美心跳回忆优化版_by_蒻芨_72b93a82878d90c60541036bbde171ae.zip',
           r'C:\Users\Admin\Downloads\卡拉彼丘MMD\香奈美女仆_by_卡拉彼丘_4dbd814e20d144e1cd090ac987fd6330')
