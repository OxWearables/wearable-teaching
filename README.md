# CDT-Wearable-Teaching
`docs` stores raw `.md` files for editing the practical instructions; 
`to_upload` stores files given to students in their CDT server.


## Creating `.pdf` instruction files

The `docs` folder contains practical sheets for students in `.md` format. 

To turn them into pdfs, `pandoc` is required.

### Setup 

* Create folders for pandoc, and then install it 
```bash
mkdir ~/.pandoc
mkdir ~/.pandoc/templates/

curl https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex -o ~/.pandoc/templates/eisvogel.latex
brew install pandoc
```

* Install necessary latex packages
```bash
brew cask install basictex
tlmgr update --self
sudo tlmgr install footnotebackref, csquotes, mdframed, needspace
sudo tlmgr install sourcesanspro, sourcecodepro, titling
sudo tlmgr install collection-fontsrecommended
```

* Convert practical MD to PDF
```bash
cd docs
pandoc ./prac1.md -o ./prac1.pdf --from markdown --template eisvogel --listings --pdf-engine xelatex
```

<!-- pandoc ./prac4.md -o ../to_upload/prac4.pdf --from markdown --template eisvogel --listings --pdf-engine xelatex -->

<!-- pandoc ./prac3.md -o ../to_upload/prac3.pdf --from markdown --template eisvogel --listings --pdf-engine xelatex -->

For some reason, it is not easy to convert MD to PDF via LaTeX. Alternatively, one should use grip.
```bash
pip install grip
grip sample.md
```
This will create a web page which you can use to print as PDF.

