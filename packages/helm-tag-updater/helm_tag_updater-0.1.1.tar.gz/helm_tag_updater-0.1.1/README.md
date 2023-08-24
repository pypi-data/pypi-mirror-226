<div align="center">
<h1> ⎈ helm_tag_updater</h1>
<p>A python CLI application which updates a helm `values.yaml` image tag</p>
</div>

## Introducing

`helm_tag_updater` is a python cli tool which can update `values.yaml` fields inside a CI/CD pipeline. Also it's an easy to use tool for implementing [GitOps](https://about.gitlab.com/topics/gitops/#:~:text=GitOps%20is%20an%20operational%20framework,applies%20them%20to%20infrastructure%20automation.) principles.

## Why `helm_tag_updater` / Alternatives

`helm_tag_updater` is a simple to use cli which is also support `regular expression tag matching` and `prod` mode.

| Tool             | Easy to use | Additional setup required                                                                                |         Additional checks        |
|------------------|:-----------:|----------------------------------------------------------------------------------------------------------|:--------------------------------------------:|
| helm_tag_updater |           ✅ | No additional setup required                                                                             | Regular expression matching, production mode |
| yq               |           ✅ | No additional setup required, but yq breaks yaml structure (https://github.com/mikefarah/yq/issues/1248) |                       ❎                      |
| kustomize        |          ✅  | Require additional `kustomization.yaml`  file                                                            |                       ❎                      |
| sed              |      ❎      | Supported by all Linux systems                                                                           |                       ❎                      |

* **You can setup tag checking and regular expression matching using linux tools, but `helm_tag_updater` support it out of the box**

## Installation

You can install `helm_tag_updater` using:

**Docker**

```bash
docker pull fayvori/helm_tag_updater
```

**pip**
```bash
pip install helm_tag_updater
```

**Brew**
```bash 
brew install fayvori/helm_tag_updater
```

## Usage

![helm_image_updater tag](./assets/help-message.png)

 flag                        | default                       | purpose
-----------------------------|-------------------------------|---------
 `--help`, `-h`              |  `None`                       | Prints `help` message and exit
 `--tag`,  `-t`              |  `None`                       | Tag that should be applied on `values.yaml` file. NOTE: If you set `-p` or `--prod` flag tag should match regular expression `-e` `--expression` flag
 `--filepath`, &nbsp; `-f`   |  `None`                       | Path to the `values.yaml` file
 `--prod`, `-p`              |  `False`                      | Enables `prod` mode (e.g. enables regular expression matching)
 `--expression`, `-e`        |  `v[0-9].[0-9].[0-9]`         | Expression that tag should match if `prod` mode is enabled
 `--yaml_path`, `-y`         |  `image.tag`                  | A field that should be changed, nested fields separated with 

## Quick start

For quick start you can run `helm_tag_updater` locally in a container and download `examples/manifest.yaml` file.

```bash
docker run -it --rm --name helm_tag_updater fayvori/helm_tag_updater:1.0 /bin/sh
wget https://raw.githubusercontent.com/fayvori/helm_tag_updater/main/examples/manifest.yaml
```

Update tag in development mode

```bash
helm_tag_updater -t 3c5aec6 -f $(pwd)/manifest.yaml

cat manifest.yaml | head -n 15
```

![dev update](./assets/dev-update.jpeg)

Production mode regular expression matching (for default value see `Usage`)

```bash
helm_tag_updater -t v0.0.1 -f $(pwd)/manifest.yaml -p

cat manifest.yaml | head -n 15
```

![prod mode](./assets/prod-update.png)

*Attempt to run in production mode with not matching tag*

![prod mode attempt](./assets/prod-mode-attempt.png)

Running with custom tag matching regular expression and yaml path

![custom tag matching and yaml path](./assets/custom-tag-and-regular-expression.jpeg)

## Contributing

If you want to submit a pull request to fix a bug or enhance an existing
feature, please first open an issue and link to that issue when you
submit your pull request.

If you have any questions about a possible submission, feel free to open
an issue too.

### Pull request process

1. Fork this repository
1. Create a branch in your fork to implement the changes. We recommend using
the issue number as part of your branch name, e.g. `1234-fixes`
1. Ensure that any documentation is updated with the changes that are required
by your fix.
1. Ensure that any samples are updated if the base image has been changed.
1. Submit the pull request. *Do not leave the pull request blank*. Explain exactly
what your changes are meant to do and provide simple steps on how to validate
your changes. Ensure that you reference the issue you created as well.
The pull request will be review before it is merged.

## Made by

- [fayvori](https://github.com/fayvori)

## License

```
MIT License

Copyright (c) 2023 Ignat Belousov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
