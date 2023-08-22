from funbuild.core.version import VersionManage


def read_version(version_path):
    manage = VersionManage(version_path)
    manage.read()
    manage.add()
    manage.write()
    return manage.version
