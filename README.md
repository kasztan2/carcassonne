# Documentation
The pre-built documentation is in folder `docs` (both in html and pdf).  
The *very easy to read* UML diagrams generated with pyreverse can be found at `docs/diagrams` (they have cycles, probably because TYPE_CHECKING value is ignored in pyreverse?).

# Game controls
`return` - submit form / end program at the end  
`r` - rotate tile  
`tab` - change meeple position

# Running the game (using python interpreter)
```bash
pip install -r requirements.txt
python3 main.py
```

# Building binaries
Binaries can be created using `pyinstaller`:  
```bash
pyinstaller main.spec
```
.  
The binary will be `dist/main`.

# Things to improve
1. There is a possibility that the randomly picked tile cannot be placed at any position, in that case the tileset should be shuffled.  
2. Overall code quality... it's terrible.  
3. Obviously: graphics