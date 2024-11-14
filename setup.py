from setuptools import find_packages, setup

setup(
    name="dagster_user_code",
    packages=find_packages(exclude=["dagster_user_code_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
        "dagster-slack",
        "dagster-postgres",
        "dagster-graphql",
        "dagster-webserver",
    ],
    extras_require={
        "dev": [
            "pytest",
            "dagster-webserver",
        ]
    },
)