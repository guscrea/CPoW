**Here are some notes and instructions for using this script!**

- OpenAI's API is currently designed to be stateless; this means each API call is treated as an independent request, without knowledge of past interactions. That's good for us, as it means impartiality across repeated trial runs!

- run file_manager.py FROM THE RUN_QUERYING_SCRIPT DIRECTORY.

- Articles should be grouped in folders by wind energy project, and in Newsbank format. They should be stored in ../Data_newspapers_sample, though this can be changed in file_manager.py (news_data_rel_path = ???)

- Other file paths (e.g. for codebook, which should be in run_querying_script/resources/ directory) can also be changed manually; I've hard-coded some of them to run in my personal directory, but that was just to help with debugging; I'll definitely change that if we share this script around.

- Each run of the script codes the articles in our input folder; output is written into output.csv, and file_manager.py then attempts to rename this file with the current timestamp and then replace output.csv with a blank file. If this doesn't work, results are still saved in output.csv, and new rows will be added to existing entries.

- Find all outputs in the output folder!