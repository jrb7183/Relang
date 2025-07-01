# Relang

This application aims to help conlangers break free of their latent habits when approaching new languages. Relang analyzes aspects of conlangers' old protolangs to find commonalities amongst them and suggests a protolang that breaks from those commonalities.

Relang is currently a WIP, so it only has limited functionality. Currently, I am focused on the phonology pipeline. Specifically, I am working on the Phoneme Selector (see diagram below). The program does run, but it can only generate phonologies at this point. The phonologies it generates have not been the most naturalitsic, so that is what I am focusing on right now.

![image](https://github.com/user-attachments/assets/63b409f4-a003-47e9-a1a6-6ea7f82bc152)

## Generating Phonologies

Once the repository is cloned, you can generate a phonology using the command `python selphone/selectPhonemes.py [num] [temperature]`. Both `[num]` and `[temperature]` are required parameters. 

You can specify the number of phonemes you would like with `[num]`. 

So the program does not produce the same phonology every time, there is a degree of randomness `[temperature]` (analogous to an LLM model's temperature) that picks from a range of the most probable variables instead of just selecting the most probable one. `[temperature]` must be a rational number between `0` and `1`, where `1` is completely random, and `0` selects only the most probable phoneme. A value of `0.0001` has given me the best results so far, and anything less than `1e-5` is essentially equivalent to `0`. 

Previously, I restricted access to `consCorrespondences.json` and `vowelCorrespondences.json`. You can gain access to them by downloading the `data` folder from the `cat-prob` branch.
