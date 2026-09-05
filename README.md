# DeepTutor reading extensions

Three independently authorized actions in one Python wheel: read aloud,
contextual word lookup, and reading-comprehension quizzes.

Requires DeepTutor 1.6.4 or later (before 2.0), Python 3.11–3.14,
and Reading protocol 1. The managed installer requires the host integration
in HKUDS/DeepTutor PR #1233 (or a release containing it).

## Install

Download the versioned wheel from this repository's Releases.
In DeepTutor, open Settings → Reading extensions and upload the wheel, or run:

```sh
deeptutor plugin reading install ./deeptutor_reading_extensions-0.1.0-py3-none-any.whl
deeptutor plugin reading list
```

Restart the backend after installation, updates, changes to enabled actions,
or uninstall. No frontend rebuild is needed after the host integration is deployed.
The managed package lives under the runtime home's data/system/reading-plugins,
so retain the data volume when rebuilding a container.

`deeptutor plugin reading uninstall` disables the three actions after restart.
`deeptutor plugin reading restore` restores the host's bundled versions.

Standard Python entry-point installation also works with the integrated host:
`python -m pip install ./deeptutor_reading_extensions-0.1.0-py3-none-any.whl`
using the backend interpreter. Use either managed installation or pip; the
managed lifecycle takes precedence when configured.

## Develop

```sh
python -m pip install build
python -m build --wheel
```

The implementation originates from HKUDS/DeepTutor and retains its Apache-2.0
license. The package uses the host's verified ReadingContext and LLM services.
It does not bundle provider credentials or material data.
