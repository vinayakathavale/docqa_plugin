# Document QA Plugin for insurance policy docs

This plugin allows you to inquire about specific travel insurance policy documents stored in its database. Furthermore, you have the option to link new insurance policy PDFs and pose questions about them.

![Alt text](images/example.png?raw=true "Title")

# Setup locally

1. To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements.txt
```

2. Download a bunch of insurance policy pdf documents (or any pdf documents for that matter) and save them in a folder called docs.


3. To run the plugin, enter the following command:

```bash
python main.py
```



Once the local server is running:

1. Navigate to https://chat.openai.com. 
2. In the Model drop down, select "Plugins" (note, if you don't see it there, you don't have access yet).
3. Select "Plugin store"
4. Select "Develop your own plugin"
5. Enter in `localhost:5003` since this is the URL the server is running on locally, then select "Find manifest file".

The plugin should now be installed and enabled! 



Todo:

1. Move the index to a database
2. Add tests to check output of the plugin
