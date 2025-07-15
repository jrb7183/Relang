# Relang

This application aims to help conlangers break free of their latent habits when approaching new languages. Relang analyzes aspects of conlangers' old protolangs to find commonalities amongst them and suggests a protolang that breaks from those commonalities.

Relang is currently a WIP, so it only has limited functionality. Currently, I am focused on the phonology pipeline. Specifically, I am working on the Phoneme Selector (see diagram below). The program does run, but it can only generate phonologies at this point. The phonologies it generates have not been the most naturalitsic, so that is what I am focusing on right now.

![image](https://github.com/user-attachments/assets/63b409f4-a003-47e9-a1a6-6ea7f82bc152)

## Generating Phonologies
Once the repository is cloned, use the command `cd src` to switch to the main directory, and then type `python main.py test [num]` to run the application. You can specify the number of phonemes you would like with `[num]`. If you want to view the output on the website instead, use the command `python main.py app`.

## Old Phonology Selector

Once the repository is cloned, you also have the option to use the old phonology selector. In the base directory, use the command `python old_files/selectPhonemes.py [num] [temperature]`. Both `[num]` and `[temperature]` are required parameters. Similar to the current phoneme selector, you can specify the number of phonemes you would like with `[num]`. 

So the program does not produce the same phonology every time, there is a degree of randomness `[temperature]` (analogous to an LLM model's temperature) that picks from a range of the most probable variables instead of just selecting the most probable one. `[temperature]` must be a rational number between `0` and `1`, where `1` is completely random, and `0` selects only the most probable phoneme. A value of `0.0001` has given me the best results so far, and anything less than `1e-5` is essentially equivalent to `0`.
