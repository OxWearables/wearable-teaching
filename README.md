# CDT-Wearable-Teaching
`src` stores raw `.md` files for editing the practical instructions;
`practicals` stores files given to students in their CDT server.


## Creating `.pdf` instruction files

The `src` folder contains practical sheets for students in `.md` format.

To turn them into pdfs, one should use grip.
```bash
pip install grip
grip src/prac1-deviceSetup.md --export
```
This will create a web page which you can use to print as PDF.
