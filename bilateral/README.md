# Bilateral Experiment

This is the code and data for the comparison between a bilateral persuasion scenario and a trilateral one (Section 5.4 of the paper).

## Code
- `generate_judge_prompts_bilateral.py`: generate prompts without any arguments: facts and legal issue only.
- `generate_judge_prompts_bilateral_2.py`: present judge with arguments counter to its initial decision, without including its initial decision.
- `generate_judge_prompts_bilateral_3.py`: present judge with arguments counter to its initial decision,  including its initial decision.
- `merge-bilateral.py`: generate results file

## Data
In this folder `-initial` refers to the response of the Judge when presented only with the facts and legal issue, `-2` refers to when the Judge also has been presented with an argument counter to its original decision, but not the original decision, and `-3` refers to when the Judge was presented with its own decision plus a counter-argument.

- `judgments-*` Judge model outputs
- `outcomes-*` Extracted outcomes from Judge outputs
- `bilateral_scenarios.csv` - scenarios used for bilateral experiments
- `bilateral_results.csv` - aggregated results of bilateral experiment (Table 5)