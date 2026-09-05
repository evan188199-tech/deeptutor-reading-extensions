"""Small original glossary illustrating the provider contract, not a full dictionary."""
from deeptutor.reading.extensions import (
    ReadingAction, ReadingContext, ReadingExtensionManifest, ReadingExtensionResult,
)

TERMS = {
    'photosynthesis': 'The process by which plants use light energy to make sugars from carbon dioxide and water.',
    'algorithm': 'A finite sequence of well-defined steps used to solve a problem.',
    'variable': 'A named quantity whose value can change or be assigned in a calculation.',
}


class DictionaryExtension:
    manifest = ReadingExtensionManifest(
        id='vocabulary', version='0.2.0', name='Offline dictionary example',
        actions=[ReadingAction(id='explain', label='Look up word', requires=['selection'])],
        result_types=['card'],
    )

    def run_action(self, action: str, context: ReadingContext):
        if action != 'explain' or not context.selection.strip():
            raise ValueError('Select a word before looking it up.')
        word = context.selection.strip().casefold()
        definition = TERMS.get(word)
        return ReadingExtensionResult(
            type='card', title=context.selection[:160],
            message=(definition + '\n\nSource: original demonstration glossary (3 entries).') if definition else 'No entry in this demonstration glossary. Try photosynthesis, algorithm or variable.',
        )
