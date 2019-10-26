import setuptools

setuptools.setup(
    name = 'gitlab_ci_env',
    version = '1.0.0',
    python_requires='>=3.6',
    install_requires=['requests>=2.21.0'],
    py_modules=['gitlab_ci_env'],
    entry_points = {
        'console_scripts': [
            'gitlab-ci-env=gitlab_ci_env:main'
        ]
    }
)
