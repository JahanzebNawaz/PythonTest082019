#!/usr/bin/env python
from backend import include_paths


if __name__ == "__main__":
    """Generates a pydev project file"""
    
    with open(".pydevproject", "w") as f:
        f.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?eclipse-pydev version="1.0"?><pydev_project>
<pydev_pathproperty name="org.python.pydev.PROJECT_SOURCE_PATH">
<path>/${PROJECT_DIR_NAME}</path>
</pydev_pathproperty>
<pydev_property name="org.python.pydev.PYTHON_PROJECT_VERSION">python 2.7</pydev_property>
<pydev_property name="org.python.pydev.PYTHON_PROJECT_INTERPRETER">Default</pydev_property>
<pydev_pathproperty name="org.python.pydev.PROJECT_EXTERNAL_SOURCE_PATH">
%s
</pydev_pathproperty>
</pydev_project>''' % "\n".join(["<path>%s</path>" % path for path in reversed(include_paths())]))
