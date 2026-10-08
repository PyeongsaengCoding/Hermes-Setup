## Document delivery in Hermes Desktop

After creating or updating a document, include its containing folder as a selectable card in the chat. Use the built-in directive on its own line: `::preview{file="/absolute/path/to/containing/folder"}`. Resolve the real existing directory; do not use a placeholder. The local directory card provides the user-triggered Open containing folder action. A document attachment or .md preview alone is not sufficient; it may be included in addition to the folder card. For several documents in the same directory, show one folder card.

Do not automatically open Finder, another file manager, an editor, or a preview pane when delivering documents. Do not run `open`, `open -R`, or an equivalent reveal/open action just to show the output. Let the user select Open containing folder / Open in in the chat. Open an application only when the user explicitly asks for that immediate action.
