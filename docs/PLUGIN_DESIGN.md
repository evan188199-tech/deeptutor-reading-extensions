# Modular reading plugins

A repository is a maintenance boundary, not an installation boundary. This repository builds five independent wheels: the convenient three-action bundle, one wheel for each action, and a tiny offline dictionary example. Installing one component does not install the bundle or the other components.

## Provider contract

The host owns verified reading context, rendering, account permissions and action execution. A provider receives `ReadingContext` and returns a schema-validated card, quiz, feedback or browser-speech result. It cannot install frontend JavaScript. Python plugins execute with backend permissions and must come from a trusted publisher; namespace validation is not a sandbox.

- Package: a unique `deeptutor-reading-*` distribution with a matching underscore Python namespace.
- Wheel: pure Python, at most 10 MB, depends only on a compatible DeepTutor host.
- Include `<namespace>/reading_plugin.json`: `{"protocol":"1","name":"My dictionary"}`.
- Register `deeptutor.reading_extensions` entry points inside that namespace.
- Each entry-point name must match its `ReadingExtensionManifest.id`.
- To supply the fixed word-lookup action, implement ID `vocabulary`, action `explain`, and require `selection`. Read-aloud uses `read_aloud/read`; quiz uses `quiz/start` and `quiz/grade`.
- Novel IDs, such as `anki_export`, are allowed and appear under More after an administrator selects their provider. Only declared result schemas are supported; new browser interaction types require a host protocol change.
- Installation never automatically selects a provider. Multiple providers can coexist. Select one per action; use the default option to return to the bundled implementation.
- Disable the corresponding action to hide it globally. Learner grants still govern discovery and execution. Additional action IDs require appropriate learner authorization.
- Installation, update, selection and removal take effect after all backend workers restart. Wheels remain immutable while older workers may use them. Uninstall removes the registration, not user learning data.

See [dictionary.py](../examples/dictionary.py) for a three-entry, original glossary that needs no API key. It is a contract demonstration, not a comprehensive or authoritative dictionary. Change the package name, namespace and manifest before publishing a derivative.

## Candidate plugins

These are design directions, not shipped features or promises of integration.

| Plugin | Role | Additional host interface needed |
| --- | --- | --- |
| Subject dictionary / terminology bank | Alternative vocabulary provider with source and edition | Dictionary adapter and optional owner-scoped credential settings |
| Bilingual alignment / translation | Additional action or alternative translation provider | Existing context/card contract can support an initial version |
| Vocabulary collection and Anki export | Save selected words with provenance; export review cards | User-scoped persistence and explicit export/download protocol |
| Annotation export (Markdown / Obsidian) | Export selected annotations with locators | Read-authorized annotation enumeration and export protocol |
| Formula / symbol glossary | Explain symbols in current mathematical context | Existing context/card contract for a text-first provider |
| Citation and evidence checker | Compare a selected claim with permitted references | Explicit retrieval and source-attribution contract |
| Accessibility reading | Alternative speech preparation, terminology pronunciation | Browser speech contract today; voices/audio require host support |
| Spaced review / learning analytics | Schedule reviews and summarize learning progress | Account-scoped learning records; tracked upstream separately |

Avoid exposing arbitrary file paths, browser scripts, shell execution or provider credentials through reader payloads. APIs for persistence, exports and network providers should be explicit, versioned, and account-scoped before those plugins ship.

## Open-source references

- [calibre plugin API](https://manual.calibre-ebook.com/plugins.html): typed extension points and plugin metadata. We adopt a stable host contract rather than allowing unrestricted UI replacement.
- [Anki add-on management](https://docs.ankiweb.net/addons.html): independent install/remove lifecycle and visible compatibility concerns. We expose active and selected versions and require restart.
- [pluggy discovery](https://pluggy.readthedocs.io/en/stable/): discover installed providers through Python entry points. DeepTutor retains entry-point discovery and uses explicit selection to resolve competing providers.

These are architectural references, not runtime dependencies. We do not claim compatibility with their plugin packages.

## Reading-session models (v0.2.1)

Providers that call the host LLM should declare `requires_llm=True` in their `ReadingExtensionManifest`. The updated host validates the reading conversation's selected model against account grants and activates its configuration for the action, including synchronous worker calls. Use the host's `complete()` inside that scope; do not replace it with `task_llm_scope()`.

Leave `requires_llm=False` for offline dictionaries and browser speech. They remain usable when no model is configured. Providers should raise failures instead of returning a success-shaped error card: the host distinguishes invalid output from provider failures and attaches a safe request identifier. Async timeout cancellation must be allowed to propagate; synchronous work cannot be forcibly stopped and blocks another call until it finishes.
