# Converts Hexadecimal Unicode Codes with the prefix 'U+/u+' in text to Corresponding Characters

## Tested against Windows 10 / Python 3.10 / Anaconda

## pip install unicodekonverter


```python
    Converts Hexadecimal Unicode Codes with the prefix 'U+/u+' in text to Corresponding Characters

    This function takes a text containing hexadecimal Unicode codes and replaces them with their corresponding
    characters. It utilizes a precompiled Trie regex pattern (compiled at the first run) to efficiently
    identify and replace the Unicode codes.

    Args:
        tex (str): The input text containing hexadecimal Unicode codes to be converted.
        concurrent (int or None): The number of concurrent threads to use during pattern matching.
            If provided, the function will use multiple threads to process the text concurrently.
            Set to None (default) to disable concurrent processing.

    Returns:
        str: The input text with hexadecimal Unicode codes replaced by their corresponding characters.

    Example:

text2='''
U+25A0	Black square
U+25A1	White square
U+25A2	White square with rounded corners
U+25A3	White square containing small black square
U+25A4	Square with horizontal fill
U+25A5	Square with vertical fill
U+25A6	Square with orthogonal crosshatch fill
U+25A7	Square with upper left to lower right fill
U+25A8	Square with upper right to lower left fill
U+25A9	Square with diagonal crosshatch fill
U+25AA	Black small square
U+25AB	White small square
U+25AC	Black rectangle
U+25AD	White rectangle
U+25AE	Black vertical rectangle
U+25AF	White vertical rectangle
U+25B0	Black parallelogram
U+25B1	White parallelogram
U+25B2	Black up-pointing triangle
U+25B3	White up-pointing triangle
U+25B4	Black up-pointing small triangle
U+25B5	White up-pointing small triangle
U+25B6	Black right-pointing triangle
U+25B7	White right-pointing triangle
U+25B8	Black right-pointing small triangle
U+25B9	White right-pointing small triangle
U+25BA	Black right-pointing pointer
U+25BB	White right-pointing pointer
U+25BC	Black down-pointing triangle
U+25BD	White down-pointing triangle
U+25BE	Black down-pointing small triangle
U+25BF	White down-pointing small triangle
U+25C0	Black left-pointing triangle
U+25C1	White left-pointing triangle
U+25C2	Black left-pointing small triangle
U+25C3	White left-pointing small triangle
U+25C4	Black left-pointing pointer
U+25C5	White left-pointing pointer
U+25C6	Black diamond
U+25C7	White diamond
U+25C8	White diamond containing small black diamond
U+25C9	Fisheye
U+25CA	Lozenge
U+25CB	White circle
U+25CC	Dotted circle
U+25CD	Circle with vertical fill
U+25CE	Bullseye
U+25CF	Black circle
U+25D0	Circle with left half black
U+25D1	Circle with right half black
U+25D2	Circle with lower half black
U+25D3	Circle with upper half black
U+25D4	Circle with upper right quadrant black
U+25D5	Circle with all but upper left quadrant black
U+25D6	Left half circle black
U+25D7	Right half black circle
U+25D8	Inverse bullet
U+25D9	Inverse white circle
U+25DA	Upper half inverse white circle
U+25DB	Lower half inverse white circle
U+25DC	Upper left quadrant circular arc
U+25DD	Upper right quadrant circular arc
U+25DE	Lower right quadrant circular arc
U+25DF	Lower left quadrant circular arc
U+25E0	Upper half circle
U+25E1	Lower half circle
U+25E2	Black lower right triangle
U+25E3	Black lower left triangle
U+25E4	Black upper left triangle
U+25E5	Black upper right triangle
U+25E6	White bullet
U+25E7	Square with left half black
U+25E8	Square with right half black
U+25E9	Square with upper left diagonal half black
U+25EA	Square with lower right diagonal half black
U+25EB	White square with vertical bisecting line
U+25EC	White up-pointing triangle with dot
U+25ED	Up-pointing triangle with left half black
U+25EE	Up-pointing triangle with right half black
U+25EF	Large circle
U+25F0	White square with upper left quadrant
U+25F1	White square with lower left quadrant
U+25F2	White square with lower right quadrant
U+25F3	White square with upper right quadrant
U+25F4	White circle with upper left quadrant
U+25F5	White circle with lower left quadrant
U+25F6	White circle with lower right quadrant
U+25F7	White circle with upper right quadrant
U+25F8	Upper left triangle
U+25F9	Upper right triangle
U+25FA	Lower-left triangle
U+25FB	White medium square
U+25FC	Black medium square
U+25FD	White medium small square
U+25FE	Black medium small square
U+25FF	Lower right U+25FF triangle
'''

te=convert_2_unicode(text2)
print(te)

output:

■	Black square
□	White square
▢	White square with rounded corners
▣	White square containing small black square
▤	Square with horizontal fill
▥	Square with vertical fill
▦	Square with orthogonal crosshatch fill
▧	Square with upper left to lower right fill
▨	Square with upper right to lower left fill
▩	Square with diagonal crosshatch fill
▪	Black small square
▫	White small square
▬	Black rectangle
▭	White rectangle
▮	Black vertical rectangle
▯	White vertical rectangle
▰	Black parallelogram
▱	White parallelogram
▲	Black up-pointing triangle
△	White up-pointing triangle
▴	Black up-pointing small triangle
▵	White up-pointing small triangle
▶	Black right-pointing triangle
▷	White right-pointing triangle
▸	Black right-pointing small triangle
▹	White right-pointing small triangle
►	Black right-pointing pointer
▻	White right-pointing pointer
▼	Black down-pointing triangle
▽	White down-pointing triangle
▾	Black down-pointing small triangle
▿	White down-pointing small triangle
◀	Black left-pointing triangle
◁	White left-pointing triangle
◂	Black left-pointing small triangle
◃	White left-pointing small triangle
◄	Black left-pointing pointer
◅	White left-pointing pointer
◆	Black diamond
◇	White diamond
◈	White diamond containing small black diamond
◉	Fisheye
◊	Lozenge
○	White circle
◌	Dotted circle
◍	Circle with vertical fill
◎	Bullseye
●	Black circle
◐	Circle with left half black
◑	Circle with right half black
◒	Circle with lower half black
◓	Circle with upper half black
◔	Circle with upper right quadrant black
◕	Circle with all but upper left quadrant black
◖	Left half circle black
◗	Right half black circle
◘	Inverse bullet
◙	Inverse white circle
◚	Upper half inverse white circle
◛	Lower half inverse white circle
◜	Upper left quadrant circular arc
◝	Upper right quadrant circular arc
◞	Lower right quadrant circular arc
◟	Lower left quadrant circular arc
◠	Upper half circle
◡	Lower half circle
◢	Black lower right triangle
◣	Black lower left triangle
◤	Black upper left triangle
◥	Black upper right triangle
◦	White bullet
◧	Square with left half black
◨	Square with right half black
◩	Square with upper left diagonal half black
◪	Square with lower right diagonal half black
◫	White square with vertical bisecting line
◬	White up-pointing triangle with dot
◭	Up-pointing triangle with left half black
◮	Up-pointing triangle with right half black
◯	Large circle
◰	White square with upper left quadrant
◱	White square with lower left quadrant
◲	White square with lower right quadrant
◳	White square with upper right quadrant
◴	White circle with upper left quadrant
◵	White circle with lower left quadrant
◶	White circle with lower right quadrant
◷	White circle with upper right quadrant
◸	Upper left triangle
◹	Upper right triangle
◺	Lower-left triangle
◻	White medium square
◼	Black medium square
◽	White medium small square
◾	Black medium small square
◿	Lower right ◿ triangle

```