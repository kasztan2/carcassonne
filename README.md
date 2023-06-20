# Documentation
The pre-built documentation is in folder `docs`.  
The *very easy to read* UML diagrams generated with pyreverse can be found at `docs/diagrams`.

# Game controls
`return` - submit form / end program at the end  
`r` - rotate tile  
`tab` - change meeple position

# Building binaries
Binaries can be created using `pyinstaller`:  
```bash
pyinstaller main.spec
```
.  
The binary will be `dist/main`.

# Things to improve
There is a possibility that the randomly picked tile cannot be placed at any position, in that case the tileset should be shuffled.  
Overall code quality... it's terrible