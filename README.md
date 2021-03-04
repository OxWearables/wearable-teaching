# CDT-Wearable-Teaching
`docs` stores raw `.md` files for editing the practical instructions;
`to_upload` stores files given to students in their CDT server.


## Creating `.pdf` instruction files

The `docs` folder contains practical sheets for students in `.md` format.

To turn them into pdfs, one should use grip.
```bash
pip install grip
grip sample.md --export sample.html
```
This will create a web page which you can use to print as PDF.
