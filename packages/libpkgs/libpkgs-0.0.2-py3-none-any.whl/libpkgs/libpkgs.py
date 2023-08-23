def modify_module_info(module_name, module_version):
    if module_name == 're':
        return None
    elif module_name == 'PIL':
        return f'Pillow=={module_version}'
    elif module_name == 'sklearn':
        return f'scikit-learn=={module_version}'
    else:
        return f'{module_name}=={module_version}'


def libraries():
    print('\n'.join(modify_module_info(m.__name__, m.__version__) for m in globals().values() if getattr(m, '__version__', None) and m.__name__ != 're'))