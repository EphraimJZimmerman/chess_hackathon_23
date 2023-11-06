# The Legendary Grob Bot

## Quickstart

```
pip install -r requirements.txt

python -m grob
```

## Visualization

```
pip install -r requirements.txt
pip install -r dev_requirements.txt

jupyter lab
```


# The Brandeis Quant Club ML/AI Competition

**Project Description**: In this Python-driven competition, you will be building a model to play chess. Specifically, given any arbitrary position, what is the next best move?


## Getting Started

1. Clone this repository.
2. Install required dependencies using `pip install -r requirements.txt`
3. Run the application using `python bot.py`

## Submission

1. A team member is responsible for uploading a link to your `chess_hackathon_23` fork, accompanied by a video that provides an in-depth explanation of your code and overall logic. All team members are expected to appear in the video, which should have a duration of 2-3 minutes.
2. You have until 11:59pm on November 12th, 2023 to submit your build to [DevPost](https://quants.devpost.com/). 

## Rules

1. Apart from the libraries listed in the requirements.txt file, you're allowed to utilize only scikit-learn, pandas, and numpy.
2. You're free to consult online resources, such as research papers, ChatGPT, or YouTube videos, for reference. However, direct copying of open-source solutions from platforms like GitHub or using APIs is not permitted.
3. You are permitted to have up to 4 members working with your team. You must be a part of the Brandeis University community.
## Usage 

This skeleton is heavily derived from the [python-chess](https://python-chess.readthedocs.io/en/latest/) open-source library. You may use any aspect of this library for the purposes of building your bot (other than calling premade models to determine moves). 

The code skeleton involves a straightforward interaction between your code and an example bot inside of `test_bot.py`. Depending on the configuration, the example bot will either select a random piece or opt for the best possible move, if applicable.

The central logic of your bot should be contained within the `next_move(self) -> str:` function. When provided with a chessboard, this function is responsible for identifying the optimal next move for either the white or black pieces. This task can be challenging and necessitates a good grasp of the python-chess library. You may create any additional python functions or classes. Do **not** create any additional Python files, though. 

Ensure you have a solid understanding of Chess board notation. While there are several methods to input commands (moves) into the `python-chess` library, it's generally advisable to use the initial move-to, new move format, like`e2e3`. While it's sometimes possible to use a simpler format, such as `e3`, where the library will move the only valid piece to that location, it's recommended to avoid this approach for the sake of simplicity.

## Forsyth-Edwards Notation (FEN)

The board can be initialized as a new game or it can be passed a FEN board confirguation. I.e., `chess_bot = Bot()` or `chess_bot = Bot("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")`, for example. 

A list of puzzles with their corresponding FEN has been added in the `puzzles.txt` file. This will be extremely useful when testing the efficacy of your bot. It is recommended you build additional testing functions in the `test_bot.py` file to utilize these puzzles systematically. 
