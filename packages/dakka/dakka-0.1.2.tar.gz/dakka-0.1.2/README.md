# Dakka CLI
`dakka` is a Python CLI tool that allows you to interact with an AI agent. It lets you set up configurations composed of several different OpenAPI specs that correspond to server endpoints, which the AI will be allowed to use when answering user questions.

## Installation
You can install `dakka` by cloning the repository and running the `setup.py` file:

```shell
git clone https://github.com/your_username/dakka.git
cd dakka
python setup.py install
```

## Initial Setup

Before using `dakka`, you need to set up your OpenAI key. Run the following command and enter your OpenAI key when prompted:

```shell
dakka install
```

## Configuring OpenAPI Specs

1. Save an OpenAPI spec from a URL or a file path:
```shell
dakka config save https://example.com/klarna.json --name klarna
```
or

```shell
dakka config save path/to/klarna.json --name klarna
```

2. Enable or disable an OpenAPI spec:
```shell
dakka config enable klarna
dakka config disable klarna
```

3. List all installed specs for the default configuration or a specified configuration:
```shell
dakka config list-specs
```
or

```shell
dakka config list-specs --config-name config_name
```

## Configurations

1. Switch to a different configuration:
```shell
dakka config switch config_name
```

2. Set the default configuration:
```shell
dakka config default config_name
```

3. List all available configurations:
```shell
dakka config list-configs
```

## Asking Questions
Ask a question using the default configuration:

```shell
dakka ask "Do I need an umbrella today in Manhattan?"
```
Or specify a different configuration:

```shell
dakka ask -c weather "Do I need an umbrella today in Manhattan?"
```

# Contributing

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py develop
```

### Uploading

```shell
# Update version in setup.py
rm -rf build dist
python setup.py sdist bdist_wheel
twine upload dist/*
```

# TODO
