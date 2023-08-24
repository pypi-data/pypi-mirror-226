# twitter-conversation

This repository contains a Python project for obtaining Twitter conversations using the [Tweepy](https://www.tweepy.org) library.
The project allows you to reconstruct conversations based on conversation IDs or search for conversations based on specific topics. It also provides
functionality to "moisturize" dehydrated tweets with text.

## Installation

The project can be installed via [PyPI](https://pypi.org/project/twitter-conversation/) using pip. Run the following command to install the package:

```shell
pip install twitter-conversation
```

Alternatively, you can clone this repository and install the project locally. Follow these steps:

1. Clone this repository:

   ```shell
   git clone https://gitlab.cs.uni-duesseldorf.de/feger/twitter-conversation.git
   ```

2. Change into the project directory:

   ```shell
   cd twitter-conversation
   ```

3. Install the project dependencies using Poetry:

   ```shell
   poetry install
   ```

## Configuration

Before running the script, make sure to configure the following:

1. Set the `BEARER_TOKEN` environment variable with your Twitter API bearer token. You can set the variable using one of the following methods:


- Export the variable in the terminal:
  ```shell
  export BEARER_TOKEN=your_bearer_token
  ```
- Create a `.env` file in the project directory and set the variable:
  ```plaintext
  BEARER_TOKEN=your_bearer_token
  ```

**Note:** The `BEARER_TOKEN` is obtained from the Twitter Developer Program and is required for accessing the Twitter API v2. If you don't have a
bearer token, you can apply for one [here](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens).

2. Review and update the configuration options in the `pyproject.toml` file according to your needs.

## Usage

The project provides a command-line interface (CLI) with different options for obtaining and processing Twitter conversations. You can run the CLI
using Poetry by adding ```poetry run``` to this command:

```shell
obtain <options>
```

Replace `<options>` with the appropriate command and arguments based on your requirements. Here are the available options:

### Single Conversation Mode

To reconstruct a single conversation using a conversation ID, use the following command:

```shell
obtain single_conversation -c <conversation_id>
```

Replace `<conversation_id>` with the ID of the conversation you want to reconstruct.

### Multiple Conversations Mode

To reconstruct multiple conversations using a CSV file containing conversation-starting tweet IDs, use the following command:

```shell
obtain multiple_conversations -s <starting_tweets_csv_file> [-i <index_column_name>]
```

Replace `<starting_tweets_csv_file>` with the path to the CSV file that contains the conversation-starting tweet IDs. Optionally, you can specify the
index column name using the `-i` or `--index` flag.

### Search Conversations Mode

To obtain conversations by searching for root tweets based on a specific topic, use the following command:

```shell
obtain search_conversations -t <topic>
```

Replace `<topic>` with the topic word (e.g., hashtag) that should be present in the root tweets. The script will search for relevant tweets in English
that are not replies, retweets, or quotes.

### Moisturize Tweets Mode

To "moisturize" dehydrated tweets with text using a CSV file, use the following command:

```shell
obtain moisturize_tweets -d <dry_tweets_csv_file> [-i <index_column_name>]
```

Replace `<dry_tweets_csv_file>` with the path to the CSV file that contains the dehydrated tweet IDs. Optionally, you can specify the index column
name using the `-i` or `--index` flag.

### Additional Options

The project provides the following additional options:

- `-h/--help`: The detailed manual for each option.
- `-s/--start`: The UTC time in the past to start the search (default: today at 0 o'clock).
- `-e/--end`: The UTC time to end the search (default: current time).
- `-p/--path`: The path to the CSV file where the obtained tweets should be written (default: './reply_tree.csv').
- `-or/--only-root`: By using this flag, only the root tweets will be obtained, and the reply tweets are skipped.

Make sure to configure these additional options as per your requirements.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please submit an issue or a pull request. We appreciate your
feedback and involvement in improving this project.

## License

<p>
    <a property="dct:title" rel="cc:attributionURL" href="https://pypi.org/search/?q=twitter-conversation">twitter-conversation</a> by 
    <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="mailto:marc.feger@icloud.com">Marc Feger</a> is licensed under
    <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0</a>
    <div style="display:block;">
        <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1">
        <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">
        <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1">
        <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1">
    </div>
</p>

Feel free to explore the project and customize it to suit your needs. If you encounter any issues or have suggestions for improvement, please submit
an issue or pull request. Happy coding!