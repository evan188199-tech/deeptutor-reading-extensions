"""Build independent wheels from this monorepo; no shared package is required."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
VERSION = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']['version']
SOURCES = {
    'read-aloud': ('Read aloud', 'read_aloud', 'ReadAloudExtension'),
    'vocabulary': ('Contextual vocabulary', 'vocabulary', 'VocabularyExtension'),
    'quiz': ('Reading quiz', 'quiz', 'ReadingQuizExtension'),
    'dictionary-example': ('Offline dictionary example', 'vocabulary', 'DictionaryExtension'),
}
for suffix, (label, slot, symbol) in SOURCES.items():
    name = 'deeptutor-reading-' + suffix
    namespace = name.replace('-', '_')
    directory = ROOT / 'build' / 'providers' / suffix
    directory.mkdir(parents=True, exist_ok=True)
    package = directory / namespace
    package.mkdir(exist_ok=True)
    (package / '__init__.py').write_text('')
    (package / 'reading_plugin.json').write_text(json.dumps({'protocol': '1', 'name': label}))
    if suffix == 'dictionary-example':
        shutil.copy(ROOT / 'examples' / 'dictionary.py', package / 'vocabulary.py')
    else:
        for module in [slot, '_grounding']:
            text = (ROOT / 'deeptutor_reading_extensions' / (module + '.py')).read_text()
            (package / (module + '.py')).write_text(text.replace('deeptutor_reading_extensions.', namespace + '.'))
    shutil.copy(ROOT / 'LICENSE', directory / 'LICENSE')
    (directory / 'pyproject.toml').write_text(f'''[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"
[project]
name = "{name}"
version = "{VERSION}"
description = "{label} for DeepTutor"
requires-python = ">=3.11,<3.15"
dependencies = ["deeptutor>=1.6.4,<2"]
license = {{text = "Apache-2.0"}}
[project.entry-points."deeptutor.reading_extensions"]
{slot} = "{namespace}.{slot}:{symbol}"
[tool.setuptools.package-data]
"*" = ["reading_plugin.json"]
''')
    subprocess.run([sys.executable, '-m', 'build', '--wheel', '--no-isolation', '--outdir', str(ROOT / 'dist'), str(directory)], check=True)
