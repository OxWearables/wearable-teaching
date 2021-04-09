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

## Sample files in case data collection fails

There is a two-day camera and accelerometer data for people to use in the future in case for some reason the students cannot collect or fail to collect their own data. This data was collected in Mar, 2021 and is being stored in rescomp under `/well/doherty/projects/stuff/teaching`.

