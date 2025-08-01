# Relang

This application aims to help conlangers break free of their latent habits when approaching new languages. Relang analyzes aspects of conlangers' old protolangs to find commonalities amongst them and suggests an outline for protolang that breaks from those commonalities. **While Relang can generate many aspects of a protolang, it is truly meant for inspiration.** 

Relang is currently a WIP, so it only has limited functionality. Currently, I am focused on the phonology pipeline. At this point, every part of it is up and running (for consonants), so I am focused on refining Relang Probs and the Phoneme Selector (see the diagram below). The program can take in phonologies as inputs, but they are currently hard-coded. Before I continue refining Relang Probs and the Phoneme Selector, I am going to implement a way to input phonologies on the application's frontend.

<img width="1645" height="685" alt="image" src="https://github.com/user-attachments/assets/b8d61ad3-24b2-47bf-b795-d48ec39fdf23" />

## Generating Phonologies
Once the repository is cloned, use the command `cd src` to switch to the main directory, and then type `python main.py test {option}` to run the application. For `{option}`, you can either choose `base` or `relang`. If you type `base`, it will just generate a phonology with a random number of consonants. On the other hand, typing `relang` will allow you to input phonologies to impact the output (though they must be hardcoded if you are only running the app on the backend). 

You can also view the output on the website by using the command `python main.py app`. You can simply generate a phonology using the base probabilities by leaving the phonology inputs blank, or you can add at least one of your phonologies to influence the output.

## Old Phonology Selector

Once the repository is cloned, you also have the option to use the old phonology selector. In the base directory, use the command `python old_files/selectPhonemes.py [num] [temperature]`. Both `[num]` and `[temperature]` are required parameters. Similar to the current phoneme selector, you can specify the number of phonemes you would like with `[num]`. 

So the program did not produce the same phonology every time, there was a degree of randomness `[temperature]` (analogous to an LLM model's temperature) that picked from a range of the most probable variables instead of just selecting the most probable one. `[temperature]` must be a rational number between `0` and `1`, where `1` is completely random, and `0` selects only the most probable phoneme. A value of `0.0001` had given me the best results with the old setup, and anything less than `1e-5` was essentially equivalent to `0`.
