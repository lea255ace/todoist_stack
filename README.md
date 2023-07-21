# Todoist Stack

This is a tool that integrates with Todoist to help you to maintain a mental stack.
It provides two basic operations, push and pop.

The push operation will add a task with the given description to the Stack project. \
The pop operation will locate the most recent active task in the Stack project and apply the 'stackdone' label

To view the stack effectively, I recommend that you create a Todoist filter as follows: `#Stack & !@stackdone` \
Set your custom view to sort by date added in descending order so that the most recent item
is always at the top of the stack.

## Dependencies
This tool makes use of the Todoist REST API via the python SDK, which is distributed via PyPI.
It can be installed as follows:
```bash
$ pip install todoist-api-python
```
This SDK is only tested against python 3.9, so it is recommended that you use that version to run this tool.

## Configuration
The python SDK authenticates by use of an API key, which can be found in your Todoist settings under
Integrations->Developer->API token. By default, this tool will look for the API key under the environment variable
`TODOIST_API_KEY`. If you wish, you can provide it in a file instead using the `--key_file` flag.<sup>1</sup>

By default, tasks will be pushed and popped from the default Todoist project 'Stack.' If you wish to override this
behavior, you can provide an alternate project name with the `--proj_name` flag, or directly provide the project ID
with the `--proj_id` flag.

<sup>1</sup> Not yet implemented.

