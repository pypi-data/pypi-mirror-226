## Pegwords

I read Harry Lorayne's book [How to Develop a Super Power
Memory](https://www.amazon.com/How-Develop-Super-Power-Memory/dp/0811901815)
back in about 1979 and spent a lot of time becoming quite good at
memorizing numbers by turning them in words using the "phonetic alphabet"
therein.

Last night I decided to write a couple of quick scripts to make it easy to
pick a sequence of long words to memorize.

### Installation

```sh
$ pip install pegwords
```

### Usage

There are two scripts here:

#### Making a list of words given a sequence of digits

This is interactive. Try it on the first 50 digits of Pi:

```sh
$ ./digits-to-words.py 1415926535897932384626433832795028841971693993751
```

The program will read `/usr/share/dict/web2` (or pass a dictionary file
using `--dictionaryFile`) and will then prompt you to pick one word at a
time to build a sequence of words matching the given string of digits.

At each step you can type:

* A number to choose your next word from the current list of candidates.
* `?` to see the current list.
* `-` to make the matched prefix one character shorter (= more words to choose from).
* `+` to make the matched prefix one character longer (= fewer words to choose from).
* `q` to quit.

#### Getting the sequence of digits for a list of words

Simpler is going the other way:

```sh
$ ./words-to-digits.py hello world
4 digits (5451) covered by 2 words:
  DIGITS: 5     451
  WORDS:  hello world
```

And if you want to check a sequence of words has the expected digit sequence:

```
$ ./words-to-digits.py --expected 5456 hello world
4 digits (5451) covered by 2 words:
  DIGITS: 5     451
  WORDS:  hello world
Result '5451' does not match expected '5456'!
EXPECTED: 5456
             |
RECEIVED: 5451
For word 'world', expected '456' but the correct value is '451'.
```
